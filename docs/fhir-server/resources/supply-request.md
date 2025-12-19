# SupplyRequest

## Overview

The SupplyRequest resource represents a request for medical supplies or equipment. It is used to order items like surgical masks, gloves, IV catheters, and other clinical supplies.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/supplyrequest.html](https://hl7.org/fhir/R4/supplyrequest.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | draft, active, suspended, cancelled, completed, entered-in-error, unknown |
| `category` | CodeableConcept | Supply category |
| `priority` | code | routine, urgent, asap, stat |
| `itemCodeableConcept` | CodeableConcept | Item being requested |
| `itemReference` | Reference(Medication,Substance,Device) | Item reference |
| `quantity` | Quantity | Quantity requested (required) |
| `parameter` | BackboneElement[] | Request parameters |
| `occurrenceDateTime` | dateTime | When needed |
| `occurrencePeriod` | Period | When needed (period) |
| `occurrenceTiming` | Timing | When needed (timing) |
| `authoredOn` | dateTime | When request created |
| `requester` | Reference(Practitioner) | Who requested |
| `supplier` | Reference(Organization)[] | Suppliers |
| `reasonCode` | CodeableConcept[] | Why requested |
| `reasonReference` | Reference[] | Why references |
| `deliverFrom` | Reference(Organization,Location) | Deliver from |
| `deliverTo` | Reference(Organization,Location,Patient) | Deliver to |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=sr-001` |
| `identifier` | token | Business identifier | `identifier=SR-12345678` |
| `status` | token | Request status | `status=active` |
| `category` | token | Supply category | `category=central` |
| `date` | date | When authored | `date=ge2024-01-01` |
| `requester` | reference | Requester | `requester=Practitioner/789` |
| `subject` | reference | Patient (if applicable) | `subject=Patient/123` |
| `supplier` | reference | Supplier | `supplier=Organization/456` |

## Examples

### Create a SupplyRequest

```bash
curl -X POST http://localhost:8080/baseR4/SupplyRequest \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SupplyRequest",
    "identifier": [{
      "system": "http://example.org/supply-request-ids",
      "value": "SR-12345678"
    }],
    "status": "active",
    "priority": "routine",
    "category": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supply-kind",
        "code": "central",
        "display": "Central Supply"
      }],
      "text": "Central Supply"
    },
    "itemCodeableConcept": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "468063009",
        "display": "Surgical mask"
      }],
      "text": "Surgical mask"
    },
    "quantity": {
      "value": 500,
      "unit": "units",
      "system": "http://unitsofmeasure.org",
      "code": "{unit}"
    },
    "occurrenceDateTime": "2024-06-20",
    "authoredOn": "2024-06-15T10:00:00Z",
    "requester": {
      "reference": "Practitioner/practitioner-001"
    },
    "supplier": [{
      "reference": "Organization/supplier-001"
    }],
    "deliverTo": {
      "reference": "Location/ward-3a"
    },
    "reasonCode": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supplyrequest-reason",
        "code": "ward-stock",
        "display": "Ward Stock"
      }]
    }]
  }'
```

### Create an Urgent Patient-Specific Request

```bash
curl -X POST http://localhost:8080/baseR4/SupplyRequest \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SupplyRequest",
    "status": "active",
    "priority": "urgent",
    "category": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supply-kind",
        "code": "nonstock",
        "display": "Non-Stock"
      }]
    },
    "itemCodeableConcept": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "102303004",
        "display": "Intravenous catheter"
      }]
    },
    "quantity": {
      "value": 10,
      "unit": "units"
    },
    "authoredOn": "2024-06-15T14:30:00Z",
    "requester": {
      "reference": "Practitioner/practitioner-001"
    },
    "deliverFrom": {
      "display": "Central Supply"
    },
    "deliverTo": {
      "reference": "Patient/patient-001"
    },
    "reasonCode": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/supplyrequest-reason",
        "code": "patient-care",
        "display": "Patient Care"
      }]
    }]
  }'
```

### Search SupplyRequests

```bash
# By status
curl "http://localhost:8080/baseR4/SupplyRequest?status=active"

# By priority
curl "http://localhost:8080/baseR4/SupplyRequest?priority=urgent"

# By requester
curl "http://localhost:8080/baseR4/SupplyRequest?requester=Practitioner/789"

# By date
curl "http://localhost:8080/baseR4/SupplyRequest?date=ge2024-06-01"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| draft | Draft | Request is being prepared |
| active | Active | Request is active |
| suspended | Suspended | Request is on hold |
| cancelled | Cancelled | Request was cancelled |
| completed | Completed | Request fulfilled |
| entered-in-error | Entered in Error | Data entry error |
| unknown | Unknown | Status unknown |

## Priority Codes

| Code | Display | Description |
|------|---------|-------------|
| routine | Routine | Normal priority |
| urgent | Urgent | Needs attention soon |
| asap | ASAP | As soon as possible |
| stat | STAT | Immediately |

## Supply Categories

| Code | Display | Description |
|------|---------|-------------|
| central | Central Supply | From central supply |
| nonstock | Non-Stock | Non-stock item |

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

## Reason Codes

| Code | Display |
|------|---------|
| patient-care | Patient Care |
| ward-stock | Ward Stock |
