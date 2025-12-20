# NamingSystem

## Overview

A NamingSystem defines a code system, identifier system, or other naming system and its unique identifiers. It provides metadata about naming conventions used in healthcare.

This resource is essential for identifier management, code system registration, and terminology governance.

**Common use cases:**
- Identifier system registration
- Code system documentation
- OID management
- URI namespace definition
- Terminology governance

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/namingsystem.html](https://hl7.org/fhir/R4/namingsystem.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `name` | string | Computer-friendly name (required) |
| `status` | code | draft, active, retired, unknown (required) |
| `kind` | code | codesystem, identifier, root (required) |
| `date` | dateTime | Date last changed (required) |
| `publisher` | string | Publisher name |
| `responsible` | string | Organization responsible |
| `type` | CodeableConcept | Type of naming system |
| `description` | markdown | Natural language description |
| `usage` | string | How/where the system is used |
| `uniqueId` | BackboneElement[] | Unique identifiers (required, at least one) |
| `uniqueId.type` | code | oid, uuid, uri, other (required) |
| `uniqueId.value` | string | The unique identifier value (required) |
| `uniqueId.preferred` | boolean | Is this the preferred identifier? |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=mrn-system` |
| `name` | string | Computer-friendly name | `name=MRNSystem` |
| `status` | token | Status | `status=active` |
| `kind` | token | Kind | `kind=identifier` |
| `type` | token | Type code | `type=MR` |
| `value` | string | Unique ID value | `value=2.16.840.1.113883.4.1` |

## Examples

### Create a NamingSystem

```bash
curl -X POST http://localhost:8080/baseR4/NamingSystem \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "NamingSystem",
    "name": "HospitalMRN",
    "status": "active",
    "kind": "identifier",
    "date": "2024-01-15",
    "publisher": "Example Hospital",
    "responsible": "Health Information Management",
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code": "MR",
        "display": "Medical Record Number"
      }]
    },
    "description": "Medical record numbering system for Example Hospital",
    "uniqueId": [
      {
        "type": "uri",
        "value": "http://example.org/fhir/mrn",
        "preferred": true
      },
      {
        "type": "oid",
        "value": "2.16.840.1.113883.4.123"
      }
    ]
  }'
```

### Search NamingSystems

```bash
# By kind
curl "http://localhost:8080/baseR4/NamingSystem?kind=identifier"

# By type
curl "http://localhost:8080/baseR4/NamingSystem?type=MR"

# By status
curl "http://localhost:8080/baseR4/NamingSystem?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import NamingSystemGenerator

generator = NamingSystemGenerator(seed=42)

# Generate a random naming system
ns = generator.generate()

# Generate identifier system
id_system = generator.generate(kind="identifier")

# Generate batch
systems = generator.generate_batch(count=10)
```

## Kind Codes

| Code | Description |
|------|-------------|
| codesystem | Defines a code system |
| identifier | Defines an identifier system |
| root | Defines a root OID/UUID |

## Unique ID Type Codes

| Code | Description |
|------|-------------|
| oid | OID (object identifier) |
| uuid | UUID |
| uri | URI |
| other | Other type |

## Related Resources

- [CodeSystem](./code-system.md) - Code systems documented by naming systems
- [ValueSet](./value-set.md) - Value sets using documented systems
- [Identifier](./patient.md) - Resources using identifier systems
