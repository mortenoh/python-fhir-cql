# ExampleScenario

## Overview

An ExampleScenario describes a set of interrelated actors and activities that illustrate a particular workflow or business process. It provides narrative and structured documentation of use cases.

This resource is essential for implementation guide development, workflow documentation, and standards development.

**Common use cases:**
- Workflow documentation
- Use case illustration
- Implementation guidance
- Interoperability testing
- Standards development

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/examplescenario.html](https://hl7.org/fhir/R4/examplescenario.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `identifier` | Identifier[] | Business identifiers |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `purpose` | markdown | Why this example scenario exists |
| `actor` | BackboneElement[] | Actors in the scenario |
| `instance` | BackboneElement[] | Resource instances |
| `process` | BackboneElement[] | Process steps |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=admission-workflow` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/ExampleScenario/admission` |
| `status` | token | Status | `status=active` |
| `name` | string | Name | `name=AdmissionWorkflow` |

## Examples

### Create an ExampleScenario

```bash
curl -X POST http://localhost:8080/baseR4/ExampleScenario \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ExampleScenario",
    "url": "http://example.org/fhir/ExampleScenario/medication-order",
    "name": "MedicationOrderWorkflow",
    "status": "active",
    "description": "Illustrates the medication ordering workflow",
    "purpose": "To demonstrate how medication orders flow through the system",
    "actor": [
      {
        "actorId": "physician",
        "type": "person",
        "name": "Ordering Physician",
        "description": "The physician who orders the medication"
      },
      {
        "actorId": "pharmacy",
        "type": "entity",
        "name": "Pharmacy System",
        "description": "The pharmacy information system"
      },
      {
        "actorId": "ehr",
        "type": "entity",
        "name": "EHR System",
        "description": "The electronic health record system"
      }
    ],
    "instance": [
      {
        "resourceId": "patient-1",
        "resourceType": "Patient",
        "name": "John Smith",
        "description": "The patient receiving the medication"
      },
      {
        "resourceId": "med-request-1",
        "resourceType": "MedicationRequest",
        "name": "Aspirin Order",
        "description": "The medication order for aspirin"
      }
    ],
    "process": [{
      "title": "Order Medication",
      "description": "Process of ordering a medication",
      "step": [
        {
          "process": [{
            "title": "Create Order",
            "description": "Physician creates medication order"
          }]
        },
        {
          "operation": {
            "number": "1",
            "type": "create",
            "name": "Submit Order",
            "description": "Order is submitted to pharmacy",
            "initiator": "physician",
            "receiver": "pharmacy",
            "request": {"resourceId": "med-request-1"}
          }
        }
      ]
    }]
  }'
```

### Search ExampleScenarios

```bash
# By status
curl "http://localhost:8080/baseR4/ExampleScenario?status=active"

# By name
curl "http://localhost:8080/baseR4/ExampleScenario?name:contains=medication"
```

## Generator Usage

```python
from fhirkit.server.generator import ExampleScenarioGenerator

generator = ExampleScenarioGenerator(seed=42)

# Generate random scenario
scenario = generator.generate()

# Generate with specific status
active = generator.generate(status="active")

# Generate batch
scenarios = generator.generate_batch(count=5)
```

## Actor Types

| Type | Description |
|------|-------------|
| person | Human actor |
| entity | System or application |

## Related Resources

- [ImplementationGuide](./implementation-guide.md) - Implementation guides using scenarios
- [StructureDefinition](./structure-definition.md) - Profiles referenced
