# FHIRPath Evaluator Implementation Plan

## Overview

The FHIRPath evaluator is designed as the **foundation for CQL evaluation**. CQL uses FHIRPath as its expression language and extends it with additional constructs.

```
┌──────────────────────────────────────────────────────────────┐
│                      CQL Evaluator                            │
│  - Library definitions      - Retrieve expressions [Type]    │
│  - Query expressions        - Terminology (valueset, code)   │
│  - Function definitions     - Interval operations            │
├──────────────────────────────────────────────────────────────┤
│                   FHIRPath Evaluator (Core)                   │
│  - Path navigation          - Collection functions           │
│  - Filtering (where)        - Type functions                 │
│  - Boolean/comparison ops   - String/math functions          │
│  - $this, $index, $total    - Date/time functions            │
├──────────────────────────────────────────────────────────────┤
│                      Shared Components                        │
│  - Type system              - Function registry              │
│  - Evaluation context       - Model info provider            │
└──────────────────────────────────────────────────────────────┘
```

## Architecture

### Core Components

```
src/fhir_cql/
├── engine/
│   ├── __init__.py
│   ├── types.py              # Shared type system
│   ├── context.py            # Evaluation context (extensible)
│   ├── functions.py          # Function registry (extensible)
│   ├── exceptions.py         # Shared exceptions
│   │
│   ├── fhirpath/
│   │   ├── __init__.py
│   │   ├── evaluator.py      # FHIRPathEvaluator class
│   │   ├── visitor.py        # ANTLR visitor implementation
│   │   └── functions/        # FHIRPath function implementations
│   │       ├── __init__.py
│   │       ├── existence.py  # exists, empty, count, all, any
│   │       ├── filtering.py  # where, select, repeat, ofType
│   │       ├── subsetting.py # first, last, tail, take, skip, single
│   │       ├── strings.py    # String manipulation
│   │       ├── math.py       # Math operations
│   │       ├── collections.py# union, intersect, exclude, distinct
│   │       ├── comparison.py # Equality, equivalence, ordering
│   │       ├── types.py      # is, as, type conversions
│   │       ├── datetime.py   # today, now, date components
│   │       └── utility.py    # iif, trace, etc.
│   │
│   └── cql/                  # (Future) CQL-specific extensions
│       ├── __init__.py
│       ├── evaluator.py      # CQLEvaluator (extends FHIRPath)
│       ├── visitor.py        # CQL ANTLR visitor
│       ├── library.py        # Library management
│       ├── retrieve.py       # [Type] retrieve handling
│       ├── query.py          # Query expression handling
│       └── functions/        # CQL-specific functions
│           ├── __init__.py
│           ├── clinical.py   # Age, AgeInYears, etc.
│           ├── interval.py   # Interval operations
│           └── terminology.py# ValueSet, Code operations
```

### Type System (`engine/types.py`)

Shared between FHIRPath and CQL:

```python
from enum import Enum
from dataclasses import dataclass
from typing import Any
from datetime import date, datetime, time
from decimal import Decimal

class FHIRPathType(Enum):
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
    value: Decimal
    unit: str

@dataclass
class FHIRPathResult:
    """Wrapper for FHIRPath evaluation results (always a collection)."""
    items: list[Any]

    def __bool__(self) -> bool:
        """Empty collection is falsy."""
        return len(self.items) > 0

    def single(self) -> Any:
        """Return single item or raise if not exactly one."""
        if len(self.items) != 1:
            raise FHIRPathError(f"Expected single item, got {len(self.items)}")
        return self.items[0]
```

### Evaluation Context (`engine/context.py`)

Extensible context for both FHIRPath and CQL:

```python
from typing import Any, Protocol, Callable

class ModelProvider(Protocol):
    """Protocol for FHIR model information (needed by CQL retrieve)."""
    def get_type_info(self, type_name: str) -> TypeInfo: ...
    def get_property_type(self, type_name: str, property: str) -> str: ...

class EvaluationContext:
    """Context for expression evaluation."""

    def __init__(
        self,
        resource: dict | None = None,
        root_resource: dict | None = None,
        model: ModelProvider | None = None,
    ):
        self.resource = resource          # %resource
        self.root_resource = root_resource # %rootResource
        self.model = model

        # Variable stack for $this, $index, $total
        self._variables: dict[str, Any] = {}

        # External constants (%name)
        self._constants: dict[str, Any] = {}

        # Function registry (extensible)
        self._functions: dict[str, Callable] = {}

    def with_this(self, value: Any) -> "EvaluationContext":
        """Create child context with $this bound."""
        ...

    def register_function(self, name: str, fn: Callable) -> None:
        """Register custom function (for CQL extensions)."""
        ...

    def get_function(self, name: str) -> Callable | None:
        """Get function by name."""
        ...


class CQLContext(EvaluationContext):
    """Extended context for CQL evaluation."""

    def __init__(self, ...):
        super().__init__(...)
        self.library: Library | None = None
        self.parameters: dict[str, Any] = {}
        self.patient: dict | None = None  # Patient context
        # ... CQL-specific context
```

### Function Registry (`engine/functions.py`)

Allows CQL to extend FHIRPath functions:

