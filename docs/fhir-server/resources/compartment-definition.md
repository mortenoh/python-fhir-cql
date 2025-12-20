# CompartmentDefinition

## Overview

A CompartmentDefinition defines a logical grouping of resources that share a common property. Compartments are used to restrict search results to resources associated with a particular subject (e.g., all resources for a specific patient).

This resource is essential for implementing patient-centric access controls and efficient data retrieval.

**Common use cases:**
- Patient compartment queries
- Practitioner data access
- Encounter-based grouping
- Access control implementation
- Data isolation patterns

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/compartmentdefinition.html](https://hl7.org/fhir/R4/compartmentdefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier (required) |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `status` | code | draft, active, retired, unknown (required) |
| `experimental` | boolean | For testing purposes only |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `code` | code | Patient, Encounter, RelatedPerson, Practitioner, Device (required) |
| `search` | boolean | Whether search is supported (required) |
| `resource` | BackboneElement[] | Resources included in compartment |
| `resource.code` | code | Resource type |
| `resource.param` | string[] | Search params linking to compartment |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=patient-compartment` |
| `url` | uri | Canonical URL | `url=http://hl7.org/fhir/CompartmentDefinition/patient` |
| `name` | string | Computer-friendly name | `name=PatientCompartment` |
| `code` | token | Compartment type | `code=Patient` |
| `status` | token | Status | `status=active` |

## Examples

### Create a CompartmentDefinition

```bash
curl -X POST http://localhost:8080/baseR4/CompartmentDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "CompartmentDefinition",
    "url": "http://example.org/fhir/CompartmentDefinition/custom-patient",
    "name": "CustomPatientCompartment",
    "status": "draft",
    "code": "Patient",
    "search": true,
    "resource": [
      {
        "code": "Observation",
        "param": ["subject", "performer"]
      },
      {
        "code": "Condition",
        "param": ["subject", "asserter"]
      },
      {
        "code": "MedicationRequest",
        "param": ["subject"]
      }
    ]
  }'
```

### Search CompartmentDefinitions

```bash
# By compartment code
curl "http://localhost:8080/baseR4/CompartmentDefinition?code=Patient"

# By status
curl "http://localhost:8080/baseR4/CompartmentDefinition?status=active"
```

### Use Compartment Search

```bash
# Get all resources in a patient's compartment
curl "http://localhost:8080/baseR4/Patient/123/*"

# Get specific resource types in compartment
curl "http://localhost:8080/baseR4/Patient/123/Observation"
```

## Generator Usage

```python
from fhirkit.server.generator import CompartmentDefinitionGenerator

generator = CompartmentDefinitionGenerator(seed=42)

# Generate a random compartment definition
compartment = generator.generate()

# Generate with specific code
patient_compartment = generator.generate(code="Patient")

# Generate batch
compartments = generator.generate_batch(count=5)
```

## Compartment Codes

| Code | Description |
|------|-------------|
| Patient | Resources associated with a patient |
| Encounter | Resources associated with an encounter |
| RelatedPerson | Resources associated with a related person |
| Practitioner | Resources associated with a practitioner |
| Device | Resources associated with a device |

## Related Resources

- [Patient](./patient.md) - Primary compartment subject
- [Encounter](./encounter.md) - Encounter compartment
- [Practitioner](./practitioner.md) - Practitioner compartment
- [SearchParameter](./search-parameter.md) - Search parameters defining compartment membership
