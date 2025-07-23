from enum import Enum, IntEnum, auto

from runtime_docstrings import docstrings, get_docstrings


@docstrings
class Color(IntEnum):
    """Enumeration of basic colors with integer values."""

    RED = 1
    """Represents the color red."""
    GREEN = 2
    """Represents the color green."""
    BLUE = 3
    """Represents the color blue."""

    ALIAS = BLUE

    ALIAS_BY_VALUE = 3

    ALIAS_DOC = GREEN
    """Alias for GREEN color."""

    PURPLE = 4

    ALIAS_AFTER = PURPLE
    """Represents the ALIAS purple."""

    GRAY = 5


@docstrings
class Status(Enum):
    """Enumeration of process statuses with string values."""

    PENDING = "pending"
    """Represents a pending status."""
    RUNNING = "running"
    """Represents a running status."""
    COMPLETED = "completed"
    """Represents a completed status."""


@docstrings
class Shape(Enum):
    """Enumeration of geometric shapes."""

    CIRCLE = auto()
    """Represents a circle."""
    SQUARE = auto()
    """Represents a square."""
    TRIANGLE = auto()
    """Represents a triangle."""


def test_enum():
    assert Shape.CIRCLE.value != Shape.SQUARE.value  # auto() generates unique values
    # assert Shape.TRIANGLE.__doc__ == "Represents a triangle."

    assert get_docstrings(Shape) == {
        "CIRCLE": "Represents a circle.",
        "SQUARE": "Represents a square.",
        "TRIANGLE": "Represents a triangle.",
    }


def test_int_enum():
    assert Color.RED.value == 1
    assert Color.GREEN.name == "GREEN"
    # assert Color.BLUE.__doc__ == "Represents the color blue."
    assert get_docstrings(Color) == {
        "RED": "Represents the color red.",
        "GREEN": "Represents the color green.",
        "BLUE": "Represents the color blue.",
        "ALIAS_DOC": "Alias for GREEN color.",
        "ALIAS_AFTER": "Represents the ALIAS purple.",
    }


def test_alias():
    assert Color.RED.__doc__ == "Represents the color red."

    assert Color.PURPLE.__doc__ == "Represents the ALIAS purple."
    # TODO: should aliases be able to be documented if canonical member isn't?
    assert Color.ALIAS_AFTER.__doc__ == "Represents the ALIAS purple."

    assert Color.__doc__ == "Enumeration of basic colors with integer values."
    # don't inherit the enum docstring (default enum behavior) if attaching member docs to avoid confusion
    assert Color.GRAY.__doc__ is None

    assert Color.ALIAS.__doc__ == "Represents the color blue."
    assert Color.ALIAS_BY_VALUE.__doc__ == "Represents the color blue."
    assert Color["ALIAS"].__doc__ == "Represents the color blue."

    assert Color.ALIAS_DOC is Color.GREEN
    assert Color.ALIAS_DOC.name == "GREEN"
    # will always use the canonical docstring for aliases
    # assert Color.ALIAS_DOC.__doc__ == "Alias for GREEN color."
    cached = get_docstrings(Color)
    assert cached["ALIAS_DOC"] == "Alias for GREEN color."
    cached["ALIAS_DOC"] = "Modified alias docstring."
    assert get_docstrings(Color).get("ALIAS_DOC") == "Modified alias docstring."
    del Color.__attribute_docs__
    assert get_docstrings(Color).get("ALIAS_DOC") == "Alias for GREEN color."

    assert Color.GREEN.__doc__ == "Represents the color green."


def test_str_enum():
    assert Status.PENDING.value == "pending"
    assert Status.RUNNING.name == "RUNNING"
    # assert Status.COMPLETED.__doc__ == "Represents a completed status."

    assert get_docstrings(Status) == {
        "PENDING": "Represents a pending status.",
        "RUNNING": "Represents a running status.",
        "COMPLETED": "Represents a completed status.",
    }
