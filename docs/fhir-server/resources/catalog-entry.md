# CatalogEntry

## Overview

A CatalogEntry represents an entry in a catalog of products, services, or other items. It provides metadata about items available for ordering or reference.

This resource is essential for product catalogs, service directories, and formulary management.

**Common use cases:**
- Medication formularies
- Medical device catalogs
- Laboratory test directories
- Supply catalogs
- Service directories

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/catalogentry.html](https://hl7.org/fhir/R4/catalogentry.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier[] | Business identifiers |
| `type` | CodeableConcept | Type of entry |
| `orderable` | boolean | Can be ordered (required) |
| `referencedItem` | Reference | Referenced item (required) |
| `additionalIdentifier` | Identifier[] | Additional identifiers |
| `classification` | CodeableConcept[] | Classification |
| `status` | code | draft, active, retired, unknown |
| `validityPeriod` | Period | Valid period |
| `validTo` | dateTime | Valid until |
| `lastUpdated` | dateTime | Last update date |
| `additionalCharacteristic` | CodeableConcept[] | Additional characteristics |
| `additionalClassification` | CodeableConcept[] | Additional classifications |
| `relatedEntry` | BackboneElement[] | Related entries |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=med-001` |
| `identifier` | token | Business identifier | `identifier=CAT-12345` |
| `status` | token | Entry status | `status=active` |
| `orderable` | token | Can be ordered | `orderable=true` |

## Examples

### Create a CatalogEntry

```bash
curl -X POST http://localhost:8080/baseR4/CatalogEntry \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "CatalogEntry",
    "identifier": [{
      "system": "http://example.org/catalog",
      "value": "MED-2024-001"
    }],
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v2-0351",
        "code": "M",
        "display": "Medication"
      }]
    },
    "orderable": true,
    "referencedItem": {"reference": "Medication/aspirin-81mg"},
    "classification": [{
      "coding": [{
        "system": "http://www.whocc.no/atc",
        "code": "B01AC06",
        "display": "Acetylsalicylic acid"
      }]
    }],
    "status": "active",
    "validityPeriod": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "additionalCharacteristic": [{
      "coding": [{
        "system": "http://example.org/characteristics",
        "code": "formulary",
        "display": "On formulary"
      }]
    }],
    "relatedEntry": [{
      "relationtype": {
        "coding": [{
          "system": "http://hl7.org/fhir/relation-type",
          "code": "is-replaced-by"
        }]
      },
      "item": {"reference": "CatalogEntry/new-aspirin"}
    }]
  }'
```

### Search CatalogEntries

```bash
# By status
curl "http://localhost:8080/baseR4/CatalogEntry?status=active"

# By orderable
curl "http://localhost:8080/baseR4/CatalogEntry?orderable=true"
```

## Generator Usage

```python
from fhirkit.server.generator import CatalogEntryGenerator

generator = CatalogEntryGenerator(seed=42)

# Generate random entry
entry = generator.generate()

# Generate orderable entry
orderable = generator.generate(orderable=True)

# Generate batch
entries = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| draft | Entry is a draft |
| active | Entry is active |
| retired | Entry is retired |
| unknown | Status is unknown |

## Related Resources

- [Medication](./medication.md) - Medication catalog items
- [Device](./device.md) - Device catalog items
- [HealthcareService](./healthcare-service.md) - Service catalog items
