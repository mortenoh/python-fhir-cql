# OperationDefinition

## Overview

The OperationDefinition resource defines an operation or a named query that can be invoked on a FHIR server. It describes the inputs, outputs, and behavior of the operation.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/operationdefinition.html](https://hl7.org/fhir/R4/operationdefinition.html)

## Maturity Level

**Normative** - This resource is part of the normative FHIR specification.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `url` | uri | Canonical identifier |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `title` | string | Human-friendly name |
| `status` | code | draft \| active \| retired \| unknown (required) |
| `kind` | code | operation \| query (required) |
| `date` | dateTime | Date published |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `code` | code | Invocation name (required) |
| `resource` | code[] | Resource types |
| `system` | boolean | System-level invocation (required) |
| `type` | boolean | Type-level invocation (required) |
| `instance` | boolean | Instance-level invocation (required) |
| `inputProfile` | canonical | Profile for input |
| `outputProfile` | canonical | Profile for output |
| `parameter` | BackboneElement[] | Operation parameters |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=op-001` |
| `url` | uri | Canonical URL | `url=http://example.org/op` |
| `name` | string | Name | `name=validate` |
| `title` | string | Title | `title=Validate` |
| `status` | token | Status | `status=active` |
| `code` | token | Operation code | `code=validate` |
| `kind` | token | Kind | `kind=operation` |
| `system` | token | System level | `system=true` |
| `type` | token | Type level | `type=true` |
| `instance` | token | Instance level | `instance=true` |
| `date` | date | Publication date | `date=ge2024-01-01` |
| `publisher` | string | Publisher | `publisher=HL7` |

## Examples

### Create an OperationDefinition

```bash
curl -X POST http://localhost:8080/baseR4/OperationDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "OperationDefinition",
    "url": "http://example.org/fhir/OperationDefinition/custom-validate",
    "name": "CustomValidate",
    "title": "Custom Validation Operation",
    "status": "active",
    "kind": "operation",
    "code": "custom-validate",
    "resource": ["Patient", "Observation"],
    "system": false,
    "type": true,
    "instance": true,
    "parameter": [
      {
        "name": "resource",
        "use": "in",
        "min": 1,
        "max": "1",
        "type": "Resource"
      },
      {
        "name": "return",
        "use": "out",
        "min": 1,
        "max": "1",
        "type": "OperationOutcome"
      }
    ]
  }'
```

### Search OperationDefinitions

```bash
# By code
curl "http://localhost:8080/baseR4/OperationDefinition?code=validate"

# Active operations
curl "http://localhost:8080/baseR4/OperationDefinition?status=active"

# System-level operations
curl "http://localhost:8080/baseR4/OperationDefinition?system=true"

# Operations for a specific resource
curl "http://localhost:8080/baseR4/OperationDefinition?resource=Patient"
```

## Generator

The `OperationDefinitionGenerator` creates synthetic OperationDefinition resources.

### Usage

```python
from fhirkit.server.generator import OperationDefinitionGenerator

generator = OperationDefinitionGenerator(seed=42)

# Generate an operation definition
op_def = generator.generate(
    name="CustomOperation",
    code="custom-op",
    kind="operation",
    resource=["Patient"]
)

# Uses built-in examples (validate, expand, etc.)
op_def = generator.generate()
```

## Operation Kinds

| Kind | Description |
|------|-------------|
| operation | Standard RESTful operation |
| query | Named search query |

## Parameter Use Codes

| Use | Description |
|-----|-------------|
| in | Input parameter |
| out | Output parameter |
