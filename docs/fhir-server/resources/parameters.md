# Parameters

## Overview

The Parameters resource is used to pass parameters into and receive results from FHIR operations. It is a special resource that acts as a container for operation inputs and outputs.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/parameters.html](https://hl7.org/fhir/R4/parameters.html)

## Maturity Level

**Normative** - This resource is part of the normative FHIR specification.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `parameter` | BackboneElement[] | Operation parameters |
| `parameter.name` | string | Parameter name |
| `parameter.value[x]` | * | Parameter value (various types) |
| `parameter.resource` | Resource | Whole resource value |
| `parameter.part` | BackboneElement[] | Nested parameters |

## Value Types

The `value[x]` element supports many types:
- `valueString`, `valueBoolean`, `valueInteger`, `valueDecimal`
- `valueUri`, `valueUrl`, `valueCode`
- `valueDate`, `valueDateTime`, `valueTime`, `valueInstant`
- `valueCodeableConcept`, `valueCoding`, `valueIdentifier`
- `valueReference`, `valuePeriod`, `valueQuantity`
- And more...

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=params-001` |

## Examples

### Operation Input Parameters

```bash
# $validate operation input
curl -X POST http://localhost:8080/baseR4/Patient/\$validate \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Parameters",
    "parameter": [
      {
        "name": "resource",
        "resource": {
          "resourceType": "Patient",
          "name": [{"family": "Smith", "given": ["John"]}]
        }
      },
      {
        "name": "mode",
        "valueCode": "create"
      }
    ]
  }'
```

### Operation Output Parameters

```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "return",
      "resource": {
        "resourceType": "OperationOutcome",
        "issue": [
          {
            "severity": "information",
            "code": "informational",
            "diagnostics": "Validation successful"
          }
        ]
      }
    }
  ]
}
```

### Nested Parameters

```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "coding",
      "part": [
        {
          "name": "system",
          "valueUri": "http://snomed.info/sct"
        },
        {
          "name": "code",
          "valueCode": "73211009"
        }
      ]
    }
  ]
}
```

## Generator

The `ParametersGenerator` creates synthetic Parameters resources.

### Usage

```python
from fhirkit.server.generator import ParametersGenerator

generator = ParametersGenerator(seed=42)

# Generate from a dictionary
params = generator.generate_with_values({
    "code": "validate",
    "mode": "create",
    "profile": "http://example.org/profile"
})

# Generate operation input
params = generator.generate_operation_input(
    operation_code="validate",
    resource=patient_resource,
    mode="create"
)

# Generate operation output
params = generator.generate_operation_output(
    result=operation_outcome,
    success=True
)
```

## Common Uses

1. **Operation inputs**: Passing parameters to $validate, $expand, $translate, etc.
2. **Operation outputs**: Receiving results from operations
3. **Batch parameters**: Complex parameter structures for batch operations
4. **Nested data**: Hierarchical parameter structures using `part`
