# MedicationAdministration

## Overview

The MedicationAdministration resource describes the event of a patient consuming or otherwise being administered a medication. It captures when, what, how, and by whom the medication was given, including the dosage.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/medicationadministration.html](https://hl7.org/fhir/R4/medicationadministration.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata including versionId and lastUpdated |
| `status` | code | in-progress, not-done, on-hold, completed, entered-in-error, stopped, unknown |
| `medicationCodeableConcept` | CodeableConcept | Medication code (RxNorm) |
| `medicationReference` | Reference(Medication) | Reference to Medication resource |
| `subject` | Reference(Patient) | Who received the medication |
| `context` | Reference(Encounter) | Encounter during which administered |
| `effectiveDateTime` | dateTime | When the medication was given |
| `effectivePeriod` | Period | Time period of administration |
| `performer` | BackboneElement[] | Who administered the medication |
| `dosage` | BackboneElement | Details of how medication was taken |
| `request` | Reference(MedicationRequest) | Request this fulfills |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=medadmin-001` |
| `patient` | reference | Patient who received medication | `patient=Patient/123` |
| `subject` | reference | Subject (alias for patient) | `subject=Patient/123` |
| `status` | token | Administration status | `status=completed` |
| `code` | token | Medication code | `code=http://rxnorm\|1049502` |
| `effective-time` | date | Time of administration | `effective-time=2024-01-15` |
| `performer` | reference | Who administered | `performer=Practitioner/456` |
| `request` | reference | Related MedicationRequest | `request=MedicationRequest/789` |
| `context` | reference | Encounter context | `context=Encounter/enc-1` |

## Examples

### Create a MedicationAdministration

```bash
curl -X POST http://localhost:8080/baseR4/MedicationAdministration \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MedicationAdministration",
    "status": "completed",
    "medicationCodeableConcept": {
      "coding": [{
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "1049502",
        "display": "Acetaminophen 325 MG Oral Tablet"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "effectiveDateTime": "2024-01-15T08:00:00Z",
    "performer": [{
      "actor": {"reference": "Practitioner/nurse-1"}
    }],
    "dosage": {
      "dose": {
        "value": 650,
        "unit": "mg",
        "system": "http://unitsofmeasure.org",
        "code": "mg"
      }
    }
  }'
```

### Search MedicationAdministrations

```bash
# By patient
curl "http://localhost:8080/baseR4/MedicationAdministration?patient=Patient/patient-1"

# By status
curl "http://localhost:8080/baseR4/MedicationAdministration?status=completed"

# By date
curl "http://localhost:8080/baseR4/MedicationAdministration?effective-time=2024-01-15"
```

## Generator

The `MedicationAdministrationGenerator` creates synthetic MedicationAdministration resources.

### Usage

```python
from fhirkit.server.generator import MedicationAdministrationGenerator

generator = MedicationAdministrationGenerator(seed=42)
admin = generator.generate(
    patient_id="patient-1",
    performer_id="practitioner-1"
)
```

## Status Codes

| Code | Description |
|------|-------------|
| in-progress | Administration is in progress |
| not-done | Administration was not performed |
| on-hold | Administration is paused |
| completed | Administration is complete |
| entered-in-error | Entry was made in error |
| stopped | Administration was stopped before completion |
| unknown | Status is unknown |
