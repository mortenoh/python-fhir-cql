# ResearchDefinition

## Overview

A ResearchDefinition defines a research study, including its population, exposure, and outcome. It provides a structured template for describing research protocols and study designs.

This resource is essential for clinical research planning and protocol documentation.

**Common use cases:**
- Research protocol definition
- Study design documentation
- PICO framework representation
- Clinical trial planning
- Research question formulation

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/researchdefinition.html](https://hl7.org/fhir/R4/researchdefinition.html)

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
| `subject[x]` | CodeableConcept or Reference | Subject of the research |
| `population` | Reference(ResearchElementDefinition) | Population (required) |
| `exposure` | Reference(ResearchElementDefinition) | Exposure |
| `exposureAlternative` | Reference(ResearchElementDefinition) | Alternative exposure |
| `outcome` | Reference(ResearchElementDefinition) | Outcome |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=diabetes-study` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/ResearchDefinition/dm-trial` |
| `status` | token | Status | `status=active` |
| `title` | string | Title | `title:contains=diabetes` |

## Examples

### Create a ResearchDefinition

```bash
curl -X POST http://localhost:8080/baseR4/ResearchDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ResearchDefinition",
    "url": "http://example.org/fhir/ResearchDefinition/metformin-outcomes",
    "name": "MetforminOutcomes",
    "title": "Metformin Cardiovascular Outcomes Study",
    "status": "active",
    "description": "Study of cardiovascular outcomes in patients treated with metformin",
    "subjectCodeableConcept": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "44054006",
        "display": "Type 2 diabetes mellitus"
      }]
    },
    "population": {
      "reference": "ResearchElementDefinition/diabetic-adults"
    },
    "exposure": {
      "reference": "ResearchElementDefinition/metformin-treatment"
    },
    "exposureAlternative": {
      "reference": "ResearchElementDefinition/other-oral-agents"
    },
    "outcome": {
      "reference": "ResearchElementDefinition/cv-events"
    }
  }'
```

### Search ResearchDefinitions

```bash
# By status
curl "http://localhost:8080/baseR4/ResearchDefinition?status=active"

# By title
curl "http://localhost:8080/baseR4/ResearchDefinition?title:contains=metformin"
```

## Generator Usage

```python
from fhirkit.server.generator import ResearchDefinitionGenerator

generator = ResearchDefinitionGenerator(seed=42)

# Generate random research definition
definition = generator.generate()

# Generate with specific status
active = generator.generate(status="active")

# Generate batch
definitions = generator.generate_batch(count=5)
```

## Related Resources

- [ResearchElementDefinition](./research-element-definition.md) - Population, exposure, outcome definitions
- [ResearchStudy](./research-study.md) - Actual research studies
- [Evidence](./evidence.md) - Evidence from research
