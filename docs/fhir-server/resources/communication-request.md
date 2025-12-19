# CommunicationRequest

## Overview

The CommunicationRequest resource represents a request for communication between healthcare providers, between a provider and a patient, or between a patient and their family/contacts. It is used to order notifications, reminders, or other communications.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/communicationrequest.html](https://hl7.org/fhir/R4/communicationrequest.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `basedOn` | Reference[] | Request fulfilled by this request |
| `replaces` | Reference(CommunicationRequest)[] | Request(s) superseded |
| `groupIdentifier` | Identifier | Composite request this is part of |
| `status` | code | draft, active, on-hold, revoked, completed, entered-in-error, unknown |
| `statusReason` | CodeableConcept | Reason for current status |
| `category` | CodeableConcept[] | Communication category |
| `priority` | code | routine, urgent, asap, stat |
| `doNotPerform` | boolean | If true, request NOT to perform |
| `medium` | CodeableConcept[] | How communication should occur |
| `subject` | Reference(Patient) | Focus of message |
| `about` | Reference[] | Resources request is about |
| `encounter` | Reference(Encounter) | Encounter context |
| `payload` | BackboneElement[] | Message content |
| `occurrenceDateTime` | dateTime | When should occur |
| `authoredOn` | dateTime | When request was created |
| `requester` | Reference(Practitioner) | Who requested |
| `recipient` | Reference[] | Recipients |
| `sender` | Reference | Who should send |
| `reasonCode` | CodeableConcept[] | Why |
| `note` | Annotation[] | Notes |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=cr-001` |
| `identifier` | token | Business identifier | `identifier=CR-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `status` | token | Request status | `status=active` |
| `category` | token | Communication category | `category=reminder` |
| `priority` | token | Request priority | `priority=urgent` |
| `authored` | date | When authored | `authored=ge2024-01-01` |
| `requester` | reference | Requester | `requester=Practitioner/789` |
| `recipient` | reference | Recipient | `recipient=Patient/123` |
| `sender` | reference | Sender | `sender=Practitioner/789` |
| `encounter` | reference | Encounter | `encounter=Encounter/456` |

## Examples

### Create a CommunicationRequest

```bash
curl -X POST http://localhost:8080/baseR4/CommunicationRequest \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "CommunicationRequest",
    "status": "active",
    "priority": "routine",
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/communication-category",
        "code": "reminder",
        "display": "Reminder"
      }]
    }],
    "medium": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode",
        "code": "EMAILWRIT",
        "display": "email"
      }]
    }],
    "subject": {
      "reference": "Patient/patient-001"
    },
    "payload": [{
      "contentString": "Reminder: Your annual check-up is scheduled for next week."
    }],
    "occurrenceDateTime": "2024-06-20T09:00:00Z",
    "authoredOn": "2024-06-15T10:00:00Z",
    "requester": {
      "reference": "Practitioner/practitioner-001"
    },
    "recipient": [{
      "reference": "Patient/patient-001"
    }]
  }'
```

### Search CommunicationRequests

```bash
# By patient
curl "http://localhost:8080/baseR4/CommunicationRequest?patient=Patient/123"

# By status
curl "http://localhost:8080/baseR4/CommunicationRequest?status=active"

# By priority
curl "http://localhost:8080/baseR4/CommunicationRequest?priority=urgent"

# By category
curl "http://localhost:8080/baseR4/CommunicationRequest?category=reminder"
```

### Patient Compartment

```bash
# Get all communication requests for a patient
curl "http://localhost:8080/baseR4/Patient/123/CommunicationRequest"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| draft | Draft | Request is being prepared |
| active | Active | Request is active |
| on-hold | On Hold | Request is on hold |
| revoked | Revoked | Request was revoked |
| completed | Completed | Request is complete |
| entered-in-error | Entered in Error | Data entry error |
| unknown | Unknown | Status unknown |

## Priority Codes

| Code | Display | Description |
|------|---------|-------------|
| routine | Routine | Normal priority |
| urgent | Urgent | Needs attention soon |
| asap | ASAP | As soon as possible |
| stat | STAT | Immediately |

## Communication Categories

| Code | Display |
|------|---------|
| alert | Alert |
| notification | Notification |
| reminder | Reminder |
| instruction | Instruction |

## Communication Media

| Code | Display |
|------|---------|
| EMAILWRIT | email |
| WRITTEN | written |
| VERBAL | verbal |
| PHONE | telephone |
| VIDEOCONF | videoconferencing |
