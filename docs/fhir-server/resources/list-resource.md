# List

## Overview

The List resource represents a curated collection of resources. Common uses include problem lists, medication lists, allergy lists, and other clinical summaries that aggregate related resources.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/list.html](https://hl7.org/fhir/R4/list.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | current, retired, entered-in-error |
| `mode` | code | working, snapshot, changes |
| `title` | string | List title |
| `code` | CodeableConcept | List type (problems, medications, etc.) |
| `subject` | Reference(Patient) | Subject of list |
| `encounter` | Reference(Encounter) | Encounter context |
| `date` | dateTime | When list was prepared |
| `source` | Reference(Practitioner) | Who prepared list |
| `orderedBy` | CodeableConcept | How items are ordered |
| `note` | Annotation[] | Notes |
| `entry` | BackboneElement[] | List items |
| `emptyReason` | CodeableConcept | Why list is empty |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=list-001` |
| `identifier` | token | Business identifier | `identifier=PROBLIST-123` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `status` | token | List status | `status=current` |
| `code` | token | List type | `code=11450-4` |
| `date` | date | List date | `date=ge2024-01-01` |
| `source` | reference | Who prepared | `source=Practitioner/789` |
| `encounter` | reference | Encounter | `encounter=Encounter/456` |

## Examples

### Create a Problem List

```bash
curl -X POST http://localhost:8080/baseR4/List \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "List",
    "status": "current",
    "mode": "working",
    "title": "Current Problems",
    "code": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "11450-4",
        "display": "Problem list"
      }]
    },
    "subject": {
      "reference": "Patient/patient-001"
    },
    "date": "2024-06-15T10:00:00Z",
    "source": {
      "reference": "Practitioner/practitioner-001"
    },
    "entry": [
      {
        "item": {"reference": "Condition/condition-001"},
        "date": "2024-06-15"
      },
      {
        "item": {"reference": "Condition/condition-002"},
        "date": "2024-05-10"
      }
    ]
  }'
```

### Create a Medication List

```bash
curl -X POST http://localhost:8080/baseR4/List \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "List",
    "status": "current",
    "mode": "working",
    "title": "Active Medications",
    "code": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "10160-0",
        "display": "History of Medication use"
      }]
    },
    "subject": {
      "reference": "Patient/patient-001"
    },
    "entry": [
      {"item": {"reference": "MedicationStatement/ms-001"}},
      {"item": {"reference": "MedicationStatement/ms-002"}}
    ]
  }'
```

### Search Lists

```bash
# By patient
curl "http://localhost:8080/baseR4/List?patient=Patient/123"

# Problem lists
curl "http://localhost:8080/baseR4/List?code=11450-4"

# Active lists
curl "http://localhost:8080/baseR4/List?status=current"
```

### Patient Compartment

```bash
# Get all lists for a patient
curl "http://localhost:8080/baseR4/Patient/123/List"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| current | Current | List is active |
| retired | Retired | List is no longer current |
| entered-in-error | Entered in Error | Data entry error |

## Mode Codes

| Code | Display | Description |
|------|---------|-------------|
| working | Working List | Items can be added/removed |
| snapshot | Snapshot List | Point-in-time view |
| changes | Change List | Changes since previous version |

## Common List Types (LOINC)

| Code | Display |
|------|---------|
| 11450-4 | Problem list |
| 10160-0 | History of Medication use |
| 48765-2 | Allergies and adverse reactions |
| 8671-3 | History of Procedures |
| 11369-6 | History of Immunization |
| 47420-5 | Functional status assessment |
