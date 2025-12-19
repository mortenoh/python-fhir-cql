# Audit Logging

## Overview

The FHIR server supports automatic audit logging for all CRUD operations. When enabled, every create, read, update, and delete operation automatically creates an AuditEvent resource that records:

- **Who**: The client IP address and User-Agent
- **What**: The resource type and ID being accessed
- **When**: Timestamp of the operation
- **Action**: Create (C), Read (R), Update (U), or Delete (D)
- **Outcome**: Success (0) or failure codes (4, 8, 12)
- **Patient**: Automatically extracted patient reference when available

## Configuration

Enable audit logging via environment variables or settings:

```bash
# Enable audit logging
export FHIR_SERVER_ENABLE_AUDIT=true

# Exclude read operations to reduce noise (default: true)
export FHIR_SERVER_AUDIT_EXCLUDE_READS=true
```

Or in code:

```python
from fhirkit.server.config import FHIRServerSettings

settings = FHIRServerSettings(
    enable_audit=True,
    audit_exclude_reads=True,  # Don't log reads
)
```

## AuditEvent Structure

Each AuditEvent follows the FHIR R4 AuditEvent specification:

```json
{
  "resourceType": "AuditEvent",
  "id": "audit-123",
  "type": {
    "system": "http://terminology.hl7.org/CodeSystem/audit-event-type",
    "code": "rest",
    "display": "RESTful Operation"
  },
  "subtype": [{
    "system": "http://hl7.org/fhir/restful-interaction",
    "code": "create",
    "display": "create"
  }],
  "action": "C",
  "recorded": "2024-01-15T10:30:00Z",
  "outcome": "0",
  "agent": [{
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
        "code": "IRCP",
        "display": "information recipient"
      }]
    },
    "who": {
      "display": "Mozilla/5.0..."
    },
    "network": {
      "address": "192.168.1.100",
      "type": "2"
    },
    "requestor": true
  }],
  "source": {
    "observer": {"display": "FHIR Server"},
    "type": [{
      "system": "http://terminology.hl7.org/CodeSystem/security-source-type",
      "code": "4",
      "display": "Application Server"
    }]
  },
  "entity": [
    {
      "what": {"reference": "Patient/123"},
      "type": {
        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
        "code": "1",
        "display": "Person"
      },
      "role": {
        "system": "http://terminology.hl7.org/CodeSystem/object-role",
        "code": "1",
        "display": "Patient"
      }
    },
    {
      "what": {"reference": "Observation/456"},
      "type": {
        "system": "http://terminology.hl7.org/CodeSystem/audit-entity-type",
        "code": "2",
        "display": "System Object"
      },
      "name": "Observation"
    }
  ]
}
```

## Querying Audit Events

### REST API

```bash
# Get all audit events
curl "http://localhost:8080/baseR4/AuditEvent"

# Filter by action (C=create, R=read, U=update, D=delete)
curl "http://localhost:8080/baseR4/AuditEvent?action=C"

# Filter by outcome (0=success, 4=minor failure, 8=serious, 12=major)
curl "http://localhost:8080/baseR4/AuditEvent?outcome=0"

# Filter by date range
curl "http://localhost:8080/baseR4/AuditEvent?date=ge2024-01-01"

# Filter by patient
curl "http://localhost:8080/baseR4/AuditEvent?patient=Patient/123"

# Filter by entity (any resource)
curl "http://localhost:8080/baseR4/AuditEvent?entity=Observation/456"
```

### GraphQL

```graphql
{
  auditEvents(action: "C", outcome: "0", _count: 10) {
    id
    data
  }
}
```

## Supported Operations

Audit events are created for:

| Operation | Action Code | Subtype |
|-----------|-------------|---------|
| Create (POST) | C | create |
| Read (GET by ID) | R | read |
| Update (PUT) | U | update |
| Delete (DELETE) | D | delete |
| Patch (PATCH) | U | update |

## Patient Reference Extraction

The audit service automatically extracts patient references from resources. It checks these fields in order:

1. If the resource is a Patient, uses its ID
2. `patient` field
3. `subject` field
4. `individual` field
5. `beneficiary` field
6. `for` field

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=audit-123` |
| `action` | token | Action code | `action=C` |
| `date` | date | Recorded date | `date=ge2024-01-01` |
| `outcome` | token | Outcome code | `outcome=0` |
| `type` | token | Event type | `type=rest` |
| `subtype` | token | Event subtype | `subtype=create` |
| `patient` | reference | Patient entity | `patient=Patient/123` |
| `agent` | reference | Agent reference | `agent=Practitioner/456` |
| `entity` | reference | Entity reference | `entity=Observation/789` |

## Performance Considerations

- **Exclude reads**: By default, read operations are not logged to reduce storage and improve performance. Set `audit_exclude_reads=False` to log all operations.
- **Async logging**: Audit events are created synchronously but designed to be lightweight.
- **AuditEvent operations are not audited**: To prevent infinite loops, operations on AuditEvent resources themselves are not logged.

## Security Best Practices

1. **Protect audit logs**: Consider restricting access to AuditEvent resources
2. **Retention policy**: Implement a retention policy for old audit events
3. **Monitoring**: Set up alerts for failed operations (outcome != 0)
4. **Compliance**: Use audit logs for HIPAA, GDPR, and other compliance requirements
