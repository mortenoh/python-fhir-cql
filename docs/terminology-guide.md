# Terminology Service Guide

A comprehensive guide to the FHIR terminology service for code validation and ValueSet operations.

## What is the Terminology Service?

The terminology service provides operations for working with medical codes and value sets:

- **Code Validation**: Check if a code is valid within a ValueSet
- **Membership Testing**: Verify code membership in value sets
- **Subsumption Testing**: Check hierarchical relationships between codes
- **ValueSet Expansion**: List all codes in a ValueSet

### Key Concepts

| Term | Description |
|------|-------------|
| **Code System** | A collection of codes (e.g., SNOMED CT, LOINC, ICD-10) |
| **ValueSet** | A selection of codes from one or more code systems |
| **Coding** | A single code with its system and display text |
| **CodeableConcept** | Multiple codings representing the same concept |

### Use Cases

- **Data Validation**: Ensure clinical data uses valid codes
- **CQL Evaluation**: Support terminology operations in CQL expressions
- **FHIR Validation**: Validate FHIR resources against terminology bindings
- **Data Quality**: Check code membership and relationships

---

## Quick Start

### Start Terminology Server

```bash
# Start with local ValueSets
fhir terminology serve --valuesets ./terminology

# Output:
# Terminology Service
#   Loading ValueSets from ./terminology...
#   Loaded 5 ValueSets
#
# Starting server on http://0.0.0.0:8080
#   Docs: http://0.0.0.0:8080/docs
```

### Validate a Code

```bash
# CLI validation
fhir terminology validate 44054006 \
  --system http://snomed.info/sct \
  --valueset http://example.com/vs/diabetes-conditions \
  --dir ./terminology

# Output:
# Code Validation Result
#   Code:     44054006
#   System:   http://snomed.info/sct
#   ValueSet: http://example.com/vs/diabetes-conditions
#   Result:   VALID
```

### REST API

```bash
# Validate via REST API
curl "http://localhost:8080/ValueSet/\$validate-code?url=http://example.com/vs/diabetes-conditions&code=44054006&system=http://snomed.info/sct"

# Response:
# {
#   "resourceType": "Parameters",
#   "parameter": [
#     {"name": "result", "valueBoolean": true},
#     {"name": "display", "valueString": "Diabetes mellitus"}
#   ]
# }
```

---

## CLI Reference

### fhir terminology serve

Start the terminology service server.

```bash
fhir terminology serve [OPTIONS]
```

#### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--host` | `-h` | `0.0.0.0` | Host to bind to |
| `--port` | `-p` | `8080` | Port to listen on |
| `--valuesets` | `-v` | None | Directory containing ValueSet JSON files |
| `--reload` | `-r` | `False` | Enable auto-reload for development |
| `--log-level` | `-l` | `INFO` | Logging level |

#### Examples

```bash
# Start with local ValueSets
fhir terminology serve --valuesets ./terminology

# Custom port
fhir terminology serve --valuesets ./terminology --port 9000

# Development mode
fhir terminology serve --valuesets ./terminology --reload
```

### fhir terminology validate

Validate a code against a ValueSet.

```bash
fhir terminology validate CODE [OPTIONS]
```

#### Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--system` | `-s` | Yes | Code system URL |
| `--valueset` | `-v` | Yes | ValueSet URL |
| `--dir` | `-d` | No | Directory containing ValueSet JSON files |
| `--server` | | No | Terminology server URL |

#### Examples

```bash
# Validate against local ValueSets
fhir terminology validate 44054006 \
  --system http://snomed.info/sct \
  --valueset http://example.com/vs/conditions \
  --dir ./terminology

# Validate against remote server
fhir terminology validate 8480-6 \
  --system http://loinc.org \
  --valueset http://hl7.org/fhir/ValueSet/observation-vitalsignresult \
  --server http://terminology.example.com
```

### fhir terminology member-of

Check if a code is a member of a ValueSet.

```bash
fhir terminology member-of CODE [OPTIONS]
```

#### Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--system` | `-s` | Yes | Code system URL |
| `--valueset` | `-v` | Yes | ValueSet URL |
| `--dir` | `-d` | No | Directory containing ValueSet JSON files |

