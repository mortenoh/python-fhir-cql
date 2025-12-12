"""CQL-specific types.

This module defines the CQL type system including:
- CQLCode: Represents a coded value with system, code, and display
- CQLConcept: A concept represented by multiple codes
- CQLInterval: An interval with low/high bounds (open or closed)
- CQLTuple: A structured type with named elements
- CQLRatio: A ratio of two quantities
"""

from decimal import Decimal
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, field_validator

from ..types import FHIRDate, FHIRDateTime, Quantity

T = TypeVar("T")


class CQLCode(BaseModel):
    """CQL Code type representing a coded value.

    A Code consists of:
    - code: The code value
    - system: The code system URI
    - display: Optional human-readable display name
    - version: Optional code system version
    """

    model_config = ConfigDict(frozen=True)

    code: str
    system: str
    display: str | None = None
    version: str | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CQLCode):
            # Equivalence in CQL compares code and system
            return self.code == other.code and self.system == other.system
        return False

    def __hash__(self) -> int:
        return hash((self.code, self.system))

    def __str__(self) -> str:
        if self.display:
            return f"Code '{self.code}' from {self.system} display '{self.display}'"
        return f"Code '{self.code}' from {self.system}"

    def equivalent(self, other: "CQLCode") -> bool:
        """CQL equivalence (~) - compares code and system only."""
        return self.code == other.code and self.system == other.system


class CQLConcept(BaseModel):
    """CQL Concept type representing a concept with multiple codes.

    A Concept consists of:
    - codes: One or more codes representing the concept
    - display: Optional human-readable display name
    """

    model_config = ConfigDict(frozen=True)

    codes: tuple[CQLCode, ...] = ()
    display: str | None = None

    @field_validator("codes", mode="before")
    @classmethod
    def convert_codes_to_tuple(cls, v: Any) -> tuple[CQLCode, ...]:
        if isinstance(v, list):
            return tuple(v)
        return v

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CQLConcept):
            return set(self.codes) == set(other.codes)
        return False

    def __hash__(self) -> int:
        return hash(self.codes)

    def __str__(self) -> str:
        codes_str = ", ".join(str(c) for c in self.codes)
        if self.display:
            return f"Concept {{ {codes_str} }} display '{self.display}'"
        return f"Concept {{ {codes_str} }}"


