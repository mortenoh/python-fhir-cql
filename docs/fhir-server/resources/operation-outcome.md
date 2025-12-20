# OperationOutcome

## Overview

An OperationOutcome represents the outcome of an operation, particularly when the operation resulted in an error or warning. It provides detailed information about what went wrong and how to address the issue.

This resource is returned by FHIR servers when operations fail or when additional information needs to be communicated about the result of an operation.

**Common use cases:**
- Error reporting
- Validation results
- Warning messages
- Operation status details
- Debugging information

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/operationoutcome.html](https://hl7.org/fhir/R4/operationoutcome.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `issue` | BackboneElement[] | Issues (required, at least one) |
| `issue.severity` | code | fatal, error, warning, information |
| `issue.code` | code | Issue type code |
| `issue.details` | CodeableConcept | Additional details |
| `issue.diagnostics` | string | Additional diagnostic information |
| `issue.location` | string[] | Path to element in error |
| `issue.expression` | string[] | FHIRPath to element in error |

## Search Parameters

OperationOutcome is typically not searched directly as it's returned as part of operation responses.

## Examples

### Example Error Response

```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "invalid",
    "details": {
      "text": "Patient name is required"
    },
    "diagnostics": "The 'name' element is required for Patient resources",
    "location": ["Patient.name"],
    "expression": ["Patient.name"]
  }]
}
```

### Example Validation Response

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "required",
      "details": {
        "text": "Missing required element"
      },
      "location": ["Patient.gender"]
    },
    {
      "severity": "warning",
      "code": "informational",
      "details": {
        "text": "Birth date is in the future"
      },
      "location": ["Patient.birthDate"]
    }
  ]
}
```

### Create an OperationOutcome

```bash
curl -X POST http://localhost:8080/baseR4/OperationOutcome \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "OperationOutcome",
    "issue": [{
      "severity": "information",
      "code": "informational",
      "details": {
        "text": "Operation completed successfully"
      }
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import OperationOutcomeGenerator

generator = OperationOutcomeGenerator(seed=42)

# Generate a random operation outcome
outcome = generator.generate()

# Generate an error outcome
error_outcome = generator.generate(
    severity="error",
    code="invalid"
)

# Generate batch
outcomes = generator.generate_batch(count=10)
```

## Severity Codes

| Code | Description |
|------|-------------|
| fatal | Fatal error - operation could not complete |
| error | Error - operation failed but may be retried |
| warning | Warning - operation succeeded with caution |
| information | Informational message |

## Issue Type Codes

| Code | Description |
|------|-------------|
| invalid | Invalid content |
| structure | Structural issue |
| required | Required element missing |
| value | Invalid value |
| invariant | Validation rule failed |
| security | Security issue |
| login | Login required |
| unknown | Unknown issue |
| expired | Content expired |
| forbidden | Forbidden |
| suppressed | Information suppressed |
| processing | Processing error |
| not-supported | Not supported |
| duplicate | Duplicate content |
| multiple-matches | Multiple matches found |
| not-found | Not found |
| deleted | Deleted |
| too-long | Content too long |
| code-invalid | Invalid code |
| extension | Extension error |
| too-costly | Operation too costly |
| business-rule | Business rule violation |
| conflict | Conflict |
| transient | Transient error |
| lock-error | Lock error |
| no-store | Storage not available |
| exception | Exception |
| timeout | Timeout |
| incomplete | Incomplete results |
| throttled | Throttled |
| informational | Informational |

## Related Resources

OperationOutcome is typically returned as part of other operation responses rather than being related to specific resources.
