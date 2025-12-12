# CQL Python API

This document describes the Python API for evaluating CQL (Clinical Quality Language) expressions and libraries.

## Quick Start

```python
from fhir_cql.engine.cql import CQLEvaluator

# Create evaluator
evaluator = CQLEvaluator()

# Evaluate a simple expression
result = evaluator.evaluate_expression("1 + 2 * 3")
print(result)  # 7

# Compile and run a library
lib = evaluator.compile("""
    library Example version '1.0'
    define Sum: 1 + 2 + 3
    define Greeting: 'Hello, CQL!'
""")

# Evaluate definitions
sum_result = evaluator.evaluate_definition("Sum")  # 6
greeting = evaluator.evaluate_definition("Greeting")  # 'Hello, CQL!'
```

## CQLEvaluator

The main class for CQL evaluation.

### Constructor

```python
from fhir_cql.engine.cql import CQLEvaluator

evaluator = CQLEvaluator(
    data_source=None,       # Optional DataSource for retrieve operations
    library_manager=None    # Optional LibraryManager for library dependencies
)
```

### Methods

#### compile(source: str) -> CQLLibrary

Compile CQL source code into a library.

```python
lib = evaluator.compile("""
    library MyLibrary version '1.0'
    using FHIR version '4.0.1'

    define Sum: 1 + 2 + 3
    define Product: 4 * 5
""")

print(lib.name)     # 'MyLibrary'
print(lib.version)  # '1.0'
```

#### evaluate_expression(expression, resource=None, parameters=None) -> Any

Evaluate a CQL expression directly.

```python
# Simple expression
result = evaluator.evaluate_expression("1 + 2 * 3")

# With patient resource
patient = {"resourceType": "Patient", "birthDate": "1990-05-15"}
result = evaluator.evaluate_expression(
    "years between @1990-05-15 and Today()",
    resource=patient
)

# With parameters
result = evaluator.evaluate_expression(
    "X + Y",
    parameters={"X": 10, "Y": 20}
)
```

#### evaluate_definition(name, resource=None, parameters=None, library=None) -> Any

Evaluate a named definition from a library.

```python
# Compile library first
lib = evaluator.compile("""
    library Test
    define Sum: 1 + 2 + 3
    define Double: Sum * 2
""")

# Evaluate specific definition
result = evaluator.evaluate_definition("Sum")  # 6
result = evaluator.evaluate_definition("Double")  # 12

# With patient context
patient = {"resourceType": "Patient", "birthDate": "1990-05-15"}
result = evaluator.evaluate_definition("PatientAge", resource=patient)
```

#### evaluate_all_definitions(resource=None, parameters=None, library=None) -> dict

Evaluate all definitions in a library.

```python
lib = evaluator.compile("""
    library Test
    define A: 1
    define B: 2
    define C: A + B
""")

results = evaluator.evaluate_all_definitions()
# {'A': 1, 'B': 2, 'C': 3}
```

#### load_library(name, version=None) -> CQLLibrary

Load a previously compiled library.

```python
# After compiling
evaluator.compile("library MyLib ...")

# Later load by name
lib = evaluator.load_library("MyLib")
```

#### get_definitions(library=None) -> list[str]

Get list of definition names.

```python
lib = evaluator.compile("""
    library Test
    define A: 1
    define B: 2
""")

names = evaluator.get_definitions()  # ['A', 'B']
```

#### get_parameters(library=None) -> dict

Get parameter definitions and defaults.

```python
lib = evaluator.compile("""
    library Test
    parameter X Integer default 10
    parameter Y String
""")

params = evaluator.get_parameters()
# {'X': 10, 'Y': None}
```

## CQLLibrary

Represents a compiled CQL library.

### Properties

```python
lib.name           # Library name
lib.version        # Library version
lib.using          # List of UsingDefinition
lib.includes       # List of IncludeDefinition
lib.codesystems    # Dict of CodeSystemDefinition
lib.valuesets      # Dict of ValueSetDefinition
lib.codes          # Dict of CodeDefinition
lib.concepts       # Dict of ConceptDefinition
lib.parameters     # Dict of ParameterDefinition
lib.definitions    # Dict of ExpressionDefinition
lib.functions      # Dict of FunctionDefinition
lib.contexts       # List of context names
```

### Methods

```python
# Get a specific definition
defn = lib.get_definition("Sum")

# Get a function
func = lib.get_function("MyFunc")

# Resolve a code reference
code = lib.resolve_code("DiabetesCode")
```

## Convenience Functions

### compile_library(source) -> CQLLibrary

Quick way to compile a library.

```python
from fhir_cql.engine.cql import compile_library

lib = compile_library("""
    library Test
    define Sum: 1 + 2 + 3
""")
```

### evaluate(expression, resource=None) -> Any

Quick way to evaluate an expression.

```python
from fhir_cql.engine.cql import evaluate

result = evaluate("1 + 2 * 3")  # 7
result = evaluate("Today()")    # Current date
```

## Working with Patient Data

### Basic Patient Context

