# RequestGroup

## Overview

The RequestGroup resource represents a group of related requests, typically used for order sets or protocols. It allows bundling multiple requests (medication orders, lab orders, procedure requests) that should be performed together.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/requestgroup.html](https://hl7.org/fhir/R4/requestgroup.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `instantiatesCanonical` | canonical[] | Protocol being instantiated |
| `instantiatesUri` | uri[] | External protocols |
| `basedOn` | Reference[] | Fulfills plan/proposal |
| `replaces` | Reference(RequestGroup)[] | Request(s) replaced |
| `groupIdentifier` | Identifier | Composite request ID |
| `status` | code | draft, active, on-hold, revoked, completed, entered-in-error, unknown |
| `intent` | code | proposal, plan, directive, order, etc. |
| `priority` | code | routine, urgent, asap, stat |
| `code` | CodeableConcept | Order set code |
| `subject` | Reference(Patient) | Patient |
| `encounter` | Reference(Encounter) | Encounter context |
| `authoredOn` | dateTime | When created |
| `author` | Reference(Practitioner) | Who created |
| `reasonCode` | CodeableConcept[] | Why |
| `reasonReference` | Reference[] | Why references |
| `note` | Annotation[] | Notes |
| `action` | BackboneElement[] | Actions in the group |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=rg-001` |
| `identifier` | token | Business identifier | `identifier=RG-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `status` | token | Group status | `status=active` |
| `intent` | token | Group intent | `intent=order` |
| `priority` | token | Request priority | `priority=urgent` |
| `code` | token | Order set code | `code=sepsis-bundle` |
| `authored` | date | When authored | `authored=ge2024-01-01` |
| `author` | reference | Author | `author=Practitioner/789` |
| `encounter` | reference | Encounter | `encounter=Encounter/456` |

## Examples

### Create a RequestGroup

```bash
curl -X POST http://localhost:8080/baseR4/RequestGroup \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "RequestGroup",
    "status": "active",
    "intent": "order",
    "priority": "urgent",
    "code": {
      "coding": [{
        "system": "http://example.org/orderset",
        "code": "sepsis-bundle",
        "display": "Sepsis Management Bundle"
      }],
      "text": "Sepsis Management Bundle"
    },
    "subject": {
      "reference": "Patient/patient-001"
    },
    "encounter": {
      "reference": "Encounter/encounter-001"
    },
    "authoredOn": "2024-06-15T10:00:00Z",
    "author": {
      "reference": "Practitioner/practitioner-001"
    },
    "action": [
      {
        "prefix": "1",
        "title": "Initial Assessment",
        "description": "Perform initial patient assessment",
        "priority": "stat"
      },
      {
        "prefix": "2",
        "title": "Lab Orders",
        "description": "Order lactate, blood cultures, CBC",
        "resource": {"reference": "ServiceRequest/sr-001"}
      },
      {
        "prefix": "3",
        "title": "Fluid Resuscitation",
        "description": "Administer 30mL/kg crystalloid",
        "resource": {"reference": "MedicationRequest/mr-001"}
      }
    ]
  }'
```

### Search RequestGroups

```bash
# By patient
curl "http://localhost:8080/baseR4/RequestGroup?patient=Patient/123"

# By status
curl "http://localhost:8080/baseR4/RequestGroup?status=active"

# By intent
curl "http://localhost:8080/baseR4/RequestGroup?intent=order"

# By order set code
curl "http://localhost:8080/baseR4/RequestGroup?code=sepsis-bundle"
```

### Patient Compartment

```bash
# Get all request groups for a patient
curl "http://localhost:8080/baseR4/Patient/123/RequestGroup"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| draft | Draft | Being prepared |
| active | Active | Currently active |
| on-hold | On Hold | Suspended |
| revoked | Revoked | Cancelled |
| completed | Completed | All actions done |
| entered-in-error | Entered in Error | Data entry error |
| unknown | Unknown | Status unknown |

## Intent Codes

| Code | Display | Description |
|------|---------|-------------|
| proposal | Proposal | Suggestion |
| plan | Plan | Planned action |
| directive | Directive | Directive to perform |
| order | Order | Formal order |
| original-order | Original Order | Initial order |
| reflex-order | Reflex Order | Auto-generated order |
| filler-order | Filler Order | Order by filler |
| instance-order | Instance Order | Instance of order |
| option | Option | One of several options |

## Common Order Sets

| Code | Display |
|------|---------|
| sepsis-bundle | Sepsis Management Bundle |
| diabetes-care-bundle | Diabetes Care Bundle |
| cardiac-workup | Cardiac Workup Order Set |
| preop-clearance | Pre-operative Clearance |
| admission-orders | Admission Order Set |
| discharge-bundle | Discharge Order Bundle |

## Selection Behaviors

| Code | Display | Description |
|------|---------|-------------|
| any | Any | Any action can be selected |
| all | All | All actions must be performed |
| all-or-none | All or None | All or none |
| exactly-one | Exactly One | Exactly one must be selected |
| at-most-one | At Most One | At most one can be selected |
| one-or-more | One or More | At least one required |
