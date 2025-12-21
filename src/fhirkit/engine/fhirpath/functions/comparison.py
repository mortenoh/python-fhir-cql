"""Comparison functions and operators."""

from decimal import Decimal
from typing import Any

from ...context import EvaluationContext
from ...functions import FunctionRegistry
from ...types import FHIRDate, FHIRDateTime, Quantity


def _normalize_for_comparison(value: Any) -> Any:
    """Normalize a value for comparison.

    Converts date strings to FHIRDate/FHIRDateTime for proper comparison.
    Also unwraps _PrimitiveWithExtension wrappers.
    """
    # Import here to avoid circular imports
    from ..visitor import _PrimitiveWithExtension

    # Unwrap primitive wrappers
    if isinstance(value, _PrimitiveWithExtension):
        value = value.value

    if isinstance(value, str):
        # Try to parse as date or datetime
        if "T" in value or len(value) > 10:
            # Might be a datetime
            try:
                result = FHIRDateTime.parse(value)
                if result is not None:
                    return result
            except (ValueError, AttributeError):
                pass
        # Try as date (only if looks like a date pattern: YYYY or YYYY-MM or YYYY-MM-DD)
        if len(value) >= 4 and value[:4].isdigit():
            try:
                date_result = FHIRDate.parse(value)
                if date_result is not None:
                    return date_result
            except (ValueError, AttributeError):
                pass
    return value


def equals(left: Any, right: Any) -> bool | None:
    """
    FHIRPath equality comparison.

    Returns None if either operand is empty/null.
    Collections must be singletons for comparison - different sizes = False.
    """
    if left is None or right is None:
        return None

    # Handle lists
    if isinstance(left, list):
        if not left:
            return None
        if len(left) > 1:
            # Multi-element collection on left side
            if isinstance(right, list):
                if not right:
                    return None
                if len(right) != len(left):
                    return False
                # Compare element by element
                for l_item, r_item in zip(left, right):
                    if not _equals_single(l_item, r_item):
                        return False
                return True
            return False  # Can't compare multi-element with singleton
        left = left[0]

    if isinstance(right, list):
        if not right:
            return None
        if len(right) > 1:
            return False  # Can't compare singleton with multi-element
        right = right[0]

    return _equals_single(left, right)


def _equals_single(left: Any, right: Any) -> bool:
    """Compare two single values for equality."""
    # Normalize date strings to FHIRDate/FHIRDateTime
    left = _normalize_for_comparison(left)
    right = _normalize_for_comparison(right)

    # Type-specific comparison
    if type(left) is not type(right):
        # Different types are not equal (with some exceptions)
        # int, float, and Decimal can be compared
        if isinstance(left, (int, float, Decimal)) and isinstance(right, (int, float, Decimal)):
            return float(left) == float(right)
        return False

    return left == right


def equivalent(left: Any, right: Any) -> bool:
    """
    FHIRPath equivalence comparison (~).

    Empty collections are equivalent to empty collections.
    Comparison is case-insensitive for strings.
    """
    # Handle lists
    if isinstance(left, list):
        left = left[0] if len(left) == 1 else (None if not left else left)
    if isinstance(right, list):
        right = right[0] if len(right) == 1 else (None if not right else right)

    # Both empty/null are equivalent
    if left is None and right is None:
        return True
    if left is None or right is None:
        return False

    # String comparison is case-insensitive
    if isinstance(left, str) and isinstance(right, str):
        return left.lower() == right.lower()

    return left == right


def compare(left: Any, right: Any) -> int | None:
    """
    Compare two values.

    Returns:
        -1 if left < right
        0 if left == right
        1 if left > right
        None if not comparable
    """
    if left is None or right is None:
        return None

    # Handle lists (should be singletons)
    if isinstance(left, list):
        if not left:
            return None
        left = left[0]
    if isinstance(right, list):
        if not right:
            return None
        right = right[0]

    # Normalize date strings to FHIRDate/FHIRDateTime
    left = _normalize_for_comparison(left)
    right = _normalize_for_comparison(right)

    try:
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    except TypeError:
        return None


@FunctionRegistry.register("=")
def fn_equals(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Equality operator."""
    result = equals(left, right)
    if result is None:
        return []
    return [result]


@FunctionRegistry.register("!=")
def fn_not_equals(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Inequality operator."""
    result = equals(left, right)
    if result is None:
        return []
    return [not result]


@FunctionRegistry.register("~")
def fn_equivalent(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Equivalence operator."""
    return [equivalent(left, right)]


@FunctionRegistry.register("!~")
def fn_not_equivalent(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Not equivalent operator."""
    return [not equivalent(left, right)]


@FunctionRegistry.register("<")
def fn_less_than(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Less than operator."""
    result = compare(left, right)
    if result is None:
        return []
    return [result < 0]


@FunctionRegistry.register(">")
def fn_greater_than(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Greater than operator."""
    result = compare(left, right)
    if result is None:
        return []
    return [result > 0]


@FunctionRegistry.register("<=")
def fn_less_or_equal(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Less than or equal operator."""
    result = compare(left, right)
    if result is None:
        return []
    return [result <= 0]


@FunctionRegistry.register(">=")
def fn_greater_or_equal(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Greater than or equal operator."""
    result = compare(left, right)
    if result is None:
        return []
    return [result >= 0]


@FunctionRegistry.register("comparable")
def fn_comparable(ctx: EvaluationContext, collection: list[Any], other: Any) -> list[bool]:
    """
    Returns true if the quantities are comparable (have compatible units).

    This function checks if two Quantity values can be compared by determining
    if their units can be converted to a common unit.
    """
    if not collection:
        return []

    left = collection[0]
    if not isinstance(left, Quantity):
        return []

    # Handle list argument
    if isinstance(other, list):
        if not other:
            return []
        other = other[0]

    if not isinstance(other, Quantity):
        return []

    # Check if the quantities can be converted for comparison
    result = left._convert_for_comparison(other)
    return [result is not None]
