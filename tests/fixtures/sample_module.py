"""Sample module for testing the AST parser."""


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def fetch_data(url: str, timeout: float = 30.0) -> dict:
    """Fetch data from a URL."""
    import requests

    response = requests.get(url, timeout=timeout)
    return response.json()


class Calculator:
    """Simple calculator for testing method extraction."""

    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y

    @staticmethod
    def divide(x: float, y: float) -> float:
        """Divide x by y."""
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y


async def async_process(items: list[str]) -> list[str]:
    """Process items asynchronously."""
    return [item.upper() for item in items]


def _private_helper():
    """Private helper that still has a body."""
    return 42


class AbstractBase:
    def not_implemented(self):
        """This should be skipped — empty body."""
        pass

    def also_empty(self): ...