```python
evaluator = CQLEvaluator()

lib = evaluator.compile("""
    library PatientLib version '1.0'
    using FHIR version '4.0.1'

    context Patient

    define PatientAge:
        years between Patient.birthDate and Today()

    define IsAdult:
        PatientAge >= 18

    define PatientGender:
        Patient.gender
""")

patient = {
    "resourceType": "Patient",
    "birthDate": "1990-05-15",
    "gender": "male",
    "name": [{"family": "Smith", "given": ["John"]}]
}

age = evaluator.evaluate_definition("PatientAge", resource=patient)
is_adult = evaluator.evaluate_definition("IsAdult", resource=patient)
gender = evaluator.evaluate_definition("PatientGender", resource=patient)
```

### With Parameters

```python
lib = evaluator.compile("""
    library MeasureLib

    parameter "Measurement Period" Interval<DateTime>
    parameter "Age Threshold" Integer default 18

    define IsAdultInPeriod:
        PatientAge >= "Age Threshold"
""")

from datetime import datetime

params = {
    "Measurement Period": {
        "low": datetime(2024, 1, 1),
        "high": datetime(2024, 12, 31)
    },
    "Age Threshold": 21
}

result = evaluator.evaluate_definition(
    "IsAdultInPeriod",
    resource=patient,
    parameters=params
)
```

## CQL Types

### Intervals

```python
from fhir_cql.engine.cql.types import CQLInterval

# Create interval
interval = CQLInterval(low=1, high=10, low_closed=True, high_closed=True)

# Evaluate interval expressions
result = evaluator.evaluate_expression("Interval[1, 10] contains 5")  # True
result = evaluator.evaluate_expression("5 in Interval[1, 10]")  # True
```

### Tuples

```python
from fhir_cql.engine.cql.types import CQLTuple

# Evaluate tuple expression
result = evaluator.evaluate_expression("""
    Tuple { name: 'John', age: 30, active: true }
""")
# CQLTuple with elements {'name': 'John', 'age': 30, 'active': True}

# Access elements
print(result.elements['name'])  # 'John'
```

### Codes and Concepts

```python
from fhir_cql.engine.cql.types import CQLCode, CQLConcept

# In CQL
lib = evaluator.compile("""
    library TermLib

    codesystem "LOINC": 'http://loinc.org'
    code "Glucose": '2339-0' from "LOINC"

    define GlucoseCode: "Glucose"
""")

result = evaluator.evaluate_definition("GlucoseCode")
# CQLCode(code='2339-0', system='http://loinc.org', display=None)
```

### Quantities

```python
# Evaluate quantity expressions
result = evaluator.evaluate_expression("100 'mg'")
# Quantity(value=100, unit='mg')

result = evaluator.evaluate_expression("70 'kg' + 5 'kg'")
# Quantity(value=75, unit='kg')
```

## User-Defined Functions

```python
lib = evaluator.compile("""
    library FuncLib

    // Simple function
    define function Add(a Integer, b Integer) returns Integer:
        a + b

    // Function with null handling
    define function SafeDivide(num Decimal, denom Decimal) returns Decimal:
        if denom is null or denom = 0 then null
        else num / denom

    // Recursive function
    define function Factorial(n Integer) returns Integer:
        if n <= 1 then 1
        else n * Factorial(n - 1)

    // Using functions
    define Sum: Add(5, 3)
    define Division: SafeDivide(10.0, 2.0)
    define Fact5: Factorial(5)
""")

results = evaluator.evaluate_all_definitions()
# {'Sum': 8, 'Division': 5.0, 'Fact5': 120}
```

## Error Handling

```python
from fhir_cql.engine.exceptions import CQLError

try:
    evaluator.compile("invalid cql syntax !!!")
except CQLError as e:
    print(f"Compilation error: {e}")

try:
    evaluator.evaluate_definition("NonExistent")
except CQLError as e:
    print(f"Evaluation error: {e}")
```

## Complete Example

```python
from fhir_cql.engine.cql import CQLEvaluator
import json

# Load patient data
with open("patient.json") as f:
    patient = json.load(f)

# Create evaluator
evaluator = CQLEvaluator()

# Compile clinical logic
lib = evaluator.compile("""
    library DiabetesRisk version '1.0'
    using FHIR version '4.0.1'

    context Patient

    // Patient demographics
    define PatientAge:
        years between Patient.birthDate and Today()

    define IsFemale:
        Patient.gender = 'female'

    // Risk factors
    define HasDiabetesRiskFactors:
        PatientAge >= 45

    // BMI calculation helper
    define function CalculateBMI(weightKg Decimal, heightCm Decimal) returns Decimal:
        if weightKg is null or heightCm is null or heightCm = 0 then null
        else Round(weightKg / Power(heightCm / 100, 2), 1)

    // Age categories
    define AgeCategory:
        case
            when PatientAge < 18 then 'Pediatric'
            when PatientAge < 65 then 'Adult'
            else 'Geriatric'
        end
""")

# Evaluate all definitions
results = evaluator.evaluate_all_definitions(resource=patient)

print("Patient Analysis:")
for name, value in results.items():
    print(f"  {name}: {value}")
```

