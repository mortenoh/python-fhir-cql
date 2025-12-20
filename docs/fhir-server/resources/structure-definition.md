# StructureDefinition

## Overview

A StructureDefinition defines the structure and constraints on resources, data types, and extensions. It is the foundation of FHIR's profiling mechanism and provides the rules for validating resources.

This resource is essential for defining implementation guides, creating resource profiles, and specifying conformance requirements.

**Common use cases:**
- Resource profiling
- Extension definitions
- Implementation guide authoring
- Validation rule specification
- Data type constraints

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/structuredefinition.html](https://hl7.org/fhir/R4/structuredefinition.html)

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
| `kind` | code | primitive-type, complex-type, resource, logical (required) |
| `abstract` | boolean | Whether this is an abstract definition (required) |
| `type` | uri | Type defined or constrained (required) |
| `baseDefinition` | canonical | Definition that this derives from |
| `derivation` | code | specialization, constraint |
| `differential` | BackboneElement | Differential view of changes |
| `snapshot` | BackboneElement | Snapshot view of the structure |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=us-core-patient` |
| `url` | uri | Canonical URL | `url=http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient` |
| `name` | string | Computer-friendly name | `name=USCorePatient` |
| `status` | token | Status | `status=active` |
| `kind` | token | Kind of structure | `kind=resource` |
| `type` | uri | Type defined | `type=Patient` |
| `base` | reference | Base definition | `base=http://hl7.org/fhir/StructureDefinition/Patient` |

## Examples

### Create a StructureDefinition

```bash
curl -X POST http://localhost:8080/baseR4/StructureDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "StructureDefinition",
    "url": "http://example.org/fhir/StructureDefinition/custom-patient",
    "name": "CustomPatient",
    "title": "Custom Patient Profile",
    "status": "draft",
    "kind": "resource",
    "abstract": false,
    "type": "Patient",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
    "derivation": "constraint",
    "differential": {
      "element": [{
        "id": "Patient.identifier",
        "path": "Patient.identifier",
        "min": 1
      }]
    }
  }'
```

### Search StructureDefinitions

```bash
# By type
curl "http://localhost:8080/baseR4/StructureDefinition?type=Patient"

# By kind
curl "http://localhost:8080/baseR4/StructureDefinition?kind=resource"

# By status
curl "http://localhost:8080/baseR4/StructureDefinition?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import StructureDefinitionGenerator

generator = StructureDefinitionGenerator(seed=42)

# Generate a random structure definition
structure = generator.generate()

# Generate with specific parameters
patient_profile = generator.generate(
    type="Patient",
    kind="resource",
    status="active"
)

# Generate batch
structures = generator.generate_batch(count=10)
```

## Kind Codes

| Code | Description |
|------|-------------|
| primitive-type | Defines a primitive type |
| complex-type | Defines a complex type |
| resource | Defines a resource type |
| logical | Defines a logical model |

## Related Resources

- [ImplementationGuide](./implementation-guide.md) - Implementation guides containing profiles
- [ValueSet](./value-set.md) - Value sets used in profiles
- [CodeSystem](./code-system.md) - Code systems referenced