#### Example

```bash
fhir terminology member-of 8480-6 \
  --system http://loinc.org \
  --valueset http://example.com/vs/vital-signs \
  --dir ./terminology
```

### fhir terminology list-valuesets

List ValueSets in a directory.

```bash
fhir terminology list-valuesets DIRECTORY
```

#### Example

```bash
fhir terminology list-valuesets ./terminology

# Output:
# ValueSets in ./terminology
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
# ┃ URL                                        ┃ Name               ┃ Codes  ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
# │ http://example.com/vs/diabetes-conditions  │ DiabetesConditions │     15 │
# │ http://example.com/vs/vital-signs          │ VitalSigns         │      7 │
# │ http://example.com/vs/lab-results          │ LabResults         │     23 │
# └────────────────────────────────────────────┴────────────────────┴────────┘
```

---

## REST API Reference

### ValueSet $validate-code

Validate that a code is in a ValueSet.

```http
GET /ValueSet/$validate-code?url={valueSetUrl}&code={code}&system={system}
POST /ValueSet/$validate-code
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | uri | Yes | ValueSet canonical URL |
| `code` | string | Yes* | Code to validate |
| `system` | uri | No | Code system URL |
| `display` | string | No | Expected display text |
| `coding` | Coding | Yes* | Coding to validate |
| `codeableConcept` | CodeableConcept | Yes* | CodeableConcept to validate |

*One of code, coding, or codeableConcept is required.

#### GET Example

```bash
curl "http://localhost:8080/ValueSet/\$validate-code?url=http://example.com/vs/conditions&code=44054006&system=http://snomed.info/sct"
```

#### POST Example

```bash
curl -X POST http://localhost:8080/ValueSet/\$validate-code \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Parameters",
    "parameter": [
      {"name": "url", "valueUri": "http://example.com/vs/conditions"},
      {"name": "code", "valueCode": "44054006"},
      {"name": "system", "valueUri": "http://snomed.info/sct"}
    ]
  }'
```

#### Response

```json
{
  "resourceType": "Parameters",
  "parameter": [
    {"name": "result", "valueBoolean": true},
    {"name": "display", "valueString": "Diabetes mellitus"}
  ]
}
```

### CodeSystem $lookup

Look up information about a code.

```http
GET /CodeSystem/$lookup?system={systemUrl}&code={code}
POST /CodeSystem/$lookup
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `system` | uri | Yes | Code system URL |
| `code` | string | Yes | Code to look up |
| `version` | string | No | Code system version |

#### Example

```bash
curl "http://localhost:8080/CodeSystem/\$lookup?system=http://snomed.info/sct&code=44054006"
```

#### Response

```json
{
  "resourceType": "Parameters",
  "parameter": [
    {"name": "name", "valueString": "SNOMED CT"},
    {"name": "display", "valueString": "Diabetes mellitus"},
    {"name": "code", "valueCode": "44054006"},
    {"name": "system", "valueUri": "http://snomed.info/sct"}
  ]
}
```

### CodeSystem $subsumes

Check if one code subsumes another.

