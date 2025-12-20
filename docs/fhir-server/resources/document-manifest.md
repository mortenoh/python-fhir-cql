# DocumentManifest

## Overview

A DocumentManifest represents a collection of documents or references to documents that together form a complete set. It is used to group related documents, such as a complete medical record, discharge summary package, or a set of related diagnostic reports.

This resource acts as a container or envelope for document collections, providing metadata about the collection as a whole.

**Common use cases:**
- Medical record packages
- Discharge summaries
- Care coordination documents
- XDS document sets
- Document submission packages

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/documentmanifest.html](https://hl7.org/fhir/R4/documentmanifest.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `masterIdentifier` | Identifier | Master identifier |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | current, superseded, entered-in-error |
| `type` | CodeableConcept | Kind of document set |
| `subject` | Reference(Patient) | Subject of the documents |
| `created` | dateTime | When manifest was created |
| `author` | Reference(Practitioner|Organization)[] | Who authored the manifest |
| `recipient` | Reference(Practitioner|Organization|Patient)[] | Intended recipients |
| `source` | uri | Source system URI |
| `description` | string | Manifest description |
| `content` | Reference(Any)[] | Documents included |
| `related` | BackboneElement[] | Related identifiers |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=manifest-001` |
| `identifier` | token | Business identifier | `identifier=DM-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `status` | token | Manifest status | `status=current` |
| `created` | date | Creation date | `created=2024-01-15` |
| `type` | token | Document type | `type=discharge-summary` |
| `author` | reference | Author reference | `author=Practitioner/456` |

## Examples

### Create a DocumentManifest

```bash
curl -X POST http://localhost:8080/baseR4/DocumentManifest \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DocumentManifest",
    "masterIdentifier": {
      "system": "http://hospital.example.org/manifests",
      "value": "DM-2024-001"
    },
    "status": "current",
    "type": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "18842-5",
        "display": "Discharge summary"
      }]
    },
    "subject": {"reference": "Patient/123"},
    "created": "2024-01-15T10:00:00Z",
    "author": [{"reference": "Practitioner/456"}],
    "description": "Discharge documentation package",
    "content": [
      {"reference": "DocumentReference/doc-001"},
      {"reference": "DocumentReference/doc-002"}
    ]
  }'
```

### Search DocumentManifests

```bash
# By patient
curl "http://localhost:8080/baseR4/DocumentManifest?patient=Patient/123"

# By status
curl "http://localhost:8080/baseR4/DocumentManifest?status=current"

# By type
curl "http://localhost:8080/baseR4/DocumentManifest?type=18842-5"
```

## Generator Usage

```python
from fhirkit.server.generator import DocumentManifestGenerator

generator = DocumentManifestGenerator(seed=42)

# Generate a random document manifest
manifest = generator.generate()

# Generate for specific patient
patient_manifest = generator.generate(
    subject_reference="Patient/123",
    status="current"
)

# Generate batch
manifests = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| current | Manifest is current |
| superseded | Manifest has been superseded |
| entered-in-error | Entered in error |

## Related Resources

- [DocumentReference](./document-reference.md) - Individual documents in the manifest
- [Patient](./patient.md) - Subject of the documents
- [Composition](./composition.md) - Clinical document
