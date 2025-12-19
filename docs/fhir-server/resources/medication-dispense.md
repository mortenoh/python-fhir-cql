# MedicationDispense

## Overview

The MedicationDispense resource indicates that a medication product is to be or has been dispensed for a patient. It tracks the actual dispensing event, including the quantity dispensed and any substitutions made.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/medicationdispense.html](https://hl7.org/fhir/R4/medicationdispense.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata including versionId and lastUpdated |
| `status` | code | preparation, in-progress, cancelled, on-hold, completed, entered-in-error, stopped, declined, unknown |
| `medicationCodeableConcept` | CodeableConcept | Medication code |
| `medicationReference` | Reference(Medication) | Reference to Medication resource |
| `subject` | Reference(Patient) | Who the dispense is for |
| `performer` | BackboneElement[] | Who performed the dispense |
| `authorizingPrescription` | Reference(MedicationRequest)[] | Prescription authorizing dispense |
| `quantity` | SimpleQuantity | Amount dispensed |
| `daysSupply` | SimpleQuantity | Days of supply |
| `whenPrepared` | dateTime | When product was packaged |
| `whenHandedOver` | dateTime | When product was given out |
| `dosageInstruction` | Dosage[] | How the medication is to be used |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=meddispense-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Dispense status | `status=completed` |
| `code` | token | Medication code | `code=http://rxnorm\|617314` |
| `performer` | reference | Who dispensed | `performer=Practitioner/pharmacist-1` |
| `prescription` | reference | Authorizing prescription | `prescription=MedicationRequest/rx-1` |
| `whenhandedover` | date | When handed over | `whenhandedover=2024-01-15` |
| `whenprepared` | date | When prepared | `whenprepared=2024-01-15` |

## Examples

### Create a MedicationDispense

```bash
curl -X POST http://localhost:8080/baseR4/MedicationDispense \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MedicationDispense",
    "status": "completed",
    "medicationCodeableConcept": {
      "coding": [{
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "617314",
        "display": "Metformin 500 MG Oral Tablet"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "performer": [{
      "actor": {"reference": "Practitioner/pharmacist-1"}
    }],
    "authorizingPrescription": [
      {"reference": "MedicationRequest/medrequest-1"}
    ],
    "quantity": {
      "value": 60,
      "unit": "tablets"
    },
    "daysSupply": {
      "value": 30,
      "unit": "days"
    },
    "whenHandedOver": "2024-01-15T14:00:00Z"
  }'
```

### Search MedicationDispenses

```bash
# By patient
curl "http://localhost:8080/baseR4/MedicationDispense?patient=Patient/patient-1"

# By status
curl "http://localhost:8080/baseR4/MedicationDispense?status=completed"

# By prescription
curl "http://localhost:8080/baseR4/MedicationDispense?prescription=MedicationRequest/rx-1"
```

## Generator

The `MedicationDispenseGenerator` creates synthetic MedicationDispense resources.

### Usage

```python
from fhirkit.server.generator import MedicationDispenseGenerator

generator = MedicationDispenseGenerator(seed=42)
dispense = generator.generate(
    patient_id="patient-1",
    pharmacist_id="pharmacist-1"
)
```

## Status Codes

| Code | Description |
|------|-------------|
| preparation | Being prepared |
| in-progress | In progress |
| cancelled | Cancelled |
| on-hold | Paused |
| completed | Dispensing complete |
| entered-in-error | Entry was made in error |
| stopped | Stopped before completion |
| declined | Not dispensed |
| unknown | Status unknown |
