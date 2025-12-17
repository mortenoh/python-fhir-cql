# _contained Search Parameter

## Overview

The `_contained` parameter controls whether contained resources are returned in search results.

## FHIR Specification

- [_contained](https://hl7.org/fhir/R4/search.html#contained) - Control contained resource behavior

## Values

| Value | Description |
|-------|-------------|
| `false` | Do not return contained resources (default behavior) |
| `true` | Return only contained resources from matched container resources |
| `both` | Return both top-level resources and their contained resources |

## Usage

```bash
# Default behavior - only top-level resources
GET /MedicationRequest

# Only contained resources (e.g., contained Medications)
GET /MedicationRequest?_contained=true

# Both top-level and contained resources
GET /MedicationRequest?_contained=both

# Explicitly request no contained resources
GET /MedicationRequest?_contained=false
```

## Response Examples

### Default (`_contained=false`)

Returns only the container resources:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 2,
  "entry": [
    {
      "resource": {
        "resourceType": "MedicationRequest",
        "id": "mr-001",
        "contained": [
          {
            "resourceType": "Medication",
            "id": "med-1",
            "code": {"coding": [{"display": "Aspirin"}]}
          }
        ],
        "medicationReference": {"reference": "#med-1"}
      }
    }
  ]
}
```

### With `_contained=true`

Returns only the contained resources:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [
    {
      "resource": {
        "resourceType": "Medication",
        "id": "med-1",
        "code": {"coding": [{"display": "Aspirin"}]}
      }
    }
  ]
}
```

### With `_contained=both`

Returns both container and contained resources:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 2,
  "entry": [
    {
      "resource": {
        "resourceType": "MedicationRequest",
        "id": "mr-001",
        "contained": [{"resourceType": "Medication", "id": "med-1"}],
        "medicationReference": {"reference": "#med-1"}
      }
    },
    {
      "resource": {
        "resourceType": "Medication",
        "id": "med-1",
        "code": {"coding": [{"display": "Aspirin"}]}
      }
    }
  ]
}
```

## Common Use Cases

### Finding all contained Medications

```bash
curl "http://localhost:8000/MedicationRequest?_contained=true"
```

### Audit all resources including contained

```bash
curl "http://localhost:8000/DiagnosticReport?_contained=both"
```

### Extract Practitioners from contained resources

```bash
curl "http://localhost:8000/Claim?_contained=true"
```

## Combining with Other Parameters

The `_contained` parameter can be combined with:

- **Pagination**: `?_contained=both&_count=50`
- **_elements**: `?_contained=true&_elements=code,status`
- **_summary**: `?_contained=both&_summary=true`
- **Search params**: `?status=active&_contained=both`

## Notes

- When `_contained` is not specified, the default behavior is `false`
- Contained resources extracted with `_contained=true` lose their container context
- The `_contained` parameter affects the result count and pagination
- Contained resources must have resourceType and id to be properly returned

## Related Parameters

- [_containedType](https://hl7.org/fhir/R4/search.html#containedType) - Filter by contained resource type (not yet implemented)
