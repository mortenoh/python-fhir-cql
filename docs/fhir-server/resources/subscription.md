# Subscription

## Overview

The Subscription resource defines a push-based subscription from a server to another system. It allows clients to be notified when resources matching specific criteria are created or updated.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/subscription.html](https://hl7.org/fhir/R4/subscription.html)

## Maturity Level

**FMM 3** - This resource is considered stable for trial use.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | requested \| active \| error \| off (required) |
| `contact` | ContactPoint[] | Contact details for source |
| `end` | instant | When subscription expires |
| `reason` | string | Description of why subscription exists (required) |
| `criteria` | string | Search query for triggering (required) |
| `error` | string | Error message if status is error |
| `channel` | BackboneElement | Notification channel (required) |
| `channel.type` | code | rest-hook \| websocket \| email \| sms \| message |
| `channel.endpoint` | url | Notification endpoint |
| `channel.payload` | code | MIME type for payload |
| `channel.header` | string[] | HTTP headers for rest-hook |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=sub-001` |
| `status` | token | Subscription status | `status=active` |
| `type` | token | Channel type | `type=rest-hook` |
| `url` | uri | Endpoint URL | `url=https://example.org/notify` |
| `payload` | token | Payload MIME type | `payload=application/fhir+json` |
| `criteria` | string | Search criteria | `criteria=Observation` |
| `contact` | token | Contact details | `contact=email` |

## Examples

### Create a REST Hook Subscription

```bash
curl -X POST http://localhost:8080/baseR4/Subscription \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Subscription",
    "status": "requested",
    "reason": "Monitor critical lab results",
    "criteria": "Observation?code=http://loinc.org|85354-9&value-quantity=gt140",
    "channel": {
      "type": "rest-hook",
      "endpoint": "https://alerts.hospital.org/fhir/notify",
      "payload": "application/fhir+json",
      "header": [
        "Authorization: Bearer abc123"
      ]
    }
  }'
```

### Create a WebSocket Subscription

```bash
curl -X POST http://localhost:8080/baseR4/Subscription \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Subscription",
    "status": "requested",
    "reason": "Real-time patient monitoring",
    "criteria": "Observation?category=vital-signs",
    "channel": {
      "type": "websocket",
      "payload": "application/fhir+json"
    }
  }'
```

### Search Subscriptions

```bash
# Active subscriptions
curl "http://localhost:8080/baseR4/Subscription?status=active"

# REST hook subscriptions
curl "http://localhost:8080/baseR4/Subscription?type=rest-hook"

# By criteria
curl "http://localhost:8080/baseR4/Subscription?criteria=Observation"

# Error state subscriptions
curl "http://localhost:8080/baseR4/Subscription?status=error"
```

## Generator

The `SubscriptionGenerator` creates synthetic Subscription resources.

### Usage

```python
from fhirkit.server.generator import SubscriptionGenerator

generator = SubscriptionGenerator(seed=42)

# Generate a subscription
sub = generator.generate(
    criteria="Observation?code=http://loinc.org|85354-9",
    channel_type="rest-hook",
    endpoint="https://example.org/notify"
)

# Generate REST hook subscription
sub = generator.generate_rest_hook(
    criteria="Condition?clinical-status=active",
    endpoint="https://example.org/conditions"
)

# Generate WebSocket subscription
sub = generator.generate_websocket(
    criteria="Encounter?status=in-progress"
)
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| requested | Requested | Client has requested subscription |
| active | Active | Subscription is active and sending notifications |
| error | Error | Delivery has failed |
| off | Off | Subscription has been turned off |

## Channel Types

| Type | Description |
|------|-------------|
| rest-hook | HTTP POST to endpoint |
| websocket | WebSocket PING message |
| email | Email notification |
| sms | SMS text message |
| message | FHIR message to endpoint |
