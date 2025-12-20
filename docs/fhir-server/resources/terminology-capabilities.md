# TerminologyCapabilities

## Overview

A TerminologyCapabilities resource describes the code systems, value sets, and terminology operations that a terminology server can perform. It provides a declaration of terminology service capabilities.

This resource is essential for discovering what terminology services a server provides.

**Common use cases:**
- Terminology service discovery
- Code system capability declaration
- Validation capability advertising
- Expansion service documentation
- Translation service capabilities

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/terminologycapabilities.html](https://hl7.org/fhir/R4/terminologycapabilities.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed (required) |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `kind` | code | instance, capability, requirements (required) |
| `codeSystem` | BackboneElement[] | Code systems supported |
| `expansion` | BackboneElement | Expansion operation capabilities |
| `codeSearch` | code | explicit, all |
| `validateCode` | BackboneElement | Validation capabilities |
| `translation` | BackboneElement | Translation capabilities |
| `closure` | BackboneElement | Closure operation capabilities |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=tx-server-caps` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/TerminologyCapabilities/main` |
| `name` | string | Computer-friendly name | `name=MainTermServer` |
| `status` | token | Status | `status=active` |

## Examples

### Create a TerminologyCapabilities

```bash
curl -X POST http://localhost:8080/baseR4/TerminologyCapabilities \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "TerminologyCapabilities",
    "url": "http://example.org/fhir/TerminologyCapabilities/server",
    "name": "ExampleTermServer",
    "title": "Example Terminology Server Capabilities",
    "status": "active",
    "date": "2024-01-15",
    "kind": "instance",
    "codeSystem": [
      {
        "uri": "http://snomed.info/sct",
        "version": [{"code": "http://snomed.info/sct/900000000000207008"}]
      },
      {
        "uri": "http://loinc.org"
      }
    ],
    "expansion": {
      "hierarchical": true,
      "paging": true,
      "textFilter": "Supports text-based filtering"
    },
    "validateCode": {
      "translations": true
    }
  }'
```

### Read Server Capabilities

```bash
# Get terminology capabilities
curl "http://localhost:8080/baseR4/TerminologyCapabilities"

# By status
curl "http://localhost:8080/baseR4/TerminologyCapabilities?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import TerminologyCapabilitiesGenerator

generator = TerminologyCapabilitiesGenerator(seed=42)

# Generate terminology capabilities
caps = generator.generate()

# Generate with specific kind
instance_caps = generator.generate(kind="instance")

# Generate batch
capabilities = generator.generate_batch(count=5)
```

## Kind Codes

| Code | Description |
|------|-------------|
| instance | Describes a specific server instance |
| capability | Describes capabilities of a type of server |
| requirements | Describes required capabilities |

## Related Resources

- [CapabilityStatement](./capability-statement.md) - Overall server capabilities
- [CodeSystem](./code-system.md) - Code systems supported
- [ValueSet](./value-set.md) - Value sets supported
- [ConceptMap](./concept-map.md) - Concept maps for translation
