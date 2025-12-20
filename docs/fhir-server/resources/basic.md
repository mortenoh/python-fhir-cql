# Basic

## Overview

The Basic resource is used to represent resources that are not covered by other specific FHIR resource types. It provides a mechanism for extending FHIR to cover concepts not yet defined in the specification.

Basic is a "catch-all" resource for concepts that need to be tracked but don't fit into existing resource types. It should be used sparingly and only when no other appropriate resource type exists.

**Common use cases:**
- Custom clinical concepts
- Administrative records not covered elsewhere
- Temporary representations before formal resources exist
- Legacy data migration
- Prototype resource types

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/basic.html](https://hl7.org/fhir/R4/basic.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier[] | Business identifiers |
| `code` | CodeableConcept | Kind of resource (required) |
| `subject` | Reference(Any) | Resource the record is about |
| `created` | date | When the record was created |
| `author` | Reference(Practitioner|Patient|RelatedPerson) | Who created the record |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=basic-001` |
| `identifier` | token | Business identifier | `identifier=BSC-12345` |
| `code` | token | Resource type code | `code=referral` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `created` | date | Creation date | `created=2024-01-15` |
| `author` | reference | Author reference | `author=Practitioner/456` |

## Examples

### Create a Basic Resource

```bash
curl -X POST http://localhost:8080/baseR4/Basic \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Basic",
    "identifier": [{
      "system": "http://hospital.example.org/basic",
      "value": "BSC-2024-001"
    }],
    "code": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/basic-resource-type",
        "code": "referral",
        "display": "Referral"
      }]
    },
    "subject": {"reference": "Patient/123"},
    "created": "2024-01-15",
    "author": {"reference": "Practitioner/456"}
  }'
```

### Search Basic Resources

```bash
# By code
curl "http://localhost:8080/baseR4/Basic?code=referral"

# By subject
curl "http://localhost:8080/baseR4/Basic?subject=Patient/123"

# By author
curl "http://localhost:8080/baseR4/Basic?author=Practitioner/456"
```

## Generator Usage

```python
from fhirkit.server.generator import BasicGenerator

generator = BasicGenerator(seed=42)

# Generate a random basic resource
basic = generator.generate()

# Generate with specific code
referral = generator.generate(
    code_system="http://terminology.hl7.org/CodeSystem/basic-resource-type",
    code="referral"
)

# Generate batch
basics = generator.generate_batch(count=10)
```

## Common Code Values

| Code | Description |
|------|-------------|
| consent | Consent record |
| referral | Referral record |
| advevent | Adverse event record |
| protocol | Study protocol |
| account | Account record |
| invoice | Invoice record |
| adjudicat | Adjudication record |
| predetreq | Pre-determination request |
| predetermine | Pre-determination |

## Related Resources

All FHIR resources can potentially be related to Basic, depending on its use case.
