"""Tests for the AST parser module."""

from pathlib import Path

import pytest

from testal.analyzer.ast_parser import discover_python_files, extract_functions
from testal.analyzer.models import FunctionContext

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_MODULE = FIXTURES_DIR / "sample_module.py"


class TestExtractFunctions:
    """Tests for extract_functions."""

    def test_extracts_top_level_functions(self):
        functions = extract_functions(SAMPLE_MODULE)
        names = [f.name for f in functions]
        assert "add" in names
        assert "fetch_data" in names
        assert "async_process" in names
        assert "_private_helper" in names

    def test_extracts_methods_with_class_context(self):
        functions = extract_functions(SAMPLE_MODULE)
        methods = [f for f in functions if f.is_method]
        assert len(methods) == 2  # multiply and divide
        assert all(f.class_name == "Calculator" for f in methods)

    def test_skips_empty_bodies(self):
        functions = extract_functions(SAMPLE_MODULE)
        names = [f.name for f in functions]
        assert "not_implemented" not in names
        assert "also_empty" not in names

    def test_extracts_args_without_self(self):
        functions = extract_functions(SAMPLE_MODULE)
        multiply = next(f for f in functions if f.name == "multiply")
        assert multiply.args == ["x", "y"]
        assert "self" not in multiply.args

    def test_extracts_return_annotation(self):
        functions = extract_functions(SAMPLE_MODULE)
        add_fn = next(f for f in functions if f.name == "add")
        assert add_fn.return_annotation == "int"

    def test_extracts_docstring(self):
        functions = extract_functions(SAMPLE_MODULE)
        add_fn = next(f for f in functions if f.name == "add")
        assert add_fn.docstring == "Add two numbers."

    def test_extracts_decorators(self):
        functions = extract_functions(SAMPLE_MODULE)
        divide = next(f for f in functions if f.name == "divide")
        assert "staticmethod" in divide.decorators

    def test_captures_line_numbers(self):
        functions = extract_functions(SAMPLE_MODULE)
        add_fn = next(f for f in functions if f.name == "add")
        assert add_fn.lineno > 0
        assert add_fn.end_lineno >= add_fn.lineno

    def test_captures_source_code(self):
        functions = extract_functions(SAMPLE_MODULE)
        add_fn = next(f for f in functions if f.name == "add")
        assert "return a + b" in add_fn.source

    def test_empty_file_returns_empty_list(self, tmp_path):
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("")
        assert extract_functions(empty_file) == []


class TestDiscoverPythonFiles:
    """Tests for discover_python_files."""

    def test_single_file(self):
        result = discover_python_files(SAMPLE_MODULE)
        assert result == [SAMPLE_MODULE]

    def test_directory_recursion(self):
        result = discover_python_files(FIXTURES_DIR)
        assert SAMPLE_MODULE in result
        assert all(f.suffix == ".py" for f in result)

    def test_nonexistent_returns_empty(self, tmp_path):
        result = discover_python_files(tmp_path / "nope.txt")
        assert result == []