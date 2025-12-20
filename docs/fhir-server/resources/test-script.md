# TestScript

## Overview

A TestScript defines a series of tests that can be executed to verify FHIR server behavior. It describes a set of operations and assertions that test specific functionality and expected outcomes.

This resource is used for automated testing, conformance testing, and quality assurance of FHIR implementations.

**Common use cases:**
- Automated testing
- Conformance verification
- Regression testing
- Implementation validation
- Integration testing

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/testscript.html](https://hl7.org/fhir/R4/testscript.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical URL |
| `identifier` | Identifier | Business identifier |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown |
| `date` | dateTime | Date published |
| `publisher` | string | Publisher name |
| `description` | markdown | Description |
| `fixture` | BackboneElement[] | Test fixtures |
| `variable` | BackboneElement[] | Variables for the test |
| `setup` | BackboneElement | Setup operations |
| `test` | BackboneElement[] | Test definitions |
| `teardown` | BackboneElement | Teardown operations |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=test-001` |
| `url` | uri | Canonical URL | `url=http://example.org/tests/patient-crud` |
| `name` | string | Name | `name=PatientCRUD` |
| `status` | token | Status | `status=active` |
| `identifier` | token | Business identifier | `identifier=TEST-12345` |

## Examples

### Create a TestScript

```bash
curl -X POST http://localhost:8080/baseR4/TestScript \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "TestScript",
    "url": "http://example.org/fhir/TestScript/patient-crud-test",
    "name": "PatientCRUDTest",
    "title": "Patient CRUD Operations Test",
    "status": "active",
    "date": "2024-01-15",
    "description": "Tests basic CRUD operations for Patient resources",
    "fixture": [{
      "id": "patient-fixture",
      "autocreate": false,
      "autodelete": false,
      "resource": {
        "reference": "Patient/test-patient"
      }
    }],
    "test": [{
      "name": "Create Patient",
      "description": "Test creating a new patient",
      "action": [{
        "operation": {
          "type": {"code": "create"},
          "resource": "Patient",
          "sourceId": "patient-fixture"
        }
      }, {
        "assert": {
          "response": "created"
        }
      }]
    }]
  }'
```

### Search TestScripts

```bash
# By status
curl "http://localhost:8080/baseR4/TestScript?status=active"

# By name
curl "http://localhost:8080/baseR4/TestScript?name=PatientCRUD"
```

## Generator Usage

```python
from fhirkit.server.generator import TestScriptGenerator

generator = TestScriptGenerator(seed=42)

# Generate a random test script
script = generator.generate()

# Generate with specific name
patient_test = generator.generate(
    name="PatientTest",
    status="active"
)

# Generate batch
scripts = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| draft | Test script is in development |
| active | Test script is ready for use |
| retired | Test script is no longer active |
| unknown | Status is unknown |

## Related Resources

- [TestReport](./test-report.md) - Results of running the test script
- [CapabilityStatement](./capability-statement.md) - Server capabilities being tested
