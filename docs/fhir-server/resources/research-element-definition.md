# ResearchElementDefinition

## Overview

A ResearchElementDefinition describes a single element of a PICO (Population, Intervention, Comparison, Outcome) research framework. It provides detailed definitions for research variables.

This resource is essential for precise research protocol specifications and evidence synthesis.

**Common use cases:**
- Population criteria definition
- Intervention specification
- Outcome measurement definition
- Comparison group definition
- Research variable documentation

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/researchelementdefinition.html](https://hl7.org/fhir/R4/researchelementdefinition.html)

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
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `type` | code | population, exposure, outcome (required) |
| `characteristic` | BackboneElement[] | Characteristics of the element (required) |
| `characteristic.definition[x]` | CodeableConcept, canonical, Expression, DataRequirement | Definition |
| `characteristic.studyEffective[x]` | dateTime, Period, Duration, Timing | Study effective period |
| `characteristic.exclude` | boolean | Exclude from the element |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=diabetic-population` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/ResearchElementDefinition/dm` |
| `status` | token | Status | `status=active` |
| `type` | token | Element type | `type=population` |

## Examples

### Create a ResearchElementDefinition

```bash
curl -X POST http://localhost:8080/baseR4/ResearchElementDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ResearchElementDefinition",
    "url": "http://example.org/fhir/ResearchElementDefinition/adult-dm2",
    "name": "AdultType2Diabetics",
    "title": "Adult Patients with Type 2 Diabetes",
    "status": "active",
    "type": "population",
    "characteristic": [
      {
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "44054006",
            "display": "Type 2 diabetes mellitus"
          }]
        }
      },
      {
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "133936004",
            "display": "Adult"
          }]
        }
      },
      {
        "exclude": true,
        "definitionCodeableConcept": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "77386006",
            "display": "Pregnant"
          }]
        }
      }
    ]
  }'
```

### Search ResearchElementDefinitions

```bash
# By type
curl "http://localhost:8080/baseR4/ResearchElementDefinition?type=population"

# By status
curl "http://localhost:8080/baseR4/ResearchElementDefinition?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import ResearchElementDefinitionGenerator

generator = ResearchElementDefinitionGenerator(seed=42)

# Generate random definition
element = generator.generate()

# Generate population element
population = generator.generate(type="population")

# Generate batch
elements = generator.generate_batch(count=10)
```

## Type Codes

| Code | Description |
|------|-------------|
| population | Defines a population |
| exposure | Defines an exposure/intervention |
| outcome | Defines an outcome |

## Related Resources

- [ResearchDefinition](./research-definition.md) - Research definitions using elements
- [EvidenceVariable](./evidence-variable.md) - Evidence variables
- [ResearchStudy](./research-study.md) - Research studies
