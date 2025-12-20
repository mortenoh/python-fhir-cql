# TestReport

## Overview

A TestReport contains the results of executing a TestScript against a FHIR server. It records the outcome of each test, including successes, failures, and any error messages.

This resource provides detailed information about test execution for quality assurance, debugging, and compliance verification.

**Common use cases:**
- Test result documentation
- Quality assurance reporting
- Compliance verification
- Debugging failed tests
- Continuous integration results

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/testreport.html](https://hl7.org/fhir/R4/testreport.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier | Business identifier |
| `name` | string | Report name |
| `status` | code | completed, in-progress, waiting, stopped, entered-in-error |
| `testScript` | Reference(TestScript) | Test script executed |
| `result` | code | pass, fail, pending |
| `score` | decimal | Overall score (0-100) |
| `tester` | string | Name of tester |
| `issued` | dateTime | When the report was issued |
| `participant` | BackboneElement[] | Systems involved |
| `setup` | BackboneElement | Setup results |
| `test` | BackboneElement[] | Test results |
| `teardown` | BackboneElement | Teardown results |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=report-001` |
| `identifier` | token | Business identifier | `identifier=RPT-12345` |
| `testscript` | reference | TestScript reference | `testscript=TestScript/test-001` |
| `result` | token | Test result | `result=pass` |
| `issued` | date | Issue date | `issued=2024-01-15` |
| `tester` | string | Tester name | `tester=QA%20Team` |

## Examples

### Create a TestReport

```bash
curl -X POST http://localhost:8080/baseR4/TestReport \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "TestReport",
    "identifier": {
      "system": "http://example.org/reports",
      "value": "RPT-2024-001"
    },
    "name": "Patient CRUD Test Results",
    "status": "completed",
    "testScript": {"reference": "TestScript/patient-crud-test"},
    "result": "pass",
    "score": 100.0,
    "tester": "Automated Test Runner",
    "issued": "2024-01-15T15:30:00Z",
    "test": [{
      "name": "Create Patient",
      "action": [{
        "operation": {
          "result": "pass",
          "message": "Patient created successfully"
        }
      }, {
        "assert": {
          "result": "pass"
        }
      }]
    }]
  }'
```

### Search TestReports

```bash
# By result
curl "http://localhost:8080/baseR4/TestReport?result=pass"

# By test script
curl "http://localhost:8080/baseR4/TestReport?testscript=TestScript/patient-crud-test"

# By date
curl "http://localhost:8080/baseR4/TestReport?issued=ge2024-01-01"
```

## Generator Usage

```python
from fhirkit.server.generator import TestReportGenerator

generator = TestReportGenerator(seed=42)

# Generate a random test report
report = generator.generate()

# Generate a passing report
pass_report = generator.generate(
    result="pass",
    status="completed"
)

# Generate batch
reports = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| completed | Report is complete |
| in-progress | Tests are still running |
| waiting | Waiting for input |
| stopped | Testing was stopped |
| entered-in-error | Entered in error |

## Result Codes

| Code | Description |
|------|-------------|
| pass | All tests passed |
| fail | One or more tests failed |
| pending | Tests are pending |

## Related Resources

- [TestScript](./test-script.md) - The test script that was executed
- [CapabilityStatement](./capability-statement.md) - Server being tested
