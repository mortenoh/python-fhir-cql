# ResearchSubject

## Overview

The ResearchSubject resource describes a patient's participation in a clinical trial or research study. It links the patient to the study and tracks their enrollment status and assigned study arm.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/researchsubject.html](https://hl7.org/fhir/R4/researchsubject.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | Subject status |
| `period` | Period | Participation period |
| `study` | Reference(ResearchStudy) | Research study |
| `individual` | Reference(Patient) | Patient participant |
| `assignedArm` | string | Arm subject was assigned to |
| `actualArm` | string | Arm subject is actually in |
| `consent` | Reference(Consent) | Study consent |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=rsub-001` |
| `identifier` | token | Business identifier | `identifier=SUBJ-1234` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `individual` | reference | Individual reference | `individual=Patient/123` |
| `status` | token | Subject status | `status=on-study` |
| `study` | reference | Study reference | `study=ResearchStudy/rs-001` |
| `date` | date | Participation period | `date=ge2024-01-01` |

## Examples

### Create a ResearchSubject

```bash
curl -X POST http://localhost:8080/baseR4/ResearchSubject \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ResearchSubject",
    "identifier": [{
      "system": "http://example.org/research-subject-ids",
      "value": "SUBJ-1234"
    }],
    "status": "on-study",
    "period": {
      "start": "2024-06-15"
    },
    "study": {
      "reference": "ResearchStudy/rs-001"
    },
    "individual": {
      "reference": "Patient/patient-001"
    },
    "assignedArm": "Treatment Arm",
    "actualArm": "Treatment Arm",
    "consent": {
      "reference": "Consent/consent-001"
    }
  }'
```

### Create a Withdrawn Subject

```bash
curl -X POST http://localhost:8080/baseR4/ResearchSubject \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ResearchSubject",
    "identifier": [{
      "system": "http://example.org/research-subject-ids",
      "value": "SUBJ-5678"
    }],
    "status": "withdrawn",
    "period": {
      "start": "2024-01-15",
      "end": "2024-04-01"
    },
    "study": {
      "reference": "ResearchStudy/rs-001"
    },
    "individual": {
      "reference": "Patient/patient-002"
    },
    "assignedArm": "Control Arm",
    "actualArm": "Control Arm"
  }'
```

### Search ResearchSubjects

```bash
# By patient
curl "http://localhost:8080/baseR4/ResearchSubject?patient=Patient/123"

# By study
curl "http://localhost:8080/baseR4/ResearchSubject?study=ResearchStudy/rs-001"

# By status
curl "http://localhost:8080/baseR4/ResearchSubject?status=on-study"

# Active subjects in a study
curl "http://localhost:8080/baseR4/ResearchSubject?study=ResearchStudy/rs-001&status=on-study"
```

### Patient Compartment

```bash
# Get all research participation for a patient
curl "http://localhost:8080/baseR4/Patient/123/ResearchSubject"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| candidate | Candidate | Subject is a candidate |
| eligible | Eligible | Subject is eligible |
| follow-up | Follow Up | Subject is in follow-up |
| ineligible | Ineligible | Subject is not eligible |
| not-registered | Not Registered | Not registered |
| off-study | Off Study | No longer participating |
| on-study | On Study | Actively participating |
| on-study-intervention | On Study Intervention | Receiving intervention |
| on-study-observation | On Study Observation | Under observation |
| pending-on-study | Pending On Study | Pending enrollment |
| potential-candidate | Potential Candidate | May be a candidate |
| screening | Screening | Being screened |
| withdrawn | Withdrawn | Subject withdrew |

## Common Study Arms

| Name | Description |
|------|-------------|
| Treatment Arm | Receives experimental intervention |
| Control Arm | Control group (standard care or placebo) |
| Arm A | First study arm |
| Arm B | Second study arm |
| Placebo | Receives placebo |
| Active Control | Receives active comparator |

## Usage Notes

### Tracking Arm Crossover

When a subject crosses over to a different study arm:

```json
{
  "resourceType": "ResearchSubject",
  "status": "on-study-intervention",
  "assignedArm": "Arm A",
  "actualArm": "Arm B"
}
```

### Subject Lifecycle

1. **candidate** - Patient identified as potential participant
2. **screening** - Undergoing screening procedures
3. **eligible/ineligible** - Eligibility determination
4. **pending-on-study** - Awaiting enrollment
5. **on-study** - Enrolled and participating
6. **on-study-intervention** - Receiving study intervention
7. **on-study-observation** - Observation phase
8. **follow-up** - Post-intervention follow-up
9. **off-study** - Completed participation
10. **withdrawn** - Subject withdrew from study
