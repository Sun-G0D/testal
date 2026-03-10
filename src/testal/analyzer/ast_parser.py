"""AST-based Python source code parser for function extraction."""

import ast
import textwrap
from pathlib import Path

from testal.analyzer.models import FunctionContext

_FuncNode = ast.FunctionDef | ast.AsyncFunctionDef


def extract_functions(filepath: Path) -> list[FunctionContext]:
    """Parse a Python file and extract all function/method contexts."""
    source = filepath.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(filepath))
    functions: list[FunctionContext] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, _FuncNode):
                    ctx = _node_to_context(item, filepath, source, class_name=node.name)
                    if ctx:
                        functions.append(ctx)
        elif isinstance(node, _FuncNode) and not _is_inside_class(tree, node):
            ctx = _node_to_context(node, filepath, source)
            if ctx:
                functions.append(ctx)

    return functions


def _node_to_context(
    node: _FuncNode,
    filepath: Path,
    source: str,
    class_name: str | None = None,
) -> FunctionContext | None:
    """Convert an AST function node to a FunctionContext."""
    # Skip empty/abstract functions (no meaningful body to test)
    if _is_empty_body(node):
        return None

    lines = source.splitlines()
    func_lines = lines[node.lineno - 1 : node.end_lineno]
    func_source = textwrap.dedent("\n".join(func_lines))

    return FunctionContext(
        name=node.name,
        filepath=str(filepath),
        lineno=node.lineno,
        end_lineno=node.end_lineno or node.lineno,
        source=func_source,
        args=_extract_args(node),
        return_annotation=_extract_return_annotation(node),
        docstring=ast.get_docstring(node),
        decorators=[_decorator_name(d) for d in node.decorator_list],
        is_method=class_name is not None,
        class_name=class_name,
    )


def _extract_args(node: _FuncNode) -> list[str]:
    """Extract argument names, excluding 'self' and 'cls'."""
    return [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]


def _extract_return_annotation(node: _FuncNode) -> str | None:
    """Extract return type annotation as string, if present."""
    if node.returns:
        return ast.unparse(node.returns)
    return None


def _decorator_name(node: ast.expr) -> str:
    """Get the string representation of a decorator."""
    return ast.unparse(node)


def _is_empty_body(node: _FuncNode) -> bool:
    """Check if function body is empty (pass, ellipsis, docstring-only,
    or docstring+pass/ellipsis)."""
    stmts = node.body

    # Filter out the docstring if present
    non_docstring = stmts
    if (
        stmts
        and isinstance(stmts[0], ast.Expr)
        and isinstance(stmts[0].value, ast.Constant)
        and isinstance(stmts[0].value.value, str)
    ):
        non_docstring = stmts[1:]

    # After removing docstring: empty, just pass, or just ellipsis → empty body
    if len(non_docstring) == 0:
        return True  # docstring-only
    if len(non_docstring) == 1:
        stmt = non_docstring[0]
        if isinstance(stmt, ast.Pass):
            return True
        if (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and stmt.value.value is ...
        ):
            return True
    return False


def _is_inside_class(tree: ast.Module, target: ast.AST) -> bool:
    """Check if a node is directly inside a class body (i.e., is a method)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if item is target:
                    return True
    return False


def discover_python_files(path: Path) -> list[Path]:
    """Recursively discover all .py files under a path."""
    if path.is_file() and path.suffix == ".py":
        return [path]
    if path.is_dir():
        return sorted(path.rglob("*.py"))
    return []
