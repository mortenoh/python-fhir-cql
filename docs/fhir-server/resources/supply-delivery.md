# SupplyDelivery

## Overview

The SupplyDelivery resource represents the fulfillment of a supply request - the actual delivery of supplies. It tracks when supplies were delivered, what was delivered, and to whom.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/supplydelivery.html](https://hl7.org/fhir/R4/supplydelivery.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `basedOn` | Reference(SupplyRequest)[] | Request being fulfilled |
| `partOf` | Reference[] | Part of larger delivery |
| `status` | code | in-progress, completed, abandoned, entered-in-error |
| `patient` | Reference(Patient) | Patient receiving supplies |
| `type` | CodeableConcept | Supply type |
| `suppliedItem` | BackboneElement | Supplied item details |
| `suppliedItem.quantity` | Quantity | Quantity supplied |
| `suppliedItem.itemCodeableConcept` | CodeableConcept | Item supplied |
| `suppliedItem.itemReference` | Reference | Item reference |
| `occurrenceDateTime` | dateTime | When delivered |
| `occurrencePeriod` | Period | Delivery period |
| `occurrenceTiming` | Timing | Delivery timing |
| `supplier` | Reference(Practitioner,Organization) | Supplier |
| `destination` | Reference(Location) | Where delivered |
| `receiver` | Reference(Practitioner)[] | Who received |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=sd-001` |
| `identifier` | token | Business identifier | `identifier=SD-12345678` |
| `status` | token | Delivery status | `status=completed` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `receiver` | reference | Receiver | `receiver=Practitioner/789` |
| `supplier` | reference | Supplier | `supplier=Organization/456` |

## Examples

### Create a SupplyDelivery

```bash
curl -X POST http://localhost:8080/baseR4/SupplyDelivery \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SupplyDelivery",
    "identifier": [{
      "system": "http://example.org/supply-delivery-ids",
      "value": "SD-12345678"
    }],
    "basedOn": [{
      "reference": "SupplyRequest/sr-001"
    }],
    "status": "completed",
    "patient": {
      "reference": "Patient/patient-001"
    },
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supply-item-type",
        "code": "device",
        "display": "Device"
      }],
      "text": "Device"
    },
    "suppliedItem": {
      "quantity": {
        "value": 100,
        "unit": "units",
        "system": "http://unitsofmeasure.org",
        "code": "{unit}"
      },
      "itemCodeableConcept": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "468063009",
          "display": "Surgical mask"
        }],
        "text": "Surgical mask"
      }
    },
    "occurrenceDateTime": "2024-06-15T14:30:00Z",
    "supplier": {
      "reference": "Organization/supplier-001"
    },
    "destination": {
      "reference": "Location/ward-3a"
    },
    "receiver": [{
      "reference": "Practitioner/nurse-001"
    }]
  }'
```

### Create an In-Progress Delivery

```bash
curl -X POST http://localhost:8080/baseR4/SupplyDelivery \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SupplyDelivery",
    "status": "in-progress",
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supply-item-type",
        "code": "medication",
        "display": "Medication"
      }]
    },
    "suppliedItem": {
      "quantity": {
        "value": 50,
        "unit": "units"
      },
      "itemCodeableConcept": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "61968008",
          "display": "Syringe"
        }]
      }
    },
    "occurrencePeriod": {
      "start": "2024-06-15T08:00:00Z"
    },
    "supplier": {
      "reference": "Organization/central-supply"
    },
    "destination": {
      "reference": "Location/emergency-dept"
    }
  }'
```

### Search SupplyDeliveries

```bash
# By status
curl "http://localhost:8080/baseR4/SupplyDelivery?status=completed"

# By patient
curl "http://localhost:8080/baseR4/SupplyDelivery?patient=Patient/123"

# By supplier
curl "http://localhost:8080/baseR4/SupplyDelivery?supplier=Organization/456"

# By receiver
curl "http://localhost:8080/baseR4/SupplyDelivery?receiver=Practitioner/789"
```

### Patient Compartment

```bash
# Get all supply deliveries for a patient
curl "http://localhost:8080/baseR4/Patient/123/SupplyDelivery"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| in-progress | In Progress | Delivery in progress |
| completed | Completed | Delivery complete |
| abandoned | Abandoned | Delivery abandoned |
| entered-in-error | Entered in Error | Data entry error |

## Supply Types

| Code | Display | Description |
|------|---------|-------------|
| medication | Medication | Medication supplies |
| device | Device | Medical devices |

## Common Supply Items (SNOMED CT)

| Code | Display |
|------|---------|
| 468063009 | Surgical mask |
| 469008007 | Examination gloves |
| 102303004 | Intravenous catheter |
| 61968008 | Syringe |
| 118456007 | Wound dressing |
| 19923001 | Surgical gown |
| 469252005 | Sterilized gauze |
| 465839001 | Bandage |
| 425620007 | Antiseptic wipe |
| 37299003 | Glucose test strip |

## Workflow

1. **SupplyRequest** created with status `active`
2. **SupplyDelivery** created with status `in-progress`
3. On delivery, **SupplyDelivery** updated to `completed`
4. **SupplyRequest** updated to `completed`

### Linking Request to Delivery

```json
{
  "resourceType": "SupplyDelivery",
  "basedOn": [{
    "reference": "SupplyRequest/sr-001"
  }],
  "status": "completed",
  "suppliedItem": {
    "quantity": {"value": 100, "unit": "units"},
    "itemCodeableConcept": {
      "coding": [{"code": "468063009", "display": "Surgical mask"}]
    }
  }
}
```
