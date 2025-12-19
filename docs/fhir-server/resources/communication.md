# Communication

## Overview

The Communication resource represents a conveyance of information from one entity to another. It can record messages between healthcare providers, from providers to patients, or system notifications.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/communication.html](https://hl7.org/fhir/R4/communication.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | preparation, in-progress, not-done, on-hold, stopped, completed, entered-in-error, unknown |
| `category` | CodeableConcept[] | Message category |
| `priority` | code | routine, urgent, asap, stat |
| `subject` | Reference(Patient) | Focus of message |
| `encounter` | Reference(Encounter) | Related encounter |
| `sent` | dateTime | When sent |
| `received` | dateTime | When received |
| `recipient` | Reference[] | Message recipients |
| `sender` | Reference | Message sender |
| `payload` | BackboneElement[] | Message content |
| `about` | Reference[] | Resources this relates to |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=comm-001` |
| `patient` | reference | Patient subject | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Message status | `status=completed` |
| `sent` | date | When sent | `sent=2024-01-15` |
| `received` | date | When received | `received=2024-01-15` |
| `sender` | reference | Sender | `sender=Organization/lab-1` |
| `recipient` | reference | Recipient | `recipient=Practitioner/doc-1` |
| `category` | token | Message category | `category=notification` |

## Examples

### Create a Communication

```bash
curl -X POST http://localhost:8080/baseR4/Communication \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Communication",
    "status": "completed",
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/communication-category",
        "code": "notification",
        "display": "Notification"
      }]
    }],
    "priority": "routine",
    "subject": {"reference": "Patient/patient-1"},
    "sent": "2024-01-15T15:30:00Z",
    "received": "2024-01-15T16:00:00Z",
    "recipient": [
      {"reference": "Practitioner/doc-1"}
    ],
    "sender": {"reference": "Organization/lab-1"},
    "payload": [{
      "contentString": "Lab results for patient are now available. HbA1c: 7.2%"
    }],
    "about": [
      {"reference": "DiagnosticReport/hba1c-1"}
    ]
  }'
```

### Search Communications

```bash
# By patient
curl "http://localhost:8080/baseR4/Communication?patient=Patient/patient-1"

# By status
curl "http://localhost:8080/baseR4/Communication?status=completed"

# By sender
curl "http://localhost:8080/baseR4/Communication?sender=Organization/lab-1"
```

## Communication Categories

| Code | Display | Description |
|------|---------|-------------|
| alert | Alert | Urgent alert |
| notification | Notification | General notification |
| reminder | Reminder | Reminder message |
| instruction | Instruction | Instructions |

## Status Codes

| Code | Description |
|------|-------------|
| preparation | Being prepared |
| in-progress | In progress |
| not-done | Not done |
| on-hold | On hold |
| stopped | Stopped |
| completed | Completed |
| entered-in-error | Entry was made in error |
| unknown | Unknown |

## Priority Codes

| Code | Description |
|------|-------------|
| routine | Routine priority |
| urgent | Urgent priority |
| asap | As soon as possible |
| stat | Immediately |
