# AdverseEvent

## Overview

The AdverseEvent resource captures actual or potential adverse events that occurred during healthcare delivery. It includes medication reactions, device problems, and other safety events.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/adverseevent.html](https://hl7.org/fhir/R4/adverseevent.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `actuality` | code | actual, potential |
| `category` | CodeableConcept[] | Category of the event |
| `event` | CodeableConcept | Type of adverse event |
| `subject` | Reference(Patient) | Patient who had the event |
| `encounter` | Reference(Encounter) | Related encounter |
| `date` | dateTime | When the event occurred |
| `detected` | dateTime | When the event was detected |
| `recordedDate` | dateTime | When the event was recorded |
| `seriousness` | CodeableConcept | Seriousness level |
| `severity` | CodeableConcept | Severity level |
| `outcome` | CodeableConcept | Resolution status |
| `recorder` | Reference | Who recorded the event |
| `suspectEntity` | BackboneElement[] | Suspected causes |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=ae-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `actuality` | token | Actual or potential | `actuality=actual` |
| `category` | token | Event category | `category=medication-mishap` |
| `date` | date | Event date | `date=2024-01-16` |
| `event` | token | Event type code | `event=http://snomed.info/sct\|39579001` |
| `seriousness` | token | Seriousness level | `seriousness=serious` |

## Examples

### Create an AdverseEvent

```bash
curl -X POST http://localhost:8080/baseR4/AdverseEvent \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "AdverseEvent",
    "actuality": "actual",
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-category",
        "code": "medication-mishap",
        "display": "Medication Mishap"
      }]
    }],
    "event": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "39579001",
        "display": "Anaphylaxis"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "date": "2024-01-16T08:30:00Z",
    "detected": "2024-01-16T08:35:00Z",
    "seriousness": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-seriousness",
        "code": "serious",
        "display": "Serious"
      }]
    },
    "severity": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-severity",
        "code": "severe",
        "display": "Severe"
      }]
    },
    "outcome": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-outcome",
        "code": "resolved",
        "display": "Resolved"
      }]
    },
    "suspectEntity": [{
      "instance": {"reference": "Medication/penicillin-1"}
    }]
  }'
```

### Search AdverseEvents

```bash
# By patient
curl "http://localhost:8080/baseR4/AdverseEvent?patient=Patient/patient-1"

# Actual events
curl "http://localhost:8080/baseR4/AdverseEvent?actuality=actual"

# Serious events
curl "http://localhost:8080/baseR4/AdverseEvent?seriousness=serious"
```

## Event Categories

| Code | Display |
|------|---------|
| product-problem | Product Problem |
| product-quality | Product Quality |
| product-use-error | Product Use Error |
| wrong-dose | Wrong Dose |
| incorrect-prescribing | Incorrect Prescribing |
| medical-device-use-error | Medical Device Use Error |
| medication-mishap | Medication Mishap |
| unsafe-physical-environment | Unsafe Environment |

## Seriousness Codes

| Code | Display | Description |
|------|---------|-------------|
| non-serious | Non-serious | Not serious |
| serious | Serious | Serious outcome |
| serious-resultedin-death | Death | Resulted in death |
| serious-resultedin-hospitalization | Hospitalization | Required hospitalization |
| serious-resultedin-disability | Disability | Resulted in disability |
