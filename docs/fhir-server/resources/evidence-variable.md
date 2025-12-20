# EvidenceVariable

## Overview

An EvidenceVariable defines a component of an evidence statement, including population, exposure, and outcome variables. It provides structured definitions for elements used in evidence synthesis.

This resource is essential for defining research populations, interventions, and outcomes.

**Common use cases:**
- Population definitions
- Exposure/intervention definitions
- Outcome definitions
- Inclusion/exclusion criteria
- Research variable specification

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/evidencevariable.html](https://hl7.org/fhir/R4/evidencevariable.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `identifier` | Identifier[] | Business identifiers |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `type` | code | dichotomous, continuous, descriptive |
| `characteristic` | BackboneElement[] | Characteristics defining the variable |
| `characteristic.description` | string | Characteristic description |
| `characteristic.definition[x]` | Reference, canonical, CodeableConcept, Expression | Definition of the characteristic |
| `characteristic.exclude` | boolean | Include or exclude |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=diabetes-population` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/EvidenceVariable/type2-dm` |
| `status` | token | Status | `status=active` |
| `name` | string | Name | `name=Type2DiabetesPopulation` |

## Examples

### Create an EvidenceVariable

```bash
curl -X POST http://localhost:8080/baseR4/EvidenceVariable \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "EvidenceVariable",
    "url": "http://example.org/fhir/EvidenceVariable/adult-diabetics",
    "name": "AdultDiabetics",
    "title": "Adult Patients with Type 2 Diabetes",
    "status": "active",
    "type": "dichotomous",
    "characteristic": [
      {
        "description": "Age 18 years or older",
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "133936004",
            "display": "Adult"
          }]
        }
      },
      {
        "description": "Diagnosis of Type 2 Diabetes",
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "44054006",
            "display": "Type 2 diabetes mellitus"
          }]
        }
      },
      {
        "description": "Type 1 Diabetes (excluded)",
        "exclude": true,
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "46635009",
            "display": "Type 1 diabetes mellitus"
          }]
        }
      }
    ]
  }'
```

### Search EvidenceVariables

```bash
# By status
curl "http://localhost:8080/baseR4/EvidenceVariable?status=active"

# By name
curl "http://localhost:8080/baseR4/EvidenceVariable?name:contains=diabetes"
```

## Generator Usage

```python
from fhirkit.server.generator import EvidenceVariableGenerator

generator = EvidenceVariableGenerator(seed=42)

# Generate random evidence variable
variable = generator.generate()

# Generate with specific type
dichotomous = generator.generate(type="dichotomous")

# Generate batch
variables = generator.generate_batch(count=10)
```

## Type Codes

| Code | Description |
|------|-------------|
| dichotomous | Yes/no outcome |
| continuous | Numeric measurement |
| descriptive | Descriptive variable |

## Related Resources

- [Evidence](./evidence.md) - Evidence using these variables
- [EffectEvidenceSynthesis](./effect-evidence-synthesis.md) - Evidence synthesis
- [ResearchElementDefinition](./research-element-definition.md) - Research elements
