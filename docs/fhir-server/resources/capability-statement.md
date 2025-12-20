# CapabilityStatement

## Overview

A CapabilityStatement describes the capabilities of a FHIR server or client. It declares the resources types supported, operations available, and conformance to various FHIR specifications.

This resource is essential for FHIR interoperability as it allows clients to discover what a server can do before attempting operations.

**Common use cases:**
- Server capability discovery
- Conformance declaration
- API documentation
- Interoperability assessment
- Implementation guides

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/capabilitystatement.html](https://hl7.org/fhir/R4/capabilitystatement.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical URL |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown |
| `kind` | code | instance, capability, requirements |
| `date` | dateTime | Date published |
| `publisher` | string | Publisher name |
| `description` | markdown | Description |
| `fhirVersion` | code | FHIR version supported |
| `format` | code[] | Formats supported (json, xml) |
| `rest` | BackboneElement[] | REST capabilities |
| `rest.mode` | code | client, server |
| `rest.resource` | BackboneElement[] | Resource type capabilities |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=cap-001` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/metadata` |
| `name` | string | Name | `name=ExampleServer` |
| `status` | token | Status | `status=active` |
| `version` | token | Version | `version=1.0.0` |
| `fhirversion` | token | FHIR version | `fhirversion=4.0.1` |

## Examples

### Read Server CapabilityStatement

```bash
# Standard metadata endpoint
curl "http://localhost:8080/baseR4/metadata"

# Or via resource type
curl "http://localhost:8080/baseR4/CapabilityStatement"
```

### Example CapabilityStatement Structure

```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "kind": "instance",
  "fhirVersion": "4.0.1",
  "format": ["json"],
  "rest": [{
    "mode": "server",
    "resource": [{
      "type": "Patient",
      "interaction": [
        {"code": "read"},
        {"code": "search-type"},
        {"code": "create"},
        {"code": "update"},
        {"code": "delete"}
      ],
      "searchParam": [
        {"name": "name", "type": "string"},
        {"name": "identifier", "type": "token"}
      ]
    }]
  }]
}
```

## Generator Usage

```python
from fhirkit.server.generator import CapabilityStatementGenerator

generator = CapabilityStatementGenerator(seed=42)

# Generate a capability statement
capability = generator.generate()

# Generate with specific FHIR version
r4_capability = generator.generate(
    fhir_version="4.0.1",
    status="active"
)

# Generate batch
capabilities = generator.generate_batch(count=10)
```

## Kind Codes

| Code | Description |
|------|-------------|
| instance | Describes a specific server instance |
| capability | Describes capabilities of a type of system |
| requirements | Describes required capabilities |

## Status Codes

| Code | Description |
|------|-------------|
| draft | In development |
| active | Ready for use |
| retired | No longer active |
| unknown | Status unknown |

## Related Resources

- [OperationDefinition](./operation-definition.md) - Custom operations
- [SearchParameter](./search-parameter.md) - Search parameters
- [ImplementationGuide](./implementation-guide.md) - Implementation guides
