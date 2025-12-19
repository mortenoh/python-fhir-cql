# Profile Validation

## Overview

The FHIR server supports validating resources against StructureDefinition profiles. This enables conformance checking against implementation guides like US Core, IPS, and custom profiles.

## Features

- **Profile Storage**: Store StructureDefinition resources via CRUD operations
- **Profile Validation**: Validate resources against declared profiles
- **Cardinality Checking**: Validates min/max occurrence constraints
- **Fixed Values**: Validates fixed[x] values
- **Pattern Matching**: Validates pattern[x] values
- **FHIRPath Constraints**: Evaluates FHIRPath constraint expressions

## Configuration

Enable profile validation on write via environment variables:

```bash
# Validate against declared profiles on create/update
export FHIR_SERVER_VALIDATE_PROFILES_ON_WRITE=true
```

Or in code:

```python
from fhirkit.server.config import FHIRServerSettings

settings = FHIRServerSettings(
    validate_profiles_on_write=True,
)
```

## Usage

### 1. Store a Profile

First, create a StructureDefinition profile:

```bash
curl -X PUT http://localhost:8080/baseR4/StructureDefinition/simple-patient \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "StructureDefinition",
    "id": "simple-patient",
    "url": "http://example.org/fhir/StructureDefinition/simple-patient",
    "name": "SimplePatient",
    "status": "active",
    "kind": "resource",
    "abstract": false,
    "type": "Patient",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
    "derivation": "constraint",
    "snapshot": {
      "element": [
        {"id": "Patient", "path": "Patient", "min": 0, "max": "*"},
        {"id": "Patient.identifier", "path": "Patient.identifier", "min": 1, "max": "*"},
        {"id": "Patient.name", "path": "Patient.name", "min": 1, "max": "*"},
        {"id": "Patient.name.family", "path": "Patient.name.family", "min": 1, "max": "1"}
      ]
    }
  }'
```

### 2. Validate Against Profile (Query Parameter)

```bash
curl -X POST "http://localhost:8080/baseR4/Patient/\$validate?profile=http://example.org/fhir/StructureDefinition/simple-patient" \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Patient",
    "identifier": [{"system": "http://hospital.example.org", "value": "12345"}],
    "name": [{"family": "Smith", "given": ["John"]}]
  }'
```

### 3. Validate Against Profile (Parameters Resource)

```bash
curl -X POST http://localhost:8080/baseR4/Patient/\$validate \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Parameters",
    "parameter": [
      {
        "name": "resource",
        "resource": {
          "resourceType": "Patient",
          "identifier": [{"system": "http://hospital.example.org", "value": "12345"}],
          "name": [{"family": "Smith", "given": ["John"]}]
        }
      },
      {
        "name": "profile",
        "valueUri": "http://example.org/fhir/StructureDefinition/simple-patient"
      }
    ]
  }'
```

### 4. Validate Existing Resource

When validating an existing resource, the server can automatically use declared profiles:

```bash
# Resource with declared profile
curl -X PUT http://localhost:8080/baseR4/Patient/patient-001 \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Patient",
    "id": "patient-001",
    "meta": {
      "profile": ["http://example.org/fhir/StructureDefinition/simple-patient"]
    },
    "identifier": [{"system": "http://hospital.example.org", "value": "12345"}],
    "name": [{"family": "Smith", "given": ["John"]}]
  }'

# Validate - will use meta.profile automatically
curl http://localhost:8080/baseR4/Patient/patient-001/\$validate
```

## Validation Response

Validation returns an OperationOutcome resource:

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "required",
      "diagnostics": "Element 'identifier' has 0 occurrences, minimum required is 1",
      "location": ["identifier"]
    },
    {
      "severity": "information",
      "code": "informational",
      "diagnostics": "Validation successful"
    }
  ]
}
```

## Search Parameters

StructureDefinition resources support these search parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=simple-patient` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/StructureDefinition/simple-patient` |
| `name` | string | Name of profile | `name=SimplePatient` |
| `title` | string | Human-readable title | `title:contains=Patient` |
| `version` | token | Version | `version=1.0.0` |
| `status` | token | Publication status | `status=active` |
| `publisher` | string | Publisher name | `publisher=Example` |
| `type` | token | Constrained type | `type=Patient` |
| `kind` | token | Kind of structure | `kind=resource` |
| `base` | uri | Base definition URL | `base=http://hl7.org/fhir/StructureDefinition/Patient` |
| `derivation` | token | Derivation type | `derivation=constraint` |

## GraphQL

Query StructureDefinitions via GraphQL:

```graphql
{
  structureDefinition(_id: "simple-patient") {
    id
    data
  }

  structureDefinitions(type: "Patient", status: "active") {
    id
    data
  }
}
```

Mutations:

```graphql
mutation {
  createStructureDefinition(data: {
    resourceType: "StructureDefinition",
    url: "http://example.org/fhir/StructureDefinition/my-profile",
    name: "MyProfile",
    status: "draft",
    kind: "resource",
    abstract: false,
    type: "Observation",
    baseDefinition: "http://hl7.org/fhir/StructureDefinition/Observation",
    derivation: "constraint"
  }) {
    id
    data
  }
}
```

## Validation Checks

The profile validator performs these checks:

### Cardinality (min/max)

```json
{
  "id": "Patient.identifier",
  "path": "Patient.identifier",
  "min": 1,
  "max": "*"
}
```

If a resource has 0 identifiers, validation fails with:
> Element 'identifier' has 0 occurrences, minimum required is 1

### Fixed Values

```json
{
  "id": "Observation.status",
  "path": "Observation.status",
  "fixedCode": "final"
}
```

If status is not "final", validation fails with:
> Element 'status' value does not match fixed value

### Pattern Values

```json
{
  "id": "Observation.category",
  "path": "Observation.category",
  "patternCodeableConcept": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "vital-signs"
    }]
  }
}
```

The resource must contain at least the pattern elements.

### FHIRPath Constraints

```json
{
  "id": "Observation",
  "path": "Observation",
  "constraint": [{
    "key": "obs-1",
    "severity": "error",
    "human": "Must have value or data absent reason",
    "expression": "value.exists() or dataAbsentReason.exists()"
  }]
}
```

## Sample Profiles

The server includes sample profiles in `examples/fhir/`:

- `StructureDefinition-simple-patient.json` - Patient with required identifier and name
- `StructureDefinition-vital-signs-observation.json` - Observation for vital signs

## Limitations

Current limitations (may be addressed in future versions):

- **No slicing validation**: Slicing discriminators are not evaluated
- **No extension definitions**: Custom extension validation not supported
- **No terminology service**: Code bindings are logged but not fully validated
- **Single profile**: Validates against one profile at a time

## Python API

Use the ProfileValidator class directly:

```python
from fhirkit.server.validation import ProfileValidator
from fhirkit.server.storage import FHIRStore

store = FHIRStore()
validator = ProfileValidator(store)

resource = {
    "resourceType": "Patient",
    "name": [{"family": "Smith"}]
}

result = validator.validate_against_profile(
    resource,
    "http://example.org/fhir/StructureDefinition/simple-patient"
)

if result.valid:
    print("Resource conforms to profile")
else:
    for issue in result.issues:
        print(f"{issue.severity}: {issue.message}")
```
