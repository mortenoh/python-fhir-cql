# ImplementationGuide

## Overview

An ImplementationGuide defines a set of rules for how FHIR resources are used, or should be used, to solve a particular problem. It provides context and documentation for FHIR profiles, extensions, and value sets.

This resource is essential for packaging and publishing FHIR implementation specifications.

**Common use cases:**
- FHIR specification packaging
- Conformance documentation
- Profile distribution
- Implementation requirements
- Interoperability standards

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/implementationguide.html](https://hl7.org/fhir/R4/implementationguide.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier (required) |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `packageId` | id | NPM package name (required) |
| `license` | code | SPDX license code |
| `fhirVersion` | code[] | FHIR version(s) this IG supports (required) |
| `dependsOn` | BackboneElement[] | IGs this depends on |
| `global` | BackboneElement[] | Global profiles |
| `definition` | BackboneElement | IG definition resources |
| `manifest` | BackboneElement | Published implementation guide |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=us-core` |
| `url` | uri | Canonical URL | `url=http://hl7.org/fhir/us/core/ImplementationGuide/hl7.fhir.us.core` |
| `name` | string | Computer-friendly name | `name=USCore` |
| `status` | token | Status | `status=active` |
| `version` | token | Version | `version=5.0.1` |

## Examples

### Create an ImplementationGuide

```bash
curl -X POST http://localhost:8080/baseR4/ImplementationGuide \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ImplementationGuide",
    "url": "http://example.org/fhir/ImplementationGuide/example-ig",
    "name": "ExampleIG",
    "title": "Example Implementation Guide",
    "status": "draft",
    "packageId": "org.example.fhir.ig",
    "fhirVersion": ["4.0.1"],
    "description": "An example implementation guide",
    "definition": {
      "resource": [{
        "reference": {"reference": "StructureDefinition/example-patient"},
        "name": "Example Patient Profile",
        "description": "Custom patient profile"
      }]
    }
  }'
```

### Search ImplementationGuides

```bash
# By status
curl "http://localhost:8080/baseR4/ImplementationGuide?status=active"

# By name
curl "http://localhost:8080/baseR4/ImplementationGuide?name=USCore"
```

## Generator Usage

```python
from fhirkit.server.generator import ImplementationGuideGenerator

generator = ImplementationGuideGenerator(seed=42)

# Generate a random implementation guide
ig = generator.generate()

# Generate with specific status
active_ig = generator.generate(status="active")

# Generate batch
guides = generator.generate_batch(count=5)
```

## Related Resources

- [StructureDefinition](./structure-definition.md) - Profiles defined in the IG
- [ValueSet](./value-set.md) - Value sets included
- [CodeSystem](./code-system.md) - Code systems included
- [CapabilityStatement](./capability-statement.md) - Capability statements
