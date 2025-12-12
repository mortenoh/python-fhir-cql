"""Type system shared between FHIRPath and CQL."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any


class FHIRPathType(Enum):
    """FHIRPath primitive types."""

    BOOLEAN = "Boolean"
    STRING = "String"
    INTEGER = "Integer"
    DECIMAL = "Decimal"
    DATE = "Date"
    DATETIME = "DateTime"
    TIME = "Time"
    QUANTITY = "Quantity"

    # Complex types
    RESOURCE = "Resource"
    ELEMENT = "Element"

    # Special
    NULL = "Null"


@dataclass
class Quantity:
    """FHIRPath Quantity type with value and unit."""

    value: Decimal
    unit: str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Quantity):
            return self.value == other.value and self.unit == other.unit
        return False

    def __str__(self) -> str:
        return f"{self.value} '{self.unit}'"


def get_fhirpath_type(value: Any) -> FHIRPathType:
    """Determine the FHIRPath type of a Python value."""
    if value is None:
        return FHIRPathType.NULL
    if isinstance(value, bool):
        return FHIRPathType.BOOLEAN
    if isinstance(value, int):
        return FHIRPathType.INTEGER
    if isinstance(value, float | Decimal):
        return FHIRPathType.DECIMAL
    if isinstance(value, str):
        # Could be String, Date, DateTime, or Time based on format
        # For now, treat as String (parsing happens elsewhere)
        return FHIRPathType.STRING
    if isinstance(value, Quantity):
        return FHIRPathType.QUANTITY
    if isinstance(value, dict):
        if "resourceType" in value:
            return FHIRPathType.RESOURCE
        return FHIRPathType.ELEMENT
    return FHIRPathType.ELEMENT


def is_truthy(value: Any) -> bool:
    """
    Determine if a FHIRPath value is truthy.

    FHIRPath truthiness:
    - Empty collection: false
    - Single boolean: its value
    - Single non-boolean: true
    - Multiple items: error (but we return true for simplicity)
    """
    if value is None:
        return False
    if isinstance(value, list):
        if len(value) == 0:
            return False
        if len(value) == 1:
            return is_truthy(value[0])
        return True  # Non-empty collection with multiple items
    if isinstance(value, bool):
        return value
    return True  # Non-boolean singleton is truthy


def to_collection(value: Any) -> list[Any]:
    """Ensure a value is a collection (list)."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def singleton(collection: list[Any]) -> Any:
    """
    Get singleton value from collection.

    Returns None if empty, the single value if one item,
    or the list itself if multiple items.
    """
    if not collection:
        return None
    if len(collection) == 1:
        return collection[0]
    return collection
