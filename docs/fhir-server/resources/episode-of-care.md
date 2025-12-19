# EpisodeOfCare

## Overview

The EpisodeOfCare resource represents a period of healthcare provided by an organization for a specific condition or set of conditions. It is commonly used for chronic disease management, mental health programs, or coordinated care for complex patients.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/episodeofcare.html](https://hl7.org/fhir/R4/episodeofcare.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | planned, waitlist, active, onhold, finished, cancelled, entered-in-error |
| `statusHistory` | BackboneElement[] | Status history |
| `type` | CodeableConcept[] | Type of episode |
| `diagnosis` | BackboneElement[] | Diagnoses relevant to episode |
| `patient` | Reference(Patient) | Patient |
| `managingOrganization` | Reference(Organization) | Organization responsible |
| `period` | Period | Episode time period |
| `referralRequest` | Reference(ServiceRequest)[] | Referrals |
| `careManager` | Reference(Practitioner) | Care manager |
| `team` | Reference(CareTeam)[] | Care teams |
| `account` | Reference(Account)[] | Billing accounts |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=eoc-001` |
| `identifier` | token | Business identifier | `identifier=EOC-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `status` | token | Episode status | `status=active` |
| `type` | token | Episode type | `type=hacc` |
| `date` | date | Episode period | `date=ge2024-01-01` |
| `organization` | reference | Managing organization | `organization=Organization/456` |
| `care-manager` | reference | Care manager | `care-manager=Practitioner/789` |
| `condition` | reference | Diagnosis condition | `condition=Condition/cond-001` |

## Examples

### Create an EpisodeOfCare

```bash
curl -X POST http://localhost:8080/baseR4/EpisodeOfCare \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "EpisodeOfCare",
    "status": "active",
    "type": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        "code": "hacc",
        "display": "Home and Community Care"
      }]
    }],
    "patient": {
      "reference": "Patient/patient-001"
    },
    "managingOrganization": {
      "reference": "Organization/organization-001"
    },
    "period": {
      "start": "2024-01-15"
    },
    "diagnosis": [{
      "condition": {
        "reference": "Condition/condition-001"
      },
      "role": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role",
          "code": "CC",
          "display": "Chief complaint"
        }]
      },
      "rank": 1
    }],
    "careManager": {
      "reference": "Practitioner/practitioner-001"
    }
  }'
```

### Search EpisodeOfCare

```bash
# By patient
curl "http://localhost:8080/baseR4/EpisodeOfCare?patient=Patient/123"

# By status
curl "http://localhost:8080/baseR4/EpisodeOfCare?status=active"

# By type
curl "http://localhost:8080/baseR4/EpisodeOfCare?type=hacc"

# Active episodes in date range
curl "http://localhost:8080/baseR4/EpisodeOfCare?status=active&date=ge2024-01-01"
```

### Patient Compartment

```bash
# Get all episodes for a patient
curl "http://localhost:8080/baseR4/Patient/123/EpisodeOfCare"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| planned | Planned | Episode is planned |
| waitlist | Waitlist | Patient is on waitlist |
| active | Active | Episode is active |
| onhold | On Hold | Episode is on hold |
| finished | Finished | Episode is complete |
| cancelled | Cancelled | Episode was cancelled |
| entered-in-error | Entered in Error | Data entry error |

## Episode Types

| Code | Display |
|------|---------|
| hacc | Home and Community Care |
| pac | Post Acute Care |
| diab | Diabetes Management |
| da | Drug and Alcohol |
| cm | Care Management |
