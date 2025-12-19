# AuditEvent

## Overview

The AuditEvent resource captures security audit logging events. It records who accessed what data, when, and from where. Essential for HIPAA compliance and security monitoring.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/auditevent.html](https://hl7.org/fhir/R4/auditevent.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `type` | Coding | Type of event (DICOM) |
| `subtype` | Coding[] | More specific type |
| `action` | code | C (Create), R (Read), U (Update), D (Delete), E (Execute) |
| `period` | Period | When the activity occurred |
| `recorded` | instant | When the event was recorded |
| `outcome` | code | 0 (Success), 4 (Minor failure), 8 (Serious failure), 12 (Major failure) |
| `outcomeDesc` | string | Description of the outcome |
| `agent` | BackboneElement[] | Actor involved in the event |
| `source` | BackboneElement | Audit event reporter |
| `entity` | BackboneElement[] | Data or resources accessed |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=ae-001` |
| `action` | token | Action type | `action=R` |
| `date` | date | When recorded | `date=2024-01-15` |
| `type` | token | Event type | `type=110110` |
| `agent` | reference | Who was involved | `agent=Practitioner/doc-1` |
| `entity` | reference | What was accessed | `entity=Patient/patient-1` |
| `outcome` | token | Event outcome | `outcome=0` |
| `site` | token | Source site | `site=Hospital` |

## Examples

### Create an AuditEvent

```bash
curl -X POST http://localhost:8080/baseR4/AuditEvent \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "AuditEvent",
    "type": {
      "system": "http://dicom.nema.org/resources/ontology/DCM",
      "code": "110110",
      "display": "Patient Record"
    },
    "subtype": [{
      "system": "http://hl7.org/fhir/restful-interaction",
      "code": "read",
      "display": "read"
    }],
    "action": "R",
    "recorded": "2024-01-15T10:05:01Z",
    "outcome": "0",
    "outcomeDesc": "Success",
    "agent": [{
      "who": {"reference": "Practitioner/doc-1"},
      "altId": "doc1",
      "name": "Dr. Sarah Johnson",
      "requestor": true,
      "network": {
        "address": "192.168.1.100",
        "type": "2"
      }
    }],
    "source": {
      "site": "Hospital EMR",
      "observer": {"display": "FHIR Server"},
      "type": [{
        "system": "http://terminology.hl7.org/CodeSystem/security-source-type",
        "code": "4",
        "display": "Application Server"
      }]
    },
    "entity": [{
      "what": {"reference": "Patient/patient-1"},
      "type": {
        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
        "code": "1",
        "display": "Person"
      }
    }]
  }'
```

### Search AuditEvents

```bash
# By action
curl "http://localhost:8080/baseR4/AuditEvent?action=R"

# By date
curl "http://localhost:8080/baseR4/AuditEvent?date=2024-01-15"

# By agent
curl "http://localhost:8080/baseR4/AuditEvent?agent=Practitioner/doc-1"

# By entity accessed
curl "http://localhost:8080/baseR4/AuditEvent?entity=Patient/patient-1"
```

## Event Types (DICOM)

| Code | Display | Description |
|------|---------|-------------|
| 110110 | Patient Record | Patient record access |
| 110112 | Query | Query/search operation |
| 110114 | User Authentication | Login/logout |
| 110106 | Export | Data export |
| 110107 | Import | Data import |

## Action Codes

| Code | Description |
|------|-------------|
| C | Create |
| R | Read/View/Print |
| U | Update |
| D | Delete |
| E | Execute |

## Outcome Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 4 | Minor failure |
| 8 | Serious failure |
| 12 | Major failure |
