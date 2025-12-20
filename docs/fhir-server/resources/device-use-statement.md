# DeviceUseStatement

## Overview

A DeviceUseStatement records a patient's use of a medical device. Unlike DeviceRequest which represents an order for a device, DeviceUseStatement documents that a device has been or is being used by a patient.

This resource is used to track the history of device usage for clinical care, billing, and reporting purposes.

**Common use cases:**
- Medical device usage tracking
- Durable medical equipment records
- Implant history
- Home healthcare device usage
- Patient-reported device use

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/deviceusestatement.html](https://hl7.org/fhir/R4/deviceusestatement.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | active, completed, entered-in-error, intended, stopped, on-hold |
| `subject` | Reference(Patient) | Patient using the device |
| `device` | Reference(Device) | Device being used |
| `timingDateTime` | dateTime | When device was used |
| `timingPeriod` | Period | Usage period |
| `recordedOn` | dateTime | When statement was recorded |
| `source` | Reference(Patient|Practitioner|RelatedPerson) | Who made the statement |
| `derivedFrom` | Reference(Any)[] | Supporting information |
| `reasonCode` | CodeableConcept[] | Reason for device use |
| `reasonReference` | Reference(Condition)[] | Condition justifying use |
| `bodySite` | CodeableConcept | Target body site |
| `note` | Annotation[] | Additional notes |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=statement-001` |
| `identifier` | token | Business identifier | `identifier=DUS-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `device` | reference | Device reference | `device=Device/dev-001` |

## Examples

### Create a DeviceUseStatement

```bash
curl -X POST http://localhost:8080/baseR4/DeviceUseStatement \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DeviceUseStatement",
    "identifier": [{
      "system": "http://hospital.example.org/device-use",
      "value": "DUS-2024-001"
    }],
    "status": "active",
    "subject": {"reference": "Patient/123"},
    "device": {"reference": "Device/cpap-001"},
    "timingPeriod": {
      "start": "2024-01-15"
    },
    "recordedOn": "2024-01-15T10:00:00Z",
    "source": {"reference": "Patient/123"},
    "reasonCode": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "78275009",
        "display": "Obstructive sleep apnea"
      }]
    }]
  }'
```

### Search DeviceUseStatements

```bash
# By patient
curl "http://localhost:8080/baseR4/DeviceUseStatement?patient=Patient/123"

# By device
curl "http://localhost:8080/baseR4/DeviceUseStatement?device=Device/cpap-001"
```

## Generator Usage

```python
from fhirkit.server.generator import DeviceUseStatementGenerator

generator = DeviceUseStatementGenerator(seed=42)

# Generate a random device use statement
statement = generator.generate()

# Generate for specific patient
patient_statement = generator.generate(
    subject_reference="Patient/123",
    status="active"
)

# Generate batch
statements = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| active | Device is actively being used |
| completed | Device use is complete |
| entered-in-error | Entered in error |
| intended | Device use is planned |
| stopped | Device use was stopped |
| on-hold | Device use is on hold |

## Related Resources

- [Device](./device.md) - The device being used
- [DeviceRequest](./device-request.md) - Original device request
- [Patient](./patient.md) - Patient using the device
