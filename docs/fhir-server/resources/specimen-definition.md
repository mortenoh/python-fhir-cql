# SpecimenDefinition

## Overview

A SpecimenDefinition describes the characteristics of specimens for laboratory testing, including collection requirements, container specifications, and handling instructions.

This resource is essential for laboratory information systems and specimen collection protocols.

**Common use cases:**
- Specimen collection requirements
- Container specifications
- Handling instructions
- Laboratory test ordering
- Pre-analytical requirements

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/specimendefinition.html](https://hl7.org/fhir/R4/specimendefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier | Business identifier |
| `typeCollected` | CodeableConcept | Type of specimen |
| `patientPreparation` | CodeableConcept[] | Patient preparation |
| `timeAspect` | string | Time aspect (e.g., "24 hour") |
| `collection` | CodeableConcept[] | Collection procedure |
| `typeTested` | BackboneElement[] | Specimen types tested |
| `typeTested.type` | CodeableConcept | Specimen type |
| `typeTested.preference` | code | preferred, alternate |
| `typeTested.container` | BackboneElement | Container requirements |
| `typeTested.requirement` | string | Requirements for specimen |
| `typeTested.retentionTime` | Duration | Retention time |
| `typeTested.handling` | BackboneElement[] | Handling instructions |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=blood-specimen` |
| `identifier` | token | Business identifier | `identifier=SPEC-001` |
| `type` | token | Specimen type | `type=http://snomed.info/sct\|119297000` |

## Examples

### Create a SpecimenDefinition

```bash
curl -X POST http://localhost:8080/baseR4/SpecimenDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SpecimenDefinition",
    "identifier": {
      "system": "http://example.org/specimen-defs",
      "value": "BLOOD-CBC"
    },
    "typeCollected": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "119297000",
        "display": "Blood specimen"
      }]
    },
    "patientPreparation": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "263678003",
        "display": "Fasting"
      }]
    }],
    "typeTested": [{
      "type": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "122555007",
          "display": "Venous blood specimen"
        }]
      },
      "preference": "preferred",
      "container": {
        "type": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "706055000",
            "display": "EDTA tube"
          }]
        },
        "cap": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/container-cap",
            "code": "lavender"
          }]
        },
        "minimumVolumeQuantity": {"value": 3, "unit": "mL"}
      },
      "requirement": "Collect in the morning before eating",
      "retentionTime": {"value": 7, "unit": "d"},
      "handling": [{
        "temperatureQualifier": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/handling-condition",
            "code": "room"
          }]
        },
        "maxDuration": {"value": 2, "unit": "h"}
      }]
    }]
  }'
```

### Search SpecimenDefinitions

```bash
# By type
curl "http://localhost:8080/baseR4/SpecimenDefinition?type=http://snomed.info/sct|119297000"
```

## Generator Usage

```python
from fhirkit.server.generator import SpecimenDefinitionGenerator

generator = SpecimenDefinitionGenerator(seed=42)

# Generate random definition
definition = generator.generate()

# Generate batch
definitions = generator.generate_batch(count=10)
```

## Related Resources

- [Specimen](./specimen.md) - Collected specimens
- [ServiceRequest](./service-request.md) - Test orders
- [ObservationDefinition](./observation-definition.md) - Test definitions
