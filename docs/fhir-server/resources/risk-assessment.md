# RiskAssessment

## Overview

The RiskAssessment resource captures the outcome of a clinical evaluation of the patient's risk for certain outcomes. Common uses include cardiovascular risk scores, fall risk assessments, and cancer screening.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/riskassessment.html](https://hl7.org/fhir/R4/riskassessment.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | registered, preliminary, final, amended, corrected, cancelled, entered-in-error, unknown |
| `subject` | Reference(Patient) | Who/what the assessment is about |
| `encounter` | Reference(Encounter) | Related encounter |
| `occurrenceDateTime` | dateTime | When assessment was made |
| `condition` | Reference(Condition) | Condition being assessed |
| `performer` | Reference | Who did the assessment |
| `basis` | Reference[] | Information used for assessment |
| `prediction` | BackboneElement[] | Risk predictions |
| `mitigation` | string | Recommended mitigations |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=risk-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `date` | date | Assessment date | `date=2024-01-15` |
| `condition` | reference | Related condition | `condition=Condition/hypertension-1` |
| `performer` | reference | Who performed | `performer=Practitioner/doc-1` |
| `method` | token | Assessment method | `method=framingham` |

## Examples

### Create a RiskAssessment

```bash
curl -X POST http://localhost:8080/baseR4/RiskAssessment \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "RiskAssessment",
    "status": "final",
    "subject": {"reference": "Patient/patient-1"},
    "occurrenceDateTime": "2024-01-15T12:00:00Z",
    "condition": {"reference": "Condition/hypertension-1"},
    "performer": {"reference": "Practitioner/doc-1"},
    "basis": [
      {"reference": "Observation/blood-pressure-1"},
      {"reference": "Observation/cholesterol-1"},
      {"reference": "FamilyMemberHistory/fmh-1"}
    ],
    "prediction": [{
      "outcome": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "22298006",
          "display": "Myocardial infarction"
        }]
      },
      "probabilityDecimal": 0.15,
      "whenRange": {
        "low": {"value": 0, "unit": "years"},
        "high": {"value": 10, "unit": "years"}
      },
      "rationale": "Framingham Risk Score calculation"
    }],
    "mitigation": "Maintain blood pressure control, consider statin therapy"
  }'
```

### Search RiskAssessments

```bash
# By patient
curl "http://localhost:8080/baseR4/RiskAssessment?patient=Patient/patient-1"

# By condition
curl "http://localhost:8080/baseR4/RiskAssessment?condition=Condition/hypertension-1"

# By date
curl "http://localhost:8080/baseR4/RiskAssessment?date=2024-01-15"
```

## Common Risk Assessments

| Assessment | Outcome | Description |
|------------|---------|-------------|
| Framingham | Cardiovascular event | 10-year heart disease risk |
| CHADS2 | Stroke | Stroke risk in atrial fibrillation |
| Morse Fall Scale | Fall | Fall risk in hospitalized patients |
| FRAX | Fracture | 10-year fracture probability |
| PHQ-9 | Depression | Depression severity screening |

## Status Codes

| Code | Description |
|------|-------------|
| registered | Assessment recorded |
| preliminary | Preliminary results |
| final | Final results |
| amended | Amended results |
| corrected | Corrected results |
| cancelled | Assessment cancelled |
| entered-in-error | Entry was made in error |
| unknown | Status unknown |
