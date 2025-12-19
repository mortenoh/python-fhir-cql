# DetectedIssue

## Overview

The DetectedIssue resource represents a clinical issue that was detected, typically by a clinical decision support system. Common uses include drug-drug interactions, duplicate therapy alerts, and contraindications.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/detectedissue.html](https://hl7.org/fhir/R4/detectedissue.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | registered, preliminary, final, amended, corrected, cancelled, entered-in-error, unknown |
| `code` | CodeableConcept | Type of issue |
| `severity` | code | high, moderate, low |
| `patient` | Reference(Patient) | Patient with the issue |
| `identifiedDateTime` | dateTime | When the issue was identified |
| `author` | Reference | Who identified the issue |
| `implicated` | Reference[] | Resources implicated |
| `detail` | string | Description of the issue |
| `reference` | uri | Reference to supporting literature |
| `mitigation` | BackboneElement[] | Actions taken |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=di-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `status` | token | Issue status | `status=final` |
| `code` | token | Issue type | `code=DRG` |
| `identified` | date | When identified | `identified=2024-01-15` |
| `author` | reference | Who identified | `author=Device/cds-system` |

## Examples

### Create a DetectedIssue

```bash
curl -X POST http://localhost:8080/baseR4/DetectedIssue \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DetectedIssue",
    "status": "final",
    "code": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "DRG",
        "display": "Drug Interaction Alert"
      }]
    },
    "severity": "high",
    "patient": {"reference": "Patient/patient-1"},
    "identifiedDateTime": "2024-01-15T11:00:00Z",
    "author": {"reference": "Device/cds-system-1"},
    "implicated": [
      {"reference": "MedicationRequest/warfarin-rx"},
      {"reference": "MedicationRequest/aspirin-rx"}
    ],
    "detail": "Warfarin and aspirin together increase bleeding risk. Monitor INR closely.",
    "mitigation": [{
      "action": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
          "code": "EMAUTH",
          "display": "Emergency Authorization Override"
        }],
        "text": "Monitor INR more frequently"
      },
      "date": "2024-01-15T11:30:00Z",
      "author": {"reference": "Practitioner/doc-1"}
    }]
  }'
```

### Search DetectedIssues

```bash
# By patient
curl "http://localhost:8080/baseR4/DetectedIssue?patient=Patient/patient-1"

# By severity
curl "http://localhost:8080/baseR4/DetectedIssue?code=DRG"

# By date
curl "http://localhost:8080/baseR4/DetectedIssue?identified=2024-01-15"
```

## Issue Types

| Code | Display | Description |
|------|---------|-------------|
| DRG | Drug Interaction | Drug-drug interaction |
| DACT | Drug Action | Duplicate therapy |
| TIME | Time | Timing issues |
| DUPTHPY | Duplicate Therapy | Same therapeutic class |
| ALLDONE | All done | Already completed |
| NOTEQUIV | Not equivalent | Not equivalent |

## Severity Codes

| Code | Description |
|------|-------------|
| high | High severity - requires attention |
| moderate | Moderate severity |
| low | Low severity - informational |
