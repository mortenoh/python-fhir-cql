# BiologicallyDerivedProduct

## Overview

A BiologicallyDerivedProduct represents a material derived from a biological source. It tracks blood products, tissues, organs, and other biological materials used in healthcare.

This resource is essential for blood banking, tissue tracking, and organ transplantation.

**Common use cases:**
- Blood product tracking
- Tissue management
- Organ donation records
- Stem cell tracking
- Transfusion medicine

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/biologicallyderivedproduct.html](https://hl7.org/fhir/R4/biologicallyderivedproduct.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier[] | Business identifiers |
| `productCategory` | code | organ, tissue, fluid, cells, biologicalAgent |
| `productCode` | CodeableConcept | Product type code |
| `status` | code | available, unavailable |
| `request` | Reference(ServiceRequest)[] | Request for the product |
| `quantity` | integer | Number of items |
| `parent` | Reference(BiologicallyDerivedProduct)[] | Parent product |
| `collection` | BackboneElement | Collection information |
| `collection.collector` | Reference | Who collected |
| `collection.source` | Reference(Patient|Organization) | Source of the product |
| `collection.collected[x]` | dateTime, Period | Collection time |
| `processing` | BackboneElement[] | Processing information |
| `manipulation` | BackboneElement | Manipulation information |
| `storage` | BackboneElement[] | Storage information |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=blood-001` |
| `identifier` | token | Product identifier | `identifier=UNIT-12345` |
| `status` | token | Product status | `status=available` |

## Examples

### Create a BiologicallyDerivedProduct

```bash
curl -X POST http://localhost:8080/baseR4/BiologicallyDerivedProduct \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "BiologicallyDerivedProduct",
    "identifier": [{
      "system": "http://example.org/blood-bank",
      "value": "UNIT-2024-001"
    }],
    "productCategory": "fluid",
    "productCode": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "256395009",
        "display": "Packed red blood cells"
      }]
    },
    "status": "available",
    "quantity": 1,
    "collection": {
      "collector": {"reference": "Practitioner/phlebotomist-001"},
      "source": {"reference": "Patient/donor-123"},
      "collectedDateTime": "2024-01-15T09:00:00Z"
    },
    "processing": [{
      "description": "Component separation",
      "procedure": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "35507004",
          "display": "Blood component separation"
        }]
      },
      "timeDateTime": "2024-01-15T10:00:00Z"
    }],
    "storage": [{
      "description": "Refrigerated storage",
      "temperature": {"value": 4, "unit": "Cel"},
      "duration": {"value": 42, "unit": "d"}
    }]
  }'
```

### Search BiologicallyDerivedProducts

```bash
# By status
curl "http://localhost:8080/baseR4/BiologicallyDerivedProduct?status=available"

# By identifier
curl "http://localhost:8080/baseR4/BiologicallyDerivedProduct?identifier=UNIT-2024-001"
```

## Generator Usage

```python
from fhirkit.server.generator import BiologicallyDerivedProductGenerator

generator = BiologicallyDerivedProductGenerator(seed=42)

# Generate random product
product = generator.generate()

# Generate blood product
blood = generator.generate(product_category="fluid")

# Generate batch
products = generator.generate_batch(count=10)
```

## Product Category Codes

| Code | Description |
|------|-------------|
| organ | Organ |
| tissue | Tissue |
| fluid | Fluid (blood, plasma) |
| cells | Cells |
| biologicalAgent | Biological agent |

## Related Resources

- [Patient](./patient.md) - Donor or recipient
- [Specimen](./specimen.md) - Source specimen
- [ServiceRequest](./service-request.md) - Request for the product
- [Procedure](./procedure.md) - Transfusion/transplant procedure
