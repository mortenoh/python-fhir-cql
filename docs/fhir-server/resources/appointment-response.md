# AppointmentResponse

## Overview

The AppointmentResponse resource is used to accept or decline a request to participate in an Appointment. It provides a reply from a participant indicating their participation status and any proposed changes to the appointment timing.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/appointmentresponse.html](https://hl7.org/fhir/R4/appointmentresponse.html)

## Maturity Level

**FMM 3** - This resource is considered stable for trial use.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata including versionId and lastUpdated |
| `identifier` | Identifier[] | Business identifiers |
| `appointment` | Reference(Appointment) | Appointment being responded to (required) |
| `start` | instant | Proposed start time |
| `end` | instant | Proposed end time |
| `participantType` | CodeableConcept[] | Role of participant |
| `actor` | Reference | Person/device/location responding |
| `participantStatus` | code | Participation status (required) |
| `comment` | string | Additional comments |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=resp-001` |
| `identifier` | token | Business identifier | `identifier=APRESP-123` |
| `appointment` | reference | Appointment reference | `appointment=Appointment/apt-001` |
| `actor` | reference | Responding actor | `actor=Practitioner/prac-001` |
| `patient` | reference | Patient responder | `patient=Patient/123` |
| `practitioner` | reference | Practitioner responder | `practitioner=Practitioner/456` |
| `location` | reference | Location responder | `location=Location/loc-001` |
| `part-status` | token | Participation status | `part-status=accepted` |

## Examples

### Create an AppointmentResponse (Accept)

```bash
curl -X POST http://localhost:8080/baseR4/AppointmentResponse \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "AppointmentResponse",
    "appointment": {
      "reference": "Appointment/apt-001"
    },
    "actor": {
      "reference": "Practitioner/prac-001",
      "display": "Dr. Smith"
    },
    "participantType": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
        "code": "ATND",
        "display": "attender"
      }]
    }],
    "participantStatus": "accepted",
    "comment": "I will be there"
  }'
```

### Create an AppointmentResponse (Decline)

```bash
curl -X POST http://localhost:8080/baseR4/AppointmentResponse \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "AppointmentResponse",
    "appointment": {
      "reference": "Appointment/apt-001"
    },
    "actor": {
      "reference": "Practitioner/prac-002"
    },
    "participantStatus": "declined",
    "comment": "Unable to attend due to scheduling conflict"
  }'
```

### Create an AppointmentResponse with Proposed Time

```bash
curl -X POST http://localhost:8080/baseR4/AppointmentResponse \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "AppointmentResponse",
    "appointment": {
      "reference": "Appointment/apt-001"
    },
    "actor": {
      "reference": "Practitioner/prac-001"
    },
    "start": "2024-02-15T14:00:00Z",
    "end": "2024-02-15T14:30:00Z",
    "participantStatus": "tentative",
    "comment": "I can do this time instead"
  }'
```

### Search AppointmentResponses

```bash
# By appointment
curl "http://localhost:8080/baseR4/AppointmentResponse?appointment=Appointment/apt-001"

# By status
curl "http://localhost:8080/baseR4/AppointmentResponse?part-status=accepted"

# By practitioner
curl "http://localhost:8080/baseR4/AppointmentResponse?practitioner=Practitioner/prac-001"

# Declined responses
curl "http://localhost:8080/baseR4/AppointmentResponse?part-status=declined"
```

## Generator

The `AppointmentResponseGenerator` creates synthetic AppointmentResponse resources with:

- Various participation statuses
- Appropriate participant types
- Realistic comments based on status

### Usage

```python
from fhirkit.server.generator import AppointmentResponseGenerator

generator = AppointmentResponseGenerator(seed=42)

# Generate a response
response = generator.generate(
    appointment_ref="Appointment/apt-001",
    actor_ref="Practitioner/prac-001",
    participant_status="accepted"
)

# Generate responses for multiple actors
responses = generator.generate_for_appointment(
    appointment_ref="Appointment/apt-001",
    actor_refs=["Practitioner/prac-001", "Patient/patient-001"],
    participant_status="accepted"
)

# Generate batch
responses = generator.generate_batch(
    count=5,
    appointment_ref="Appointment/apt-001"
)
```

## Participant Status Codes

| Code | Display | Description |
|------|---------|-------------|
| accepted | Accepted | Participant has accepted |
| declined | Declined | Participant has declined |
| tentative | Tentative | Participant is tentative |
| needs-action | Needs Action | Participant needs to indicate acceptance |

## Participant Type Codes

Common codes from `http://terminology.hl7.org/CodeSystem/v3-ParticipationType`:

| Code | Display |
|------|---------|
| ATND | attender |
| PPRF | primary performer |
| SPRF | secondary performer |
| LOC | location |
