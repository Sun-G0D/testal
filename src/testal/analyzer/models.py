"""Data models for extracted code structures."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FunctionContext:
    """All metadata extracted from a single function/method for prompt construction."""

    name: str
    filepath: str
    lineno: int
    end_lineno: int
    source: str
    args: list[str] = field(default_factory=list)
    return_annotation: str | None = None
    docstring: str | None = None
    decorators: list[str] = field(default_factory=list)
    is_method: bool = False
    class_name: str | None = None