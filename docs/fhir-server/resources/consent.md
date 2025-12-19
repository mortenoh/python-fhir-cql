# Consent

## Overview

The Consent resource captures a healthcare consumer's choices regarding the disclosure and use of their personal health information. It supports privacy consent, treatment consent, and other regulatory consent types.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/consent.html](https://hl7.org/fhir/R4/consent.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | draft, proposed, active, rejected, inactive, entered-in-error |
| `scope` | CodeableConcept | Which areas this consent covers |
| `category` | CodeableConcept[] | Classification of the consent |
| `patient` | Reference(Patient) | Who the consent is for |
| `dateTime` | dateTime | When consent was granted |
| `performer` | Reference[] | Who gave consent |
| `organization` | Reference(Organization)[] | Custodian organization |
| `policyRule` | CodeableConcept | Regulatory framework |
| `provision` | BackboneElement | Consent provisions |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=consent-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `status` | token | Consent status | `status=active` |
| `date` | date | When consent recorded | `date=2024-01-05` |
| `organization` | reference | Custodian org | `organization=Organization/hosp-1` |
| `scope` | token | Consent scope | `scope=patient-privacy` |
| `category` | token | Category code | `category=http://loinc.org\|59284-0` |

## Examples

### Create a Consent

```bash
curl -X POST http://localhost:8080/baseR4/Consent \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Consent",
    "status": "active",
    "scope": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/consentscope",
        "code": "patient-privacy",
        "display": "Privacy Consent"
      }]
    },
    "category": [{
      "coding": [{
        "system": "http://loinc.org",
        "code": "59284-0",
        "display": "Consent Document"
      }]
    }],
    "patient": {"reference": "Patient/patient-1"},
    "dateTime": "2024-01-05T10:00:00Z",
    "performer": [
      {"reference": "Patient/patient-1"}
    ],
    "organization": [
      {"reference": "Organization/hospital-1"}
    ],
    "policyRule": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "OPTIN",
        "display": "opt-in"
      }]
    },
    "provision": {
      "type": "permit",
      "period": {
        "start": "2024-01-05",
        "end": "2025-01-05"
      }
    }
  }'
```

### Search Consents

```bash
# By patient
curl "http://localhost:8080/baseR4/Consent?patient=Patient/patient-1"

# Active consents
curl "http://localhost:8080/baseR4/Consent?status=active"

# Privacy consents
curl "http://localhost:8080/baseR4/Consent?scope=patient-privacy"
```

## Consent Scopes

| Code | Display | Description |
|------|---------|-------------|
| patient-privacy | Privacy Consent | Privacy and disclosure preferences |
| treatment | Treatment Consent | Consent for treatment |
| research | Research Consent | Consent for research participation |
| adr | Advance Directive | Advance care directive |

## Status Codes

| Code | Description |
|------|-------------|
| draft | Being developed |
| proposed | Proposed but not yet active |
| active | Currently in effect |
| rejected | Consent was rejected |
| inactive | No longer active |
| entered-in-error | Entry was made in error |
