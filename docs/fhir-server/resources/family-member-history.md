# FamilyMemberHistory

## Overview

The FamilyMemberHistory resource records significant health conditions for a person related to the patient, relevant for genetic disorders, family-linked conditions, and risk assessment.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/familymemberhistory.html](https://hl7.org/fhir/R4/familymemberhistory.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | partial, completed, entered-in-error, health-unknown |
| `patient` | Reference(Patient) | Patient whose family member this is about |
| `date` | dateTime | When history was recorded |
| `relationship` | CodeableConcept | Relationship to patient (mother, father, etc.) |
| `sex` | CodeableConcept | Sex of family member |
| `bornDate` | date | Birth date of family member |
| `deceasedBoolean` | boolean | Whether family member is deceased |
| `deceasedAge` | Age | Age at death |
| `condition` | BackboneElement[] | Health conditions |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=fmh-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `status` | token | Record status | `status=completed` |
| `relationship` | token | Relationship type | `relationship=FTH` |
| `date` | date | When recorded | `date=2024-01-08` |
| `code` | token | Condition code | `code=http://snomed.info/sct\|22298006` |

## Examples

### Create a FamilyMemberHistory

```bash
curl -X POST http://localhost:8080/baseR4/FamilyMemberHistory \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "FamilyMemberHistory",
    "status": "completed",
    "patient": {"reference": "Patient/patient-1"},
    "date": "2024-01-08",
    "relationship": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
        "code": "FTH",
        "display": "father"
      }]
    },
    "sex": {
      "coding": [{
        "system": "http://hl7.org/fhir/administrative-gender",
        "code": "male"
      }]
    },
    "deceasedAge": {
      "value": 72,
      "unit": "years"
    },
    "condition": [{
      "code": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "22298006",
          "display": "Myocardial infarction"
        }]
      },
      "contributedToDeath": true,
      "onsetAge": {
        "value": 72,
        "unit": "years"
      }
    }]
  }'
```

### Search FamilyMemberHistory

```bash
# By patient
curl "http://localhost:8080/baseR4/FamilyMemberHistory?patient=Patient/patient-1"

# By relationship
curl "http://localhost:8080/baseR4/FamilyMemberHistory?relationship=FTH"

# By condition
curl "http://localhost:8080/baseR4/FamilyMemberHistory?code=http://snomed.info/sct|22298006"
```

## Relationship Codes

| Code | Display |
|------|---------|
| FTH | Father |
| MTH | Mother |
| SIB | Sibling |
| BRO | Brother |
| SIS | Sister |
| GRPRN | Grandparent |
| GRMTH | Grandmother |
| GRFTH | Grandfather |
| UNCLE | Uncle |
| AUNT | Aunt |
| CHILD | Child |
| SON | Son |
| DAU | Daughter |

## Status Codes

| Code | Description |
|------|-------------|
| partial | Information is incomplete |
| completed | Complete history |
| entered-in-error | Entry was made in error |
| health-unknown | Health status unknown |
