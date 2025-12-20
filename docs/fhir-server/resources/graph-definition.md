# GraphDefinition

## Overview

A GraphDefinition defines a set of rules about how a set of resources are linked together. It specifies the connections between resources that form a coherent clinical or administrative context.

This resource is essential for defining document contents, message payloads, and complex resource graphs.

**Common use cases:**
- Document graph definition
- Message content specification
- Resource relationship mapping
- Graph-based queries
- Data extraction patterns

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/graphdefinition.html](https://hl7.org/fhir/R4/graphdefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `start` | code | Starting resource type (required) |
| `profile` | canonical | Profile on base resource |
| `link` | BackboneElement[] | Links from start resource |
| `link.path` | string | Path in the resource |
| `link.target` | BackboneElement[] | Target resources |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=patient-graph` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/GraphDefinition/patient-everything` |
| `name` | string | Computer-friendly name | `name=PatientEverything` |
| `status` | token | Status | `status=active` |
| `start` | token | Starting resource type | `start=Patient` |

## Examples

### Create a GraphDefinition

```bash
curl -X POST http://localhost:8080/baseR4/GraphDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "GraphDefinition",
    "url": "http://example.org/fhir/GraphDefinition/patient-summary",
    "name": "PatientSummary",
    "status": "active",
    "start": "Patient",
    "link": [
      {
        "path": "Patient.generalPractitioner",
        "target": [{
          "type": "Practitioner",
          "link": [{
            "path": "Practitioner.organization",
            "target": [{"type": "Organization"}]
          }]
        }]
      },
      {
        "path": "Condition.subject",
        "sliceName": "conditions",
        "target": [{
          "type": "Condition",
          "params": "subject={ref}"
        }]
      },
      {
        "path": "Observation.subject",
        "sliceName": "observations",
        "target": [{
          "type": "Observation",
          "params": "subject={ref}"
        }]
      }
    ]
  }'
```

### Search GraphDefinitions

```bash
# By starting resource
curl "http://localhost:8080/baseR4/GraphDefinition?start=Patient"

# By status
curl "http://localhost:8080/baseR4/GraphDefinition?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import GraphDefinitionGenerator

generator = GraphDefinitionGenerator(seed=42)

# Generate a random graph definition
graph = generator.generate()

# Generate for specific starting resource
patient_graph = generator.generate(start="Patient")

# Generate batch
graphs = generator.generate_batch(count=5)
```

## Related Resources

- [StructureDefinition](./structure-definition.md) - Resource profiles
- [Bundle](./bundle.md) - Graph results as bundles
- [Composition](./composition.md) - Documents using graphs
