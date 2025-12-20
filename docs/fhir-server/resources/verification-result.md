# VerificationResult

## Overview

A VerificationResult describes the outcome of a verification process. It records the results of validating data against source systems or authoritative databases.

This resource is essential for data quality, provider credentialing, and regulatory compliance.

**Common use cases:**
- Provider credentialing
- License verification
- Data validation results
- Credential status tracking
- Compliance verification

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/verificationresult.html](https://hl7.org/fhir/R4/verificationresult.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `target` | Reference[] | Resource(s) being verified |
| `targetLocation` | string[] | Location of data being verified |
| `need` | CodeableConcept | Need for verification |
| `status` | code | attested, validated, in-process, etc. (required) |
| `statusDate` | dateTime | When status was achieved |
| `validationType` | CodeableConcept | Type of validation |
| `validationProcess` | CodeableConcept[] | Process used for validation |
| `frequency` | Timing | How often validation required |
| `lastPerformed` | dateTime | Last verification date |
| `nextScheduled` | date | Next scheduled verification |
| `failureAction` | CodeableConcept | Action on failure |
| `primarySource` | BackboneElement[] | Primary sources |
| `attestation` | BackboneElement | Attestation information |
| `validator` | BackboneElement[] | Validation organization |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=license-check-001` |
| `target` | reference | Target resource | `target=Practitioner/123` |
| `status` | token | Verification status | `status=validated` |

## Examples

### Create a VerificationResult

```bash
curl -X POST http://localhost:8080/baseR4/VerificationResult \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "VerificationResult",
    "target": [{"reference": "Practitioner/dr-smith"}],
    "targetLocation": ["Practitioner.qualification"],
    "need": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/need",
        "code": "periodic"
      }]
    },
    "status": "validated",
    "statusDate": "2024-01-15T10:00:00Z",
    "validationType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/validation-type",
        "code": "primary"
      }]
    },
    "validationProcess": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/validation-process",
        "code": "primary"
      }]
    }],
    "lastPerformed": "2024-01-15T10:00:00Z",
    "nextScheduled": "2025-01-15",
    "primarySource": [{
      "who": {"reference": "Organization/medical-board"},
      "type": [{
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/primary-source-type",
          "code": "lic-board"
        }]
      }],
      "validationStatus": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/validation-status",
          "code": "successful"
        }]
      },
      "validationDate": "2024-01-15T10:00:00Z"
    }]
  }'
```

### Search VerificationResults

```bash
# By target
curl "http://localhost:8080/baseR4/VerificationResult?target=Practitioner/dr-smith"

# By status
curl "http://localhost:8080/baseR4/VerificationResult?status=validated"
```

## Generator Usage

```python
from fhirkit.server.generator import VerificationResultGenerator

generator = VerificationResultGenerator(seed=42)

# Generate random verification result
result = generator.generate()

# Generate validated result
validated = generator.generate(status="validated")

# Generate batch
results = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| attested | Information has been attested |
| validated | Information has been validated |
| in-process | Validation in progress |
| req-revalid | Revalidation required |
| val-fail | Validation failed |
| reval-fail | Revalidation failed |

## Related Resources

- [Practitioner](./practitioner.md) - Provider being verified
- [Organization](./organization.md) - Organization verifying
- [PractitionerRole](./practitioner-role.md) - Role being verified
