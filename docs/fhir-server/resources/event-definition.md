# EventDefinition

## Overview

An EventDefinition defines when a specific event occurs, such as when data meets certain criteria. It provides a declarative way to specify event triggers for clinical decision support and workflow automation.

This resource is essential for event-driven architectures and clinical alerting systems.

**Common use cases:**
- Clinical alert triggers
- Workflow event definition
- Subscription criteria
- Quality measure triggers
- Decision support events

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/eventdefinition.html](https://hl7.org/fhir/R4/eventdefinition.html)

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
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `purpose` | markdown | Purpose of the event definition |
| `usage` | string | How to use the event |
| `trigger` | TriggerDefinition[] | Event triggers (required) |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=high-glucose-alert` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/EventDefinition/glucose` |
| `status` | token | Status | `status=active` |
| `name` | string | Name | `name=HighGlucoseEvent` |

## Examples

### Create an EventDefinition

```bash
curl -X POST http://localhost:8080/baseR4/EventDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "EventDefinition",
    "url": "http://example.org/fhir/EventDefinition/high-glucose",
    "name": "HighGlucoseEvent",
    "title": "High Blood Glucose Alert",
    "status": "active",
    "description": "Triggers when blood glucose exceeds 300 mg/dL",
    "purpose": "Alert clinicians to dangerously high glucose levels",
    "trigger": [{
      "type": "data-changed",
      "name": "high-glucose",
      "data": [{
        "type": "Observation",
        "codeFilter": [{
          "path": "code",
          "code": [{
            "system": "http://loinc.org",
            "code": "2339-0",
            "display": "Glucose [Mass/volume] in Blood"
          }]
        }],
        "dateFilter": [{
          "path": "effectiveDateTime",
          "searchParam": "date"
        }]
      }],
      "condition": {
        "description": "Glucose > 300 mg/dL",
        "language": "text/fhirpath",
        "expression": "value.ofType(Quantity).value > 300"
      }
    }]
  }'
```

### Search EventDefinitions

```bash
# By status
curl "http://localhost:8080/baseR4/EventDefinition?status=active"

# By name
curl "http://localhost:8080/baseR4/EventDefinition?name:contains=glucose"
```

## Generator Usage

```python
from fhirkit.server.generator import EventDefinitionGenerator

generator = EventDefinitionGenerator(seed=42)

# Generate random event definition
event = generator.generate()

# Generate with specific status
active_event = generator.generate(status="active")

# Generate batch
events = generator.generate_batch(count=10)
```

## Trigger Types

| Type | Description |
|------|-------------|
| named-event | Named event |
| periodic | Periodic trigger |
| data-changed | Data change trigger |
| data-accessed | Data access trigger |
| data-access-ended | Data access ended |

## Related Resources

- [Subscription](./subscription.md) - Subscriptions using events
- [Library](./library.md) - Logic libraries
- [PlanDefinition](./plan-definition.md) - Plans triggered by events
