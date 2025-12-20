# ConceptMap

## Overview

A ConceptMap defines relationships between concepts from different code systems. It provides mapping rules to translate codes from one terminology to another.

This resource is essential for terminology translation, data migration, and system integration.

**Common use cases:**
- Code system translation
- Terminology mapping
- Data migration
- Cross-system interoperability
- Legacy system integration

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/conceptmap.html](https://hl7.org/fhir/R4/conceptmap.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `identifier` | Identifier | Business identifier |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `source[x]` | uri or canonical | Source value set |
| `target[x]` | uri or canonical | Target value set |
| `group` | BackboneElement[] | Groups of mappings |
| `group.source` | uri | Source code system |
| `group.target` | uri | Target code system |
| `group.element` | BackboneElement[] | Mappings for each source concept |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=icd10-snomed-map` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/ConceptMap/icd10-to-snomed` |
| `name` | string | Computer-friendly name | `name=ICD10ToSNOMED` |
| `status` | token | Status | `status=active` |
| `source` | reference | Source value set | `source=ValueSet/icd10-codes` |
| `target` | reference | Target value set | `target=ValueSet/snomed-conditions` |

## Examples

### Create a ConceptMap

```bash
curl -X POST http://localhost:8080/baseR4/ConceptMap \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ConceptMap",
    "url": "http://example.org/fhir/ConceptMap/gender-mapping",
    "name": "GenderMapping",
    "title": "Administrative Gender to SNOMED Mapping",
    "status": "active",
    "sourceUri": "http://hl7.org/fhir/ValueSet/administrative-gender",
    "targetUri": "http://snomed.info/sct?fhir_vs",
    "group": [{
      "source": "http://hl7.org/fhir/administrative-gender",
      "target": "http://snomed.info/sct",
      "element": [
        {
          "code": "male",
          "display": "Male",
          "target": [{
            "code": "248153007",
            "display": "Male",
            "equivalence": "equivalent"
          }]
        },
        {
          "code": "female",
          "display": "Female",
          "target": [{
            "code": "248152002",
            "display": "Female",
            "equivalence": "equivalent"
          }]
        },
        {
          "code": "unknown",
          "display": "Unknown",
          "target": [{
            "code": "261665006",
            "display": "Unknown",
            "equivalence": "wider"
          }]
        }
      ]
    }]
  }'
```

### Search ConceptMaps

```bash
# By source
curl "http://localhost:8080/baseR4/ConceptMap?source=http://hl7.org/fhir/ValueSet/administrative-gender"

# By status
curl "http://localhost:8080/baseR4/ConceptMap?status=active"
```

### Translate Using ConceptMap

```bash
# Use $translate operation
curl "http://localhost:8080/baseR4/ConceptMap/$translate?code=male&system=http://hl7.org/fhir/administrative-gender&target=http://snomed.info/sct"
```

## Generator Usage

```python
from fhirkit.server.generator import ConceptMapGenerator

generator = ConceptMapGenerator(seed=42)

# Generate a random concept map
map = generator.generate()

# Generate with specific status
active_map = generator.generate(status="active")

# Generate batch
maps = generator.generate_batch(count=10)
```

## Equivalence Codes

| Code | Description |
|------|-------------|
| relatedto | Related but not exact |
| equivalent | Exactly the same |
| equal | Identical in meaning |
| wider | Target is broader |
| subsumes | Target subsumes source |
| narrower | Target is narrower |
| specializes | Source specializes target |
| inexact | Inexact mapping |
| unmatched | No match found |
| disjoint | No overlap |

## Related Resources

- [CodeSystem](./code-system.md) - Code systems being mapped
- [ValueSet](./value-set.md) - Value sets containing codes
- [TerminologyCapabilities](./terminology-capabilities.md) - Translation capabilities
