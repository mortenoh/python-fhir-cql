# StructureMap

## Overview

A StructureMap defines a set of rules for transforming one set of resources into another. It provides a declarative way to map data between different FHIR structures or between FHIR and other formats.

This resource is essential for data transformation, migration, and integration scenarios.

**Common use cases:**
- Data transformation
- Format conversion
- Version migration
- System integration
- Data normalization

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/structuremap.html](https://hl7.org/fhir/R4/structuremap.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier (required) |
| `identifier` | Identifier[] | Business identifiers |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `structure` | BackboneElement[] | Structures used in the map |
| `import` | canonical[] | Other maps used by this map |
| `group` | BackboneElement[] | Transformation groups (required) |
| `group.name` | id | Group name (required) |
| `group.input` | BackboneElement[] | Input parameters |
| `group.rule` | BackboneElement[] | Transformation rules |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=patient-map` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/StructureMap/patient-transform` |
| `name` | string | Computer-friendly name | `name=PatientTransform` |
| `status` | token | Status | `status=active` |

## Examples

### Create a StructureMap

```bash
curl -X POST http://localhost:8080/baseR4/StructureMap \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "StructureMap",
    "url": "http://example.org/fhir/StructureMap/patient-to-bundle",
    "name": "PatientToBundle",
    "title": "Patient to Bundle Transform",
    "status": "draft",
    "structure": [
      {
        "url": "http://hl7.org/fhir/StructureDefinition/Patient",
        "mode": "source"
      },
      {
        "url": "http://hl7.org/fhir/StructureDefinition/Bundle",
        "mode": "target"
      }
    ],
    "group": [{
      "name": "PatientToBundle",
      "typeMode": "none",
      "input": [
        {"name": "src", "type": "Patient", "mode": "source"},
        {"name": "tgt", "type": "Bundle", "mode": "target"}
      ],
      "rule": [{
        "name": "patient",
        "source": [{"context": "src"}],
        "target": [{
          "context": "tgt",
          "contextType": "variable",
          "element": "entry",
          "variable": "entry"
        }]
      }]
    }]
  }'
```

### Search StructureMaps

```bash
# By status
curl "http://localhost:8080/baseR4/StructureMap?status=active"

# By name
curl "http://localhost:8080/baseR4/StructureMap?name=PatientTransform"
```

## Generator Usage

```python
from fhirkit.server.generator import StructureMapGenerator

generator = StructureMapGenerator(seed=42)

# Generate a random structure map
map = generator.generate()

# Generate with specific status
active_map = generator.generate(status="active")

# Generate batch
maps = generator.generate_batch(count=5)
```

## Structure Mode Codes

| Code | Description |
|------|-------------|
| source | Source structure for the map |
| queried | Queried structure |
| target | Target structure for the map |
| produced | Produced structure |

## Related Resources

- [StructureDefinition](./structure-definition.md) - Structures being mapped
- [ConceptMap](./concept-map.md) - Code mappings used in transforms
