# Composition

## Overview

A Composition is a structure for grouping information together into a coherent clinical document. It defines the structure and narrative content of a clinical document like a discharge summary, progress note, or consultation report.

This resource is essential for clinical documentation, document sharing, and structured clinical notes.

**Common use cases:**
- Discharge summaries
- Progress notes
- Consultation reports
- Referral letters
- Clinical document authoring

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/composition.html](https://hl7.org/fhir/R4/composition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier | Business identifier |
| `status` | code | preliminary, final, amended, entered-in-error (required) |
| `type` | CodeableConcept | Kind of composition (required) |
| `category` | CodeableConcept[] | Categorization of composition |
| `subject` | Reference | Who/what the composition is about |
| `encounter` | Reference(Encounter) | Context of the composition |
| `date` | dateTime | Composition editing time (required) |
| `author` | Reference[] | Who/what authored the composition (required) |
| `title` | string | Human-readable title (required) |
| `confidentiality` | code | Document confidentiality |
| `attester` | BackboneElement[] | Attestation statements |
| `custodian` | Reference(Organization) | Organization maintaining the document |
| `relatesTo` | BackboneElement[] | Relationships to other compositions |
| `event` | BackboneElement[] | Clinical service(s) documented |
| `section` | BackboneElement[] | Document sections |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=discharge-summary-001` |
| `identifier` | token | Business identifier | `identifier=DOC-12345` |
| `type` | token | Document type | `type=http://loinc.org\|18842-5` |
| `status` | token | Document status | `status=final` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `author` | reference | Author reference | `author=Practitioner/456` |
| `date` | date | Composition date | `date=ge2024-01-01` |
| `encounter` | reference | Encounter reference | `encounter=Encounter/789` |

## Examples

### Create a Composition

```bash
curl -X POST http://localhost:8080/baseR4/Composition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Composition",
    "status": "final",
    "type": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "18842-5",
        "display": "Discharge summary"
      }]
    },
    "subject": {"reference": "Patient/123"},
    "encounter": {"reference": "Encounter/456"},
    "date": "2024-01-15T14:30:00Z",
    "author": [{"reference": "Practitioner/789"}],
    "title": "Discharge Summary",
    "section": [
      {
        "title": "Chief Complaint",
        "code": {
          "coding": [{
            "system": "http://loinc.org",
            "code": "10154-3"
          }]
        },
        "text": {
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Patient presented with chest pain</div>"
        }
      },
      {
        "title": "Medications",
        "code": {
          "coding": [{
            "system": "http://loinc.org",
            "code": "10160-0"
          }]
        },
        "entry": [
          {"reference": "MedicationRequest/med-001"},
          {"reference": "MedicationRequest/med-002"}
        ]
      }
    ]
  }'
```

### Search Compositions

```bash
# By type
curl "http://localhost:8080/baseR4/Composition?type=http://loinc.org|18842-5"

# By subject
curl "http://localhost:8080/baseR4/Composition?subject=Patient/123"

# By date range
curl "http://localhost:8080/baseR4/Composition?date=ge2024-01-01&date=le2024-12-31"
```

## Generator Usage

```python
from fhirkit.server.generator import CompositionGenerator

generator = CompositionGenerator(seed=42)

# Generate a random composition
composition = generator.generate()

# Generate discharge summary
discharge = generator.generate(
    type_code="18842-5",
    status="final"
)

# Generate batch
compositions = generator.generate_batch(count=10)
```

## Status Codes

| Code | Description |
|------|-------------|
| preliminary | Initial draft |
| final | Complete and verified |
| amended | Modified after finalization |
| entered-in-error | Entered in error |

## Common Document Types (LOINC)

| Code | Display |
|------|---------|
| 18842-5 | Discharge summary |
| 11488-4 | Consultation note |
| 11506-3 | Progress note |
| 34133-9 | Summarization of episode note |
| 57133-1 | Referral note |

## Related Resources

- [Patient](./patient.md) - Document subject
- [Practitioner](./practitioner.md) - Document author
- [Encounter](./encounter.md) - Clinical context
- [DocumentReference](./document-reference.md) - Document metadata
- [Bundle](./bundle.md) - Document bundle
