# MessageDefinition

## Overview

A MessageDefinition defines the characteristics of a message that can be shared between systems, including what events trigger the message, what focus resources are included, and what response is expected.

This resource is essential for implementing FHIR messaging patterns and defining message-based integrations.

**Common use cases:**
- Message contract definition
- Event-based integration
- System interoperability
- Workflow orchestration
- Notification patterns

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/messagedefinition.html](https://hl7.org/fhir/R4/messagedefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `identifier` | Identifier[] | Business identifiers |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed (required) |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `event[x]` | Coding or uri | Event that triggers the message (required) |
| `category` | code | consequence, currency, notification |
| `focus` | BackboneElement[] | Resources included in message |
| `responseRequired` | code | always, on-error, never, on-success |
| `allowedResponse` | BackboneElement[] | Allowed response types |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=admission-notification` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/MessageDefinition/admission` |
| `name` | string | Computer-friendly name | `name=AdmissionNotification` |
| `status` | token | Status | `status=active` |
| `event` | token | Event code | `event=admit-inpatient` |
| `category` | token | Message category | `category=notification` |

## Examples

### Create a MessageDefinition

```bash
curl -X POST http://localhost:8080/baseR4/MessageDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MessageDefinition",
    "url": "http://example.org/fhir/MessageDefinition/patient-admission",
    "name": "PatientAdmissionNotification",
    "title": "Patient Admission Notification",
    "status": "active",
    "date": "2024-01-15",
    "eventCoding": {
      "system": "http://example.org/events",
      "code": "patient-admit"
    },
    "category": "notification",
    "focus": [{
      "code": "Encounter",
      "profile": "http://hl7.org/fhir/StructureDefinition/Encounter",
      "min": 1,
      "max": "1"
    }, {
      "code": "Patient",
      "min": 1,
      "max": "1"
    }],
    "responseRequired": "on-error"
  }'
```

### Search MessageDefinitions

```bash
# By category
curl "http://localhost:8080/baseR4/MessageDefinition?category=notification"

# By status
curl "http://localhost:8080/baseR4/MessageDefinition?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import MessageDefinitionGenerator

generator = MessageDefinitionGenerator(seed=42)

# Generate a random message definition
message = generator.generate()

# Generate notification message
notification = generator.generate(
    category="notification",
    status="active"
)

# Generate batch
messages = generator.generate_batch(count=10)
```

## Category Codes

| Code | Description |
|------|-------------|
| consequence | Message has real-world consequences |
| currency | Message provides updated information |
| notification | Message is a notification only |

## Response Required Codes

| Code | Description |
|------|-------------|
| always | Response always required |
| on-error | Response required on error |
| never | No response required |
| on-success | Response required on success |

## Related Resources

- [MessageHeader](./message-header.md) - Message instances using this definition
- [Bundle](./bundle.md) - Message bundle containing resources
- [CapabilityStatement](./capability-statement.md) - Server messaging capabilities
