# MedicationStatement

## Overview

The MedicationStatement resource captures a record of a medication that is being consumed by a patient. It may be based on patient self-reporting or inferred from prescription records. This is distinct from MedicationAdministration which represents a specific administration event.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/medicationstatement.html](https://hl7.org/fhir/R4/medicationstatement.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata including versionId and lastUpdated |
| `status` | code | active, completed, entered-in-error, intended, stopped, on-hold, unknown, not-taken |
| `medicationCodeableConcept` | CodeableConcept | Medication code |
| `medicationReference` | Reference(Medication) | Reference to Medication |
| `subject` | Reference(Patient) | Who is taking the medication |
| `effectiveDateTime` | dateTime | When medication is/was taken |
| `effectivePeriod` | Period | Period of use |
| `dateAsserted` | dateTime | When the usage was asserted |
| `informationSource` | Reference | Who provided the information |
| `reasonCode` | CodeableConcept[] | Reason for taking |
| `dosage` | Dosage[] | How medication is/was taken |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=medstmt-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Statement status | `status=active` |
| `code` | token | Medication code | `code=http://rxnorm\|197361` |
| `effective` | date | Date of use | `effective=ge2023-01-01` |
| `source` | reference | Information source | `source=Patient/123` |

## Examples

### Create a MedicationStatement

```bash
curl -X POST http://localhost:8080/baseR4/MedicationStatement \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MedicationStatement",
    "status": "active",
    "medicationCodeableConcept": {
      "coding": [{
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "197361",
        "display": "Lisinopril 10 MG Oral Tablet"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "effectivePeriod": {
      "start": "2023-06-01"
    },
    "dateAsserted": "2024-01-10T09:00:00Z",
    "informationSource": {"reference": "Patient/patient-1"},
    "reasonCode": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "38341003",
        "display": "Hypertensive disorder"
      }]
    }],
    "dosage": [{
      "text": "One tablet daily in the morning",
      "doseAndRate": [{
        "doseQuantity": {
          "value": 10,
          "unit": "mg"
        }
      }]
    }]
  }'
```

### Search MedicationStatements

```bash
# By patient
curl "http://localhost:8080/baseR4/MedicationStatement?patient=Patient/patient-1"

# Active medications
curl "http://localhost:8080/baseR4/MedicationStatement?status=active"

# By medication code
curl "http://localhost:8080/baseR4/MedicationStatement?code=http://rxnorm|197361"
```

## Generator

The `MedicationStatementGenerator` creates synthetic MedicationStatement resources.

### Usage

```python
from fhirkit.server.generator import MedicationStatementGenerator

generator = MedicationStatementGenerator(seed=42)
statement = generator.generate(
    patient_id="patient-1"
)
```

## Status Codes

| Code | Description |
|------|-------------|
| active | Currently taking |
| completed | Finished taking |
| entered-in-error | Entry was made in error |
| intended | Intends to take |
| stopped | Stopped taking |
| on-hold | Temporarily paused |
| unknown | Status unknown |
| not-taken | Patient is not taking |