```http
GET /CodeSystem/$subsumes?system={systemUrl}&codeA={codeA}&codeB={codeB}
POST /CodeSystem/$subsumes
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `system` | uri | Yes | Code system URL |
| `codeA` | string | Yes | First code |
| `codeB` | string | Yes | Second code |
| `version` | string | No | Code system version |

#### Response Outcomes

| Outcome | Meaning |
|---------|---------|
| `equivalent` | Codes are equivalent |
| `subsumes` | Code A subsumes Code B |
| `subsumed-by` | Code A is subsumed by Code B |
| `not-subsumed` | No subsumption relationship |

---

## ValueSet Format

### Basic Structure

```json
{
  "resourceType": "ValueSet",
  "id": "diabetes-conditions",
  "url": "http://example.com/vs/diabetes-conditions",
  "version": "1.0.0",
  "name": "DiabetesConditions",
  "title": "Diabetes-Related Conditions",
  "status": "active",
  "compose": {
    "include": [
      {
        "system": "http://snomed.info/sct",
        "concept": [
          {"code": "44054006", "display": "Diabetes mellitus"},
          {"code": "46635009", "display": "Type 1 diabetes"},
          {"code": "44054006", "display": "Type 2 diabetes"}
        ]
      }
    ]
  }
}
```

### Multiple Code Systems

```json
{
  "resourceType": "ValueSet",
  "url": "http://example.com/vs/lab-results",
  "compose": {
    "include": [
      {
        "system": "http://loinc.org",
        "concept": [
          {"code": "2345-7", "display": "Glucose"},
          {"code": "4548-4", "display": "HbA1c"}
        ]
      },
      {
        "system": "http://snomed.info/sct",
        "concept": [
          {"code": "33747003", "display": "Glucose measurement"}
        ]
      }
    ]
  }
}
```

### With Expansion

```json
{
  "resourceType": "ValueSet",
  "url": "http://example.com/vs/vital-signs",
  "expansion": {
    "identifier": "urn:uuid:abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "total": 7,
    "contains": [
      {"system": "http://loinc.org", "code": "8310-5", "display": "Body temperature"},
      {"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"},
      {"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}
    ]
  }
}
```

---

## Python API

### TerminologyService Base Class

```python
from fhir_cql.terminology import (
    TerminologyService,
    InMemoryTerminologyService,
    FHIRTerminologyService,
)

# Abstract base class defines the interface
class TerminologyService(ABC):
    def validate_code(self, request: ValidateCodeRequest) -> ValidateCodeResponse: ...
    def member_of(self, request: MemberOfRequest) -> MemberOfResponse: ...
    def subsumes(self, request: SubsumesRequest) -> SubsumesResponse: ...
    def get_value_set(self, url: str, version: str | None = None) -> ValueSet | None: ...
```

### InMemoryTerminologyService

For testing and development without external dependencies.

```python
from fhir_cql.terminology import InMemoryTerminologyService
from fhir_cql.terminology.models import (
    ValidateCodeRequest,
    MemberOfRequest,
    ValueSet,
)

# Create service
service = InMemoryTerminologyService()

# Load ValueSets from directory
count = service.load_value_sets_from_directory("./terminology")
print(f"Loaded {count} ValueSets")

# Load individual ValueSet
service.load_value_set_file("./diabetes-codes.json")

# Load from JSON data
service.add_value_set_from_json({
    "resourceType": "ValueSet",
    "url": "http://example.com/vs/test",
    "compose": {
        "include": [{
            "system": "http://example.com/cs",
            "concept": [{"code": "123", "display": "Test"}]
        }]
    }
})

# Validate code
request = ValidateCodeRequest(
    url="http://example.com/vs/diabetes-conditions",
    code="44054006",
    system="http://snomed.info/sct"
)
response = service.validate_code(request)

if response.result:
    print(f"Valid! Display: {response.display}")
else:
    print(f"Invalid: {response.message}")

# Check membership
member_request = MemberOfRequest(
    code="44054006",
    system="http://snomed.info/sct",
    valueSetUrl="http://example.com/vs/diabetes-conditions"
)
member_response = service.member_of(member_request)
print(f"Is member: {member_response.result}")

# Get ValueSet
value_set = service.get_value_set("http://example.com/vs/diabetes-conditions")
if value_set:
    print(f"ValueSet: {value_set.name}")
```

### FHIRTerminologyService

Delegates to an external FHIR terminology server.

```python
from fhir_cql.terminology import FHIRTerminologyService
from fhir_cql.terminology.models import ValidateCodeRequest

# Create service pointing to external server
service = FHIRTerminologyService(
    base_url="http://terminology.example.com/fhir",
    headers={"Authorization": "Bearer token123"}
)

# Operations are proxied to the FHIR server
request = ValidateCodeRequest(
    url="http://hl7.org/fhir/ValueSet/observation-codes",
    code="8480-6",
    system="http://loinc.org"
)
response = service.validate_code(request)
```

### Models

```python
from fhir_cql.terminology.models import (
    Coding,
    CodeableConcept,
    ValueSet,
    ValueSetCompose,
    ValueSetComposeInclude,
    ValueSetExpansion,
    ValidateCodeRequest,
    ValidateCodeResponse,
    MemberOfRequest,
    MemberOfResponse,
    SubsumesRequest,
    SubsumesResponse,
)

# Coding
coding = Coding(
    system="http://snomed.info/sct",
    code="44054006",
    display="Diabetes mellitus"
)

# CodeableConcept with multiple codings
concept = CodeableConcept(
    coding=[
        Coding(system="http://snomed.info/sct", code="44054006"),
        Coding(system="http://hl7.org/fhir/sid/icd-10", code="E11")
    ],
    text="Type 2 diabetes"
)

# ValueSet programmatically
value_set = ValueSet(
    url="http://example.com/vs/test",
    name="TestValueSet",
    status="active",
    compose=ValueSetCompose(
        include=[
            ValueSetComposeInclude(
                system="http://snomed.info/sct",
                concept=[
                    ValueSetComposeIncludeConcept(code="44054006", display="Diabetes")
                ]
            )
        ]
    )
)
```

---

## Integration with CQL

### Using Terminology in CQL

```cql
library DiabetesScreening version '1.0'

using FHIR version '4.0.1'

// Reference ValueSets
valueset "Diabetes Conditions": 'http://example.com/vs/diabetes-conditions'
valueset "HbA1c Tests": 'http://example.com/vs/hba1c-tests'

context Patient

// Check if patient has diabetes using ValueSet membership
define HasDiabetes:
  exists([Condition: "Diabetes Conditions"])

// Get HbA1c observations
define HbA1cResults:
  [Observation: "HbA1c Tests"]

// Check specific code membership
define HasType2Diabetes:
  exists(
    [Condition] C
      where C.code.coding contains (
        Coding { system: 'http://snomed.info/sct', code: '44054006' }
      )
  )
```

### Running CQL with Terminology

```bash
# Start terminology server
fhir terminology serve --valuesets ./terminology --port 8081 &

# Start FHIR server with data
fhir server serve --patients 100 --port 8080 &

# Evaluate CQL (uses terminology server)
fhir cql run ./diabetes-screening.cql \
  --data http://localhost:8080 \
  --terminology http://localhost:8081
```

### Terminology Service in CQL Evaluator

```python
from fhir_cql.engine.cql import CQLEvaluator
from fhir_cql.terminology import InMemoryTerminologyService

# Create terminology service
terminology = InMemoryTerminologyService()
terminology.load_value_sets_from_directory("./terminology")

# Create evaluator with terminology service
evaluator = CQLEvaluator(terminology_service=terminology)

# Parse and evaluate CQL
library = evaluator.parse_file("./diabetes-screening.cql")
results = evaluator.evaluate(library, patient_data)
```

---

## Examples

### Example ValueSet Files

#### diabetes_codes.json

```json
{
  "resourceType": "ValueSet",
  "id": "diabetes-conditions",
  "url": "http://example.com/vs/diabetes-conditions",
  "name": "DiabetesConditions",
  "title": "Diabetes-Related Conditions",
  "status": "active",
  "compose": {
    "include": [
      {
        "system": "http://snomed.info/sct",
        "concept": [
          {"code": "44054006", "display": "Diabetes mellitus"},
          {"code": "46635009", "display": "Diabetes mellitus type 1"},
          {"code": "44054006", "display": "Diabetes mellitus type 2"},
          {"code": "11530004", "display": "Gestational diabetes"},
          {"code": "426875007", "display": "Latent autoimmune diabetes"},
          {"code": "237599002", "display": "Insulin resistance"},
          {"code": "73211009", "display": "Diabetes mellitus"},
          {"code": "359642000", "display": "Diabetes type 2 with complication"}
        ]
      }
    ]
  }
}
```

#### vital_signs_codes.json

```json
{
  "resourceType": "ValueSet",
  "id": "vital-signs",
  "url": "http://example.com/vs/vital-signs",
  "name": "VitalSigns",
  "title": "Vital Sign Observation Codes",
  "status": "active",
  "compose": {
    "include": [
      {
        "system": "http://loinc.org",
        "concept": [
          {"code": "8310-5", "display": "Body temperature"},
          {"code": "8867-4", "display": "Heart rate"},
          {"code": "8480-6", "display": "Systolic blood pressure"},
          {"code": "8462-4", "display": "Diastolic blood pressure"},
          {"code": "9279-1", "display": "Respiratory rate"},
          {"code": "2708-6", "display": "Oxygen saturation"},
          {"code": "39156-5", "display": "Body mass index"}
        ]
      }
    ]
  }
}
```

### Usage Script

```python
#!/usr/bin/env python3
"""Example terminology service usage."""

from pathlib import Path
from fhir_cql.terminology import InMemoryTerminologyService
from fhir_cql.terminology.models import ValidateCodeRequest, MemberOfRequest

def main():
    # Create service
    service = InMemoryTerminologyService()

    # Load ValueSets
    terminology_dir = Path("./examples/terminology")
    count = service.load_value_sets_from_directory(terminology_dir)
    print(f"Loaded {count} ValueSets")

    # Validate diabetes code
    print("\n--- Validating Diabetes Code ---")
    request = ValidateCodeRequest(
        url="http://example.com/vs/diabetes-conditions",
        code="44054006",
        system="http://snomed.info/sct"
    )
    response = service.validate_code(request)
    print(f"Code: 44054006 (SNOMED)")
    print(f"Valid: {response.result}")
    print(f"Display: {response.display}")

    # Check vital sign membership
    print("\n--- Checking Vital Sign Membership ---")
    vital_codes = ["8310-5", "8867-4", "12345-X"]
    for code in vital_codes:
        member_request = MemberOfRequest(
            code=code,
            system="http://loinc.org",
            valueSetUrl="http://example.com/vs/vital-signs"
        )
        result = service.member_of(member_request)
        status = "MEMBER" if result.result else "NOT MEMBER"
        print(f"  {code}: {status}")

    # Get ValueSet details
    print("\n--- ValueSet Details ---")
    vs = service.get_value_set("http://example.com/vs/vital-signs")
    if vs:
        print(f"Name: {vs.name}")
        print(f"URL: {vs.url}")
        print(f"Status: {vs.status}")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Common Issues

#### ValueSet not found

```
Error: ValueSet not found: http://example.com/vs/test
```

**Solution**: Ensure the ValueSet file is in the specified directory and has the correct URL.

```bash
# Check loaded ValueSets
fhir terminology list-valuesets ./terminology
```

#### Code system mismatch

```
Code '44054006' not found in value set
```

**Solution**: Verify the code system URL matches the ValueSet definition.

```bash
# Correct - with matching system
fhir terminology validate 44054006 \
  --system http://snomed.info/sct \
  --valueset http://example.com/vs/conditions

# Incorrect - wrong system
fhir terminology validate 44054006 \
  --system http://loinc.org \
  --valueset http://example.com/vs/conditions
```

#### Invalid JSON in ValueSet file

```
Error loading ValueSet: Invalid JSON
```

**Solution**: Validate your JSON files:

```bash
python -m json.tool < diabetes_codes.json > /dev/null
```

### Performance Tips

- **Preload ValueSets**: Load all ValueSets at startup for faster lookups
- **Use Expansion**: Pre-expanded ValueSets are faster than compose-based lookups
- **Cache Results**: Consider caching validation results for frequently checked codes

---

## Supported Code Systems

The terminology service works with any code system. Common healthcare code systems:

| System URL | Name | Description |
|------------|------|-------------|
| `http://snomed.info/sct` | SNOMED CT | Clinical terminology |
| `http://loinc.org` | LOINC | Laboratory and clinical observations |
| `http://www.nlm.nih.gov/research/umls/rxnorm` | RxNorm | Medications |
| `http://hl7.org/fhir/sid/icd-10` | ICD-10 | Diagnoses |
| `http://hl7.org/fhir/sid/icd-10-cm` | ICD-10-CM | US diagnosis codes |
| `http://www.ama-assn.org/go/cpt` | CPT | Procedures |
| `http://hl7.org/fhir/sid/cvx` | CVX | Vaccines |
| `http://hl7.org/fhir/sid/ndc` | NDC | Drug codes |
