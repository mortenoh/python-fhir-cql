# MessageHeader

## Overview

The MessageHeader resource is the header for a message exchange as defined in the FHIR messaging paradigm. It carries the metadata about the message including the event type, source, destination, and any focus resources.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/messageheader.html](https://hl7.org/fhir/R4/messageheader.html)

## Maturity Level

**FMM 4** - This resource is considered mature and stable.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata including versionId and lastUpdated |
| `eventCoding` | Coding | Code for the event this message represents |
| `eventUri` | uri | Alternative: URI for the event |
| `destination` | BackboneElement[] | Message destination(s) |
| `destination.name` | string | Name of destination system |
| `destination.target` | Reference(Device) | Particular delivery destination |
| `destination.endpoint` | url | Actual destination address (required) |
| `destination.receiver` | Reference | Intended receiver |
| `sender` | Reference(Practitioner\|Organization) | Real world sender |
| `enterer` | Reference(Practitioner) | Person who entered data |
| `author` | Reference(Practitioner) | Author of message content |
| `source` | BackboneElement | Message source application (required) |
| `source.name` | string | Name of source system |
| `source.software` | string | Software running the system |
| `source.version` | string | Version of software |
| `source.contact` | ContactPoint | Contact for source system |
| `source.endpoint` | url | Actual message source address (required) |
| `responsible` | Reference | Final responsibility for event |
| `reason` | CodeableConcept | Reason for event |
| `response` | BackboneElement | Response to message |
| `response.identifier` | id | ID of original message |
| `response.code` | code | ok \| transient-error \| fatal-error |
| `response.details` | Reference(OperationOutcome) | Specific details of error |
| `focus` | Reference[] | Focus resources for this message |
| `definition` | canonical | Link to message definition |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=msg-001` |
| `event` | token | Event type code | `event=admin-notify` |
| `source` | string | Source system name | `source=Hospital%20EHR` |
| `source-uri` | uri | Source endpoint | `source-uri=http://example.org/fhir` |
| `destination` | string | Destination name | `destination=Lab%20System` |
| `destination-uri` | uri | Destination endpoint | `destination-uri=http://lab.org/fhir` |
| `sender` | reference | Sender reference | `sender=Organization/123` |
| `author` | reference | Author reference | `author=Practitioner/456` |
| `enterer` | reference | Data enterer | `enterer=Practitioner/789` |
| `responsible` | reference | Responsible party | `responsible=Organization/123` |
| `focus` | reference | Focus resources | `focus=Patient/123` |
| `target` | reference | Destination device | `target=Device/001` |
| `receiver` | reference | Message receiver | `receiver=Organization/lab` |
| `response-id` | token | Original message ID | `response-id=original-msg-001` |
| `code` | token | Response code | `code=ok` |

## Examples

### Create a MessageHeader

```bash
curl -X POST http://localhost:8080/baseR4/MessageHeader \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MessageHeader",
    "eventCoding": {
      "system": "http://terminology.hl7.org/CodeSystem/message-events",
      "code": "admin-notify",
      "display": "Admin Notify"
    },
    "source": {
      "name": "Hospital EHR System",
      "software": "HealthCare EHR",
      "version": "3.1.2",
      "contact": {
        "system": "email",
        "value": "support@hospital.org"
      },
      "endpoint": "http://hospital.org/fhir/messaging"
    },
    "destination": [{
      "name": "Lab System",
      "endpoint": "http://lab.org/fhir/messaging"
    }],
    "sender": {
      "reference": "Organization/hospital-001"
    },
    "focus": [{
      "reference": "Patient/patient-001"
    }],
    "reason": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/message-reasons-encounter",
        "code": "admit",
        "display": "Admit"
      }]
    }
  }'
```

### Create a Response Message

```bash
curl -X POST http://localhost:8080/baseR4/MessageHeader \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MessageHeader",
    "eventCoding": {
      "system": "http://terminology.hl7.org/CodeSystem/message-events",
      "code": "admin-notify",
      "display": "Admin Notify"
    },
    "source": {
      "name": "Lab System",
      "endpoint": "http://lab.org/fhir/messaging"
    },
    "response": {
      "identifier": "original-message-id",
      "code": "ok"
    }
  }'
```

### Search MessageHeaders

```bash
# By event type
curl "http://localhost:8080/baseR4/MessageHeader?event=admin-notify"

# By source endpoint
curl "http://localhost:8080/baseR4/MessageHeader?source-uri=http://hospital.org/fhir"

# By sender
curl "http://localhost:8080/baseR4/MessageHeader?sender=Organization/hospital-001"

# Response messages
curl "http://localhost:8080/baseR4/MessageHeader?response-id=original-msg-001"

# Successful responses
curl "http://localhost:8080/baseR4/MessageHeader?code=ok"
```

## Generator

The `MessageHeaderGenerator` creates synthetic MessageHeader resources with:

- Various message event types
- Realistic source and destination endpoints
- Response messages with appropriate codes

### Usage

```python
from fhirkit.server.generator import MessageHeaderGenerator

generator = MessageHeaderGenerator(seed=42)

# Generate a message header
message = generator.generate(
    source_endpoint="http://hospital.org/fhir/messaging",
    destination_endpoint="http://lab.org/fhir/messaging",
    sender_ref="Organization/hospital-001",
    focus_refs=["Patient/patient-001"]
)

# Generate a response message
response = generator.generate_response(
    original_message_id="original-msg-001",
    response_code="ok"
)

# Generate with specific event
message = generator.generate(
    event_code="diagnosticreport-provide",
    focus_refs=["DiagnosticReport/report-001"]
)
```

## Message Events

Common event codes from `http://terminology.hl7.org/CodeSystem/message-events`:

| Code | Display |
|------|---------|
| admin-notify | Admin Notify |
| diagnosticreport-provide | Provide a DiagnosticReport |
| observation-provide | Provide an Observation |
| patient-link | Patient Link |
| patient-unlink | Patient Unlink |
| valueset-expand | ValueSet Expand |

## Response Codes

| Code | Display | Description |
|------|---------|-------------|
| ok | OK | Message processed successfully |
| transient-error | Transient Error | Temporary error, retry may succeed |
| fatal-error | Fatal Error | Permanent error, do not retry |