```python
from typing import Callable, Any

class FunctionRegistry:
    """Registry for FHIRPath/CQL functions."""

    _functions: dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """Decorator to register a function."""
        def decorator(fn: Callable) -> Callable:
            cls._functions[name] = fn
            return fn
        return decorator

    @classmethod
    def get(cls, name: str) -> Callable | None:
        return cls._functions.get(name)

    @classmethod
    def call(cls, name: str, ctx: EvaluationContext, *args) -> Any:
        fn = cls.get(name)
        if fn is None:
            raise FHIRPathError(f"Unknown function: {name}")
        return fn(ctx, *args)


# FHIRPath functions register themselves
@FunctionRegistry.register("exists")
def fn_exists(ctx: EvaluationContext, collection: list) -> bool:
    return len(collection) > 0

@FunctionRegistry.register("count")
def fn_count(ctx: EvaluationContext, collection: list) -> int:
    return len(collection)

# CQL can add its own functions
@FunctionRegistry.register("AgeInYears")
def fn_age_in_years(ctx: CQLContext) -> int:
    # CQL-specific implementation
    ...
```

### FHIRPath Evaluator (`engine/fhirpath/evaluator.py`)

```python
class FHIRPathEvaluator:
    """Evaluate FHIRPath expressions against FHIR data."""

    def __init__(self, context: EvaluationContext | None = None):
        self.context = context or EvaluationContext()

    def evaluate(
        self,
        expression: str,
        resource: dict | None = None
    ) -> list[Any]:
        """
        Evaluate a FHIRPath expression.

        Args:
            expression: FHIRPath expression string
            resource: FHIR resource (JSON dict) to evaluate against

        Returns:
            List of results (FHIRPath always returns collections)
        """
        # Parse expression
        tree = parse_fhirpath(expression)

        # Create visitor with context
        ctx = self.context
        if resource:
            ctx = EvaluationContext(resource=resource, root_resource=resource)

        visitor = FHIRPathVisitor(ctx)
        return visitor.visit(tree)
```

## Implementation Phases

### Phase 1: Core Infrastructure
- [ ] Type system (`engine/types.py`)
- [ ] Evaluation context (`engine/context.py`)
- [ ] Function registry (`engine/functions.py`)
- [ ] Basic evaluator structure
- [ ] Path navigation (property access)
- [ ] Collection handling
- [ ] Indexer access `[n]`

### Phase 2: Basic Functions
- [ ] `exists()`, `empty()`, `count()`
- [ ] `first()`, `last()`, `tail()`, `take(n)`, `skip(n)`, `single()`
- [ ] `where(criteria)`
- [ ] `$this` variable

### Phase 3: Operators
- [ ] Comparison: `=`, `!=`, `<`, `>`, `<=`, `>=`
- [ ] Equivalence: `~`, `!~`
- [ ] Boolean: `and`, `or`, `not`, `xor`, `implies`
- [ ] Math: `+`, `-`, `*`, `/`, `div`, `mod`
- [ ] String concatenation: `&`
- [ ] Union: `|`

### Phase 4: String Functions
- [ ] `startsWith()`, `endsWith()`, `contains()`, `matches()`
- [ ] `replace()`, `substring()`, `length()`
- [ ] `upper()`, `lower()`, `trim()`
- [ ] `split()`, `join()`, `indexOf()`

### Phase 5: Collection Functions
- [ ] `distinct()`, `isDistinct()`
- [ ] `select(projection)`
- [ ] `repeat(expression)`
- [ ] `all(criteria)`, `any()`
- [ ] `union()`, `intersect()`, `exclude()`, `combine()`
- [ ] `flatten()`
- [ ] `orderBy()`
- [ ] `aggregate()`

### Phase 6: Type Functions
- [ ] `is(type)`, `as(type)`, `ofType(type)`
- [ ] Conversions: `toBoolean()`, `toInteger()`, `toDecimal()`, `toString()`
- [ ] `toDate()`, `toDateTime()`, `toTime()`, `toQuantity()`
- [ ] `convertsTo*()` functions

### Phase 7: Date/Time
- [ ] `today()`, `now()`, `timeOfDay()`
- [ ] Date component access
- [ ] Date arithmetic

### Phase 8: Utility Functions
- [ ] `iif(condition, true, false)`
- [ ] `trace(name)`
- [ ] `%resource`, `%rootResource`, `%context`
- [ ] `$index`, `$total`

### Phase 9: FHIR-Specific
- [ ] `resolve()` - Reference resolution
- [ ] `extension(url)`
- [ ] `hasValue()`, `getValue()`
- [ ] Polymorphic paths (`value[x]`)

### Phase 10: CQL Foundation (Future)
- [ ] Interval type and operations
- [ ] List operations (CQL-specific)
- [ ] Terminology functions
- [ ] Clinical functions (`Age`, `AgeInYears`, etc.)

## CLI Integration

```bash
# Evaluate FHIRPath against FHIR JSON
fhirpath eval "Patient.name.given" examples/fhir/patient.json

# With expression from file
fhirpath eval -f expression.fhirpath examples/fhir/patient.json

# Output as JSON
fhirpath eval "Patient.name.given" examples/fhir/patient.json --json

# Interactive REPL with loaded resource
fhirpath repl --resource examples/fhir/patient.json
```

## Testing Strategy

1. **Unit tests** per function/operator
2. **Integration tests** against example FHIR resources
3. **FHIRPath test suite** from HL7:
   - https://github.com/HL7/FHIRPath/tree/master/tests
4. **CQL test suite** (when CQL evaluator is built):
   - https://github.com/cqframework/clinical_quality_language/tree/master/Src/java/cql-to-elm/src/test

## References

- [FHIRPath N1 Specification](http://hl7.org/fhirpath/N1/)
- [FHIR FHIRPath](https://www.hl7.org/fhir/fhirpath.html)
- [CQL Specification](https://cql.hl7.org/)
- [CQL-to-ELM](https://cql.hl7.org/elm.html)
