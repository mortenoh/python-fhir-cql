# ObservationDefinition

## Overview

An ObservationDefinition defines the characteristics of an observation type, including its code, method, and valid ranges. It provides metadata about how observations should be captured and interpreted.

This resource is essential for laboratory information systems, clinical data standards, and observation validation.

**Common use cases:**
- Laboratory test definitions
- Vital sign specifications
- Reference range definitions
- Test catalog management
- Data quality standards

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/observationdefinition.html](https://hl7.org/fhir/R4/observationdefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `category` | CodeableConcept[] | Category of observation |
| `code` | CodeableConcept | Type of observation (required) |
| `identifier` | Identifier[] | Business identifiers |
| `permittedDataType` | code[] | Quantity, CodeableConcept, string, etc. |
| `multipleResultsAllowed` | boolean | Multiple results allowed |
| `method` | CodeableConcept | Method of observation |
| `preferredReportName` | string | Preferred display name |
| `quantitativeDetails` | BackboneElement | Quantitative details |
| `qualifiedInterval` | BackboneElement[] | Reference ranges |
| `validCodedValueSet` | Reference(ValueSet) | Valid coded values |
| `normalCodedValueSet` | Reference(ValueSet) | Normal coded values |
| `abnormalCodedValueSet` | Reference(ValueSet) | Abnormal coded values |
| `criticalCodedValueSet` | Reference(ValueSet) | Critical coded values |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=glucose-test` |
| `code` | token | Observation code | `code=http://loinc.org\|2339-0` |
| `identifier` | token | Business identifier | `identifier=TEST-001` |

## Examples

### Create an ObservationDefinition

```bash
curl -X POST http://localhost:8080/baseR4/ObservationDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ObservationDefinition",
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
        "code": "laboratory"
      }]
    }],
    "code": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "2339-0",
        "display": "Glucose [Mass/volume] in Blood"
      }]
    },
    "permittedDataType": ["Quantity"],
    "multipleResultsAllowed": false,
    "method": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "271061004",
        "display": "Random blood glucose measurement"
      }]
    },
    "preferredReportName": "Blood Glucose",
    "quantitativeDetails": {
      "customaryUnit": {
        "coding": [{
          "system": "http://unitsofmeasure.org",
          "code": "mg/dL"
        }]
      },
      "decimalPrecision": 0
    },
    "qualifiedInterval": [
      {
        "category": "reference",
        "range": {"low": {"value": 70}, "high": {"value": 100}},
        "context": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/referencerange-meaning",
            "code": "normal"
          }]
        }
      },
      {
        "category": "critical",
        "range": {"high": {"value": 50}},
        "context": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/referencerange-meaning",
            "code": "critical-low"
          }]
        }
      }
    ]
  }'
```

### Search ObservationDefinitions

```bash
# By code
curl "http://localhost:8080/baseR4/ObservationDefinition?code=http://loinc.org|2339-0"
```

## Generator Usage

```python
from fhirkit.server.generator import ObservationDefinitionGenerator

generator = ObservationDefinitionGenerator(seed=42)

# Generate random definition
definition = generator.generate()

# Generate batch
definitions = generator.generate_batch(count=10)
```

## Related Resources

- [Observation](./observation.md) - Observations using this definition
- [DiagnosticReport](./diagnostic-report.md) - Reports containing observations
- [ValueSet](./value-set.md) - Valid value sets
