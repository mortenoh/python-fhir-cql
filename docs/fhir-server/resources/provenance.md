# Provenance

## Overview

The Provenance resource tracks information about the creation, modification, and transmission of healthcare data. It provides an audit trail showing who, what, when, where, why, and how for any FHIR resource.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/provenance.html](https://hl7.org/fhir/R4/provenance.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `target` | Reference[] | Resources this provenance relates to |
| `occurredDateTime` | dateTime | When the activity occurred |
| `occurredPeriod` | Period | Period of activity |
| `recorded` | instant | When provenance was recorded |
| `policy` | uri[] | Policy or plan the activity was defined by |
| `location` | Reference(Location) | Where the activity occurred |
| `reason` | CodeableConcept[] | Reason the activity occurred |
| `activity` | CodeableConcept | Activity that occurred |
| `agent` | BackboneElement[] | Actor(s) involved |
| `entity` | BackboneElement[] | Source entities |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=prov-001` |
| `target` | reference | Target resources | `target=Observation/obs-1` |
| `recorded` | date | When recorded | `recorded=2024-01-15` |
| `agent` | reference | Agent involved | `agent=Practitioner/nurse-1` |
| `location` | reference | Where occurred | `location=Location/ward-1` |
| `when` | date | When occurred | `when=2024-01-15` |

## Examples

### Create a Provenance

```bash
curl -X POST http://localhost:8080/baseR4/Provenance \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Provenance",
    "target": [
      {"reference": "Observation/blood-pressure-1"}
    ],
    "occurredDateTime": "2024-01-15T13:45:00Z",
    "recorded": "2024-01-15T14:00:00Z",
    "policy": ["http://hospital.example.org/policies/data-entry"],
    "location": {"reference": "Location/ward-3a"},
    "reason": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
        "code": "TREAT",
        "display": "treatment"
      }]
    }],
    "activity": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
        "code": "CREATE",
        "display": "create"
      }]
    },
    "agent": [{
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
          "code": "author",
          "display": "Author"
        }]
      },
      "who": {"reference": "Practitioner/nurse-1"},
      "onBehalfOf": {"reference": "Organization/hospital-1"}
    }],
    "entity": [{
      "role": "source",
      "what": {"reference": "Device/bp-monitor-1"}
    }]
  }'
```

### Search Provenance

```bash
# By target resource
curl "http://localhost:8080/baseR4/Provenance?target=Observation/obs-1"

# By agent
curl "http://localhost:8080/baseR4/Provenance?agent=Practitioner/nurse-1"

# By date
curl "http://localhost:8080/baseR4/Provenance?recorded=2024-01-15"
```

## Activity Codes

| Code | Display | Description |
|------|---------|-------------|
| CREATE | Create | Data was created |
| UPDATE | Update | Data was updated |
| DELETE | Delete | Data was deleted |
| APPEND | Append | Data was appended |
| NULLIFY | Nullify | Data was nullified |

## Agent Types

| Code | Display |
|------|---------|
| author | Author |
| performer | Performer |
| verifier | Verifier |
| legal | Legal |
| attester | Attester |
| informant | Informant |
| enterer | Enterer |
| custodian | Custodian |
| assembler | Assembler |

## Entity Roles

| Code | Description |
|------|-------------|
| derivation | A transformation of an entity |
| revision | A derivation for which the resulting entity is a revised version |
| quotation | The repeat of an entity from a source |
| source | A primary source for a topic |
| removal | An entity that is removed from the target |
