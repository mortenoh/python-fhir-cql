# Linkage

## Overview

A Linkage identifies two or more records that are believed to represent the same real-world occurrence. It is used to link duplicate or related resources that refer to the same entity.

This resource is commonly used for patient matching, record deduplication, and maintaining relationships between resources in a master data management context.

**Common use cases:**
- Duplicate patient record linking
- Master person index management
- Record deduplication
- Cross-system resource matching
- Identity resolution

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/linkage.html](https://hl7.org/fhir/R4/linkage.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `active` | boolean | Whether linkage is active |
| `author` | Reference(Practitioner|Organization) | Who is responsible for the linkage |
| `item` | BackboneElement[] | Items linked together |
| `item.type` | code | source, alternate, historical |
| `item.resource` | Reference(Any) | Resource being linked |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=linkage-001` |
| `author` | reference | Author reference | `author=Practitioner/456` |
| `item` | reference | Linked resource | `item=Patient/123` |
| `source` | reference | Source resource | `source=Patient/123` |

## Examples

### Create a Linkage

```bash
curl -X POST http://localhost:8080/baseR4/Linkage \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Linkage",
    "active": true,
    "author": {"reference": "Organization/mpi-system"},
    "item": [
      {
        "type": "source",
        "resource": {"reference": "Patient/123"}
      },
      {
        "type": "alternate",
        "resource": {"reference": "Patient/456"}
      },
      {
        "type": "historical",
        "resource": {"reference": "Patient/789"}
      }
    ]
  }'
```

### Search Linkages

```bash
# By linked item
curl "http://localhost:8080/baseR4/Linkage?item=Patient/123"

# By author
curl "http://localhost:8080/baseR4/Linkage?author=Organization/mpi-system"

# By source
curl "http://localhost:8080/baseR4/Linkage?source=Patient/123"
```

## Generator Usage

```python
from fhirkit.server.generator import LinkageGenerator

generator = LinkageGenerator(seed=42)

# Generate a random linkage
linkage = generator.generate()

# Generate batch
linkages = generator.generate_batch(count=10)
```

## Item Type Codes

| Code | Description |
|------|-------------|
| source | Primary resource - the "master" record |
| alternate | Alternative representation of the same information |
| historical | Historical/obsolete version of the resource |

## Related Resources

- [Patient](./patient.md) - Commonly linked resource
- [Person](./person.md) - Master person record
- [Practitioner](./practitioner.md) - Practitioner records