class CQLInterval(BaseModel, Generic[T]):
    """CQL Interval type representing a range of values.

    An Interval consists of:
    - low: The lower bound (or None for unbounded)
    - high: The upper bound (or None for unbounded)
    - low_closed: Whether the low bound is included (default True)
    - high_closed: Whether the high bound is included (default True)

    Supports intervals of Integer, Decimal, Date, DateTime, Time, and Quantity.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    low: Any | None = None
    high: Any | None = None
    low_closed: bool = True
    high_closed: bool = True

    def __contains__(self, value: Any) -> bool:
        """Check if value is in the interval (contains operator)."""
        if value is None:
            return False

        # Check low bound
        if self.low is not None:
            if self.low_closed:
                if value < self.low:
                    return False
            else:
                if value <= self.low:
                    return False

        # Check high bound
        if self.high is not None:
            if self.high_closed:
                if value > self.high:
                    return False
            else:
                if value >= self.high:
                    return False

        return True

    def contains(self, value: Any) -> bool:
        """CQL contains operator."""
        return value in self

    def includes(self, other: "CQLInterval[Any]") -> bool:
        """CQL includes operator - this interval includes other interval."""
        if other.low is not None:
            if other.low not in self:
                # Check if it's exactly at our boundary
                if self.low is not None:
                    if other.low < self.low:
                        return False
                    if other.low == self.low and not self.low_closed and other.low_closed:
                        return False

        if other.high is not None:
            if other.high not in self:
                if self.high is not None:
                    if other.high > self.high:
                        return False
                    if other.high == self.high and not self.high_closed and other.high_closed:
                        return False

        return True

    def overlaps(self, other: "CQLInterval[Any]") -> bool:
        """CQL overlaps operator - intervals have common points."""
        # Two intervals overlap if they share at least one point
        if self.high is not None and other.low is not None:
            if self.high < other.low:
                return False
            if self.high == other.low and not (self.high_closed and other.low_closed):
                return False

        if other.high is not None and self.low is not None:
            if other.high < self.low:
                return False
            if other.high == self.low and not (other.high_closed and self.low_closed):
                return False

        return True

    def meets(self, other: "CQLInterval[Any]") -> bool:
        """CQL meets operator - this interval ends where other begins."""
        if self.high is None or other.low is None:
            return False
        return self.high == other.low and self.high_closed != other.low_closed

    def meets_before(self, other: "CQLInterval[Any]") -> bool:
        """CQL meets before - this ends exactly where other starts."""
        return self.meets(other)

    def meets_after(self, other: "CQLInterval[Any]") -> bool:
        """CQL meets after - this starts exactly where other ends."""
        return other.meets(self)

    @property
    def is_empty(self) -> bool:
        """Check if interval is empty (low > high or equal with open bounds)."""
        if self.low is None or self.high is None:
            return False
        if self.low > self.high:
            return True
        if self.low == self.high and not (self.low_closed and self.high_closed):
            return True
        return False

    def width(self) -> Any | None:
        """Calculate the width of the interval."""
        if self.low is None or self.high is None:
            return None
        return self.high - self.low

    def start(self) -> Any | None:
        """Get the start (low) of the interval."""
        return self.low

    def end(self) -> Any | None:
        """Get the end (high) of the interval."""
        return self.high

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CQLInterval):
            return (
                self.low == other.low
                and self.high == other.high
                and self.low_closed == other.low_closed
                and self.high_closed == other.high_closed
            )
        return False

    def __hash__(self) -> int:
        # Make low and high hashable
        low_hash = hash(self.low) if self.low is not None else 0
        high_hash = hash(self.high) if self.high is not None else 0
        return hash((low_hash, high_hash, self.low_closed, self.high_closed))

    def __str__(self) -> str:
        low_bracket = "[" if self.low_closed else "("
        high_bracket = "]" if self.high_closed else ")"
        low_str = str(self.low) if self.low is not None else ""
        high_str = str(self.high) if self.high is not None else ""
        return f"Interval{low_bracket}{low_str}, {high_str}{high_bracket}"


class CQLTuple(BaseModel):
    """CQL Tuple type representing a structured value with named elements.

    A Tuple is essentially a dictionary with string keys and any values.
    Used for query results and structured data.
    """

    model_config = ConfigDict(extra="allow")

    elements: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name in ("elements", "model_fields", "model_config", "__dict__", "__pydantic_fields_set__"):
            return super().__getattribute__(name)
        try:
            elements = super().__getattribute__("elements")
            if name in elements:
                return elements[name]
        except AttributeError:
            pass
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        return self.elements.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.elements[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.elements

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CQLTuple):
            return self.elements == other.elements
        if isinstance(other, dict):
            return self.elements == other
        return False

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.elements.items())))

    def __str__(self) -> str:
        items = ", ".join(f"{k}: {v}" for k, v in self.elements.items())
        return f"Tuple {{ {items} }}"

    def keys(self) -> list[str]:
        """Get all element names."""
        return list(self.elements.keys())

    def values(self) -> list[Any]:
        """Get all element values."""
        return list(self.elements.values())

    def items(self) -> list[tuple[str, Any]]:
        """Get all (name, value) pairs."""
        return list(self.elements.items())


class CQLRatio(BaseModel):
    """CQL Ratio type representing a ratio of two quantities.

    A Ratio consists of:
    - numerator: The numerator quantity
    - denominator: The denominator quantity
    """

    model_config = ConfigDict(frozen=True)

    numerator: Quantity
    denominator: Quantity

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CQLRatio):
            # Ratios are equal if their decimal equivalents are equal
            # (when units are compatible)
            return self.numerator == other.numerator and self.denominator == other.denominator
        return False

    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))

    def __str__(self) -> str:
        return f"{self.numerator} : {self.denominator}"

    def to_decimal(self) -> Decimal | None:
        """Convert ratio to decimal value (if units cancel)."""
        if self.numerator.unit == self.denominator.unit:
            if self.denominator.value == 0:
                return None
            return self.numerator.value / self.denominator.value
        return None


# Type aliases for CQL
CQLBoolean = bool
CQLInteger = int
CQLDecimal = Decimal
CQLString = str
CQLDate = FHIRDate
CQLDateTime = FHIRDateTime
CQLQuantity = Quantity
CQLList = list


def is_cql_type(value: Any) -> bool:
    """Check if a value is a recognized CQL type."""
    return isinstance(
        value,
        (
            bool,
            int,
            float,
            Decimal,
            str,
            FHIRDate,
            FHIRDateTime,
            Quantity,
            CQLCode,
            CQLConcept,
            CQLInterval,
            CQLTuple,
            CQLRatio,
            list,
            type(None),
        ),
    )


def cql_type_name(value: Any) -> str:
    """Get the CQL type name for a value."""
    if value is None:
        return "Null"
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, Decimal | float):
        return "Decimal"
    if isinstance(value, str):
        return "String"
    if isinstance(value, FHIRDate):
        return "Date"
    if isinstance(value, FHIRDateTime):
        return "DateTime"
    if isinstance(value, Quantity):
        return "Quantity"
    if isinstance(value, CQLCode):
        return "Code"
    if isinstance(value, CQLConcept):
        return "Concept"
    if isinstance(value, CQLInterval):
        return "Interval"
    if isinstance(value, CQLTuple):
        return "Tuple"
    if isinstance(value, CQLRatio):
        return "Ratio"
    if isinstance(value, list):
        return "List"
    if isinstance(value, dict):
        return "Tuple"  # FHIR resources are treated as tuples
    return "Unknown"