## FHIR Data Sources

CQL evaluation can query FHIR resources using data sources. Three implementations are provided:

### InMemoryDataSource

Store resources in memory for testing and simple use cases:

```python
from fhir_cql.engine.cql import CQLEvaluator, InMemoryDataSource

# Create data source and add resources
ds = InMemoryDataSource()
ds.add_resource({"resourceType": "Patient", "id": "p1", "birthDate": "1990-01-01"})
ds.add_resources([
    {
        "resourceType": "Condition",
        "id": "c1",
        "subject": {"reference": "Patient/p1"},
        "code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006"}]},
    },
    {
        "resourceType": "Observation",
        "id": "o1",
        "subject": {"reference": "Patient/p1"},
        "code": {"coding": [{"system": "http://loinc.org", "code": "2339-0"}]},
    },
])

# Create evaluator with data source
evaluator = CQLEvaluator(data_source=ds)

lib = evaluator.compile("""
    library Example
    using FHIR version '4.0.1'
    context Patient

    define Conditions: [Condition]
    define Observations: [Observation]
""")

patient = {"resourceType": "Patient", "id": "p1"}
conditions = evaluator.evaluate_definition("Conditions", resource=patient)
# Returns: [{"resourceType": "Condition", ...}]
```

### BundleDataSource

Load resources from a FHIR Bundle:

```python
from fhir_cql.engine.cql import CQLEvaluator, BundleDataSource

bundle = {
    "resourceType": "Bundle",
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "p1", "birthDate": "1990-01-01"}},
        {"resource": {
            "resourceType": "Condition",
            "id": "c1",
            "subject": {"reference": "Patient/p1"},
            "code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006"}]},
        }},
    ],
}

ds = BundleDataSource(bundle)
evaluator = CQLEvaluator(data_source=ds)

# Compile and evaluate...
```

### PatientBundleDataSource

For patient-centric bundles, automatically filters to the patient:

```python
from fhir_cql.engine.cql import CQLEvaluator, PatientBundleDataSource

# Load patient bundle (e.g., from a FHIR server)
with open("patient_bundle.json") as f:
    bundle = json.load(f)

ds = PatientBundleDataSource(bundle)
evaluator = CQLEvaluator(data_source=ds)

# The patient is automatically extracted
patient = ds.patient  # {"resourceType": "Patient", ...}

# Retrieve operations are automatically scoped to this patient
conditions = evaluator.evaluate_definition("Conditions", resource=patient)
```

### Retrieve Operations

CQL retrieve syntax queries the data source:

```cql
library Example
using FHIR version '4.0.1'

context Patient

// Simple retrieve - all resources of type
define AllConditions: [Condition]

// Retrieve with code filter
codesystem "SNOMED": 'http://snomed.info/sct'
valueset "Diabetes": 'http://example.org/vs/diabetes'

define DiabetesConditions: [Condition: code in "Diabetes"]

// Retrieve uses patient context automatically
define PatientObservations: [Observation]  // Filtered to current patient
```

### Adding ValueSets

For code filtering with valuesets:

```python
from fhir_cql.engine.cql import CQLCode, InMemoryDataSource

ds = InMemoryDataSource()

# Add expanded valueset
ds.add_valueset(
    "http://example.org/vs/diabetes",
    [
        CQLCode(code="44054006", system="http://snomed.info/sct"),
        CQLCode(code="E11", system="http://hl7.org/fhir/sid/icd-10"),
    ],
)

# Now [Condition: code in "Diabetes"] will filter appropriately
```

## Integration Patterns

### With FastAPI

```python
from fastapi import FastAPI
from fhir_cql.engine.cql import CQLEvaluator

app = FastAPI()
evaluator = CQLEvaluator()

@app.post("/evaluate")
async def evaluate_cql(expression: str, patient: dict = None):
    result = evaluator.evaluate_expression(expression, resource=patient)
    return {"result": result}

@app.post("/library/compile")
async def compile_library(source: str):
    lib = evaluator.compile(source)
    return {"name": lib.name, "definitions": list(lib.definitions.keys())}
```

### With Pandas

```python
import pandas as pd
from fhir_cql.engine.cql import CQLEvaluator

evaluator = CQLEvaluator()
lib = evaluator.compile("""
    library Analysis
    context Patient
    define PatientAge: years between Patient.birthDate and Today()
""")

# Process multiple patients
patients = [
    {"resourceType": "Patient", "id": "1", "birthDate": "1990-01-01"},
    {"resourceType": "Patient", "id": "2", "birthDate": "1985-06-15"},
    {"resourceType": "Patient", "id": "3", "birthDate": "2000-03-22"},
]

results = []
for patient in patients:
    age = evaluator.evaluate_definition("PatientAge", resource=patient)
    results.append({"id": patient["id"], "age": age})

df = pd.DataFrame(results)
print(df)
```
