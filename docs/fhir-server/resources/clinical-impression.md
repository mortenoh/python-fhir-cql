# ClinicalImpression

## Overview

The ClinicalImpression resource captures a clinical assessment performed by a healthcare provider. It represents the clinician's interpretation and summary of the patient's condition.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/clinicalimpression.html](https://hl7.org/fhir/R4/clinicalimpression.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | in-progress, completed, entered-in-error |
| `description` | string | Description of the clinical impression |
| `subject` | Reference(Patient) | Patient being assessed |
| `encounter` | Reference(Encounter) | Related encounter |
| `effectiveDateTime` | dateTime | When the assessment was made |
| `date` | dateTime | When the impression was recorded |
| `assessor` | Reference(Practitioner) | Who made the assessment |
| `problem` | Reference(Condition)[] | Problems being assessed |
| `investigation` | BackboneElement[] | One or more investigations |
| `summary` | string | Summary of the assessment |
| `finding` | BackboneElement[] | Possible findings |
| `prognosisCodeableConcept` | CodeableConcept[] | Prognosis codes |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=ci-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Assessment status | `status=completed` |
| `date` | date | When recorded | `date=2024-01-15` |
| `assessor` | reference | Who assessed | `assessor=Practitioner/doc-1` |
| `encounter` | reference | Related encounter | `encounter=Encounter/enc-1` |

## Examples

### Create a ClinicalImpression

```bash
curl -X POST http://localhost:8080/baseR4/ClinicalImpression \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ClinicalImpression",
    "status": "completed",
    "description": "Comprehensive assessment for chest pain",
    "subject": {"reference": "Patient/patient-1"},
    "encounter": {"reference": "Encounter/enc-1"},
    "effectiveDateTime": "2024-01-15T14:00:00Z",
    "date": "2024-01-15T14:30:00Z",
    "assessor": {"reference": "Practitioner/doc-1"},
    "problem": [
      {"reference": "Condition/chest-pain-1"}
    ],
    "investigation": [{
      "code": {"text": "Initial workup"},
      "item": [
        {"reference": "Observation/ecg-1", "display": "ECG - normal"},
        {"reference": "Observation/troponin-1", "display": "Troponin - negative"}
      ]
    }],
    "summary": "55-year-old male with atypical chest pain. Cardiac workup negative. Likely musculoskeletal.",
    "finding": [{
      "itemCodeableConcept": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "102557007",
          "display": "Musculoskeletal chest pain"
        }]
      },
      "basis": "Reproducible on palpation, negative cardiac workup"
    }],
    "prognosisCodeableConcept": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "170968001",
        "display": "Prognosis good"
      }]
    }]
  }'
```

### Search ClinicalImpressions

```bash
# By patient
curl "http://localhost:8080/baseR4/ClinicalImpression?patient=Patient/patient-1"

# By status
curl "http://localhost:8080/baseR4/ClinicalImpression?status=completed"

# By assessor
curl "http://localhost:8080/baseR4/ClinicalImpression?assessor=Practitioner/doc-1"
```

## Status Codes

| Code | Description |
|------|-------------|
| in-progress | Assessment is ongoing |
| completed | Assessment is complete |
| entered-in-error | Entry was made in error |

## Prognosis Codes

| Code | Display |
|------|---------|
| 170968001 | Prognosis good |
| 170969009 | Prognosis guarded |
| 170970005 | Prognosis poor |
| 65872000 | Prognosis uncertain |
