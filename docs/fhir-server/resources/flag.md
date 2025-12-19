# Flag

## Overview

The Flag resource represents a prospective warning or alert to draw attention to a particular aspect of patient care. Common uses include allergy alerts, fall risk warnings, and safety concerns.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/flag.html](https://hl7.org/fhir/R4/flag.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | active, inactive, entered-in-error |
| `category` | CodeableConcept[] | Clinical, administrative, etc. |
| `code` | CodeableConcept | What the flag is about |
| `subject` | Reference(Patient) | Who the flag is about |
| `period` | Period | Time period when flag is active |
| `encounter` | Reference(Encounter) | Relevant encounter |
| `author` | Reference | Who created the flag |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=flag-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Flag status | `status=active` |
| `author` | reference | Flag author | `author=Practitioner/nurse-1` |
| `date` | date | Period of flag | `date=ge2024-01-01` |

## Examples

### Create a Flag

```bash
curl -X POST http://localhost:8080/baseR4/Flag \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Flag",
    "status": "active",
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/flag-category",
        "code": "safety",
        "display": "Safety"
      }]
    }],
    "code": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "129839007",
        "display": "At risk for falls"
      }],
      "text": "Fall Risk - High"
    },
    "subject": {"reference": "Patient/patient-1"},
    "period": {"start": "2024-01-10"},
    "author": {"reference": "Practitioner/nurse-1"}
  }'
```

### Search Flags

```bash
# By patient
curl "http://localhost:8080/baseR4/Flag?patient=Patient/patient-1"

# Active flags only
curl "http://localhost:8080/baseR4/Flag?status=active"

# Safety category
curl "http://localhost:8080/baseR4/Flag?category=safety"
```

## Flag Categories

| Code | Display | Description |
|------|---------|-------------|
| safety | Safety | Safety-related alerts |
| clinical | Clinical | Clinical alerts |
| administrative | Administrative | Administrative alerts |
| behavioral | Behavioral | Behavioral concerns |
| contact | Contact | Contact-related |

## Common Flag Codes (SNOMED CT)

| Code | Display |
|------|---------|
| 129839007 | At risk for falls |
| 225338004 | Risk of violence |
| 715622005 | Latex allergy |
| 427038001 | Isolation precautions |
| 10826001 | Aggressive behavior |

## Status Codes

| Code | Description |
|------|-------------|
| active | Flag is currently active |
| inactive | Flag is no longer active |
| entered-in-error | Entry was made in error |
