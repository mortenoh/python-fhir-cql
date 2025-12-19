# Specimen

## Overview

The Specimen resource represents a sample to be used for analysis. It tracks specimen collection, processing, and container information. Specimens are commonly referenced by DiagnosticReport and Observation resources.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/specimen.html](https://hl7.org/fhir/R4/specimen.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Specimen identifiers |
| `accessionIdentifier` | Identifier | Lab accession number |
| `status` | code | available, unavailable, unsatisfactory, entered-in-error |
| `type` | CodeableConcept | Type of specimen (SNOMED CT) |
| `subject` | Reference(Patient) | Patient the specimen is from |
| `receivedTime` | dateTime | When specimen was received |
| `collection` | BackboneElement | Collection details |
| `processing` | BackboneElement[] | Processing steps |
| `container` | BackboneElement[] | Container information |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=specimen-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Specimen status | `status=available` |
| `type` | token | Specimen type | `type=http://snomed.info/sct\|119297000` |
| `collector` | reference | Who collected | `collector=Practitioner/nurse-1` |
| `accession` | token | Accession identifier | `accession=ACC-2024-001` |
| `collected` | date | Collection date | `collected=2024-01-15` |

## Examples

### Create a Specimen

```bash
curl -X POST http://localhost:8080/baseR4/Specimen \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Specimen",
    "identifier": [{
      "system": "http://lab.example.org/specimens",
      "value": "SPEC-2024-001234"
    }],
    "accessionIdentifier": {
      "system": "http://lab.example.org/accession",
      "value": "ACC-2024-5678"
    },
    "status": "available",
    "type": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "119297000",
        "display": "Blood specimen"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "receivedTime": "2024-01-15T07:30:00Z",
    "collection": {
      "collector": {"reference": "Practitioner/nurse-1"},
      "collectedDateTime": "2024-01-15T07:15:00Z",
      "quantity": {
        "value": 10,
        "unit": "mL"
      },
      "bodySite": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "49852007",
          "display": "Median cubital vein"
        }]
      }
    },
    "container": [{
      "type": {
        "text": "Purple top EDTA tube"
      },
      "specimenQuantity": {
        "value": 8,
        "unit": "mL"
      }
    }]
  }'
```

### Search Specimens

```bash
# By patient
curl "http://localhost:8080/baseR4/Specimen?patient=Patient/patient-1"

# By type
curl "http://localhost:8080/baseR4/Specimen?type=http://snomed.info/sct|119297000"

# By status
curl "http://localhost:8080/baseR4/Specimen?status=available"
```

## Specimen Types (SNOMED CT)

| Code | Display |
|------|---------|
| 119297000 | Blood specimen |
| 122555007 | Venous blood specimen |
| 119339001 | Serum specimen |
| 119361006 | Plasma specimen |
| 122575003 | Urine specimen |
| 119376003 | Tissue specimen |
| 119295008 | Aspirate |
| 258580003 | Whole blood |

## Status Codes

| Code | Description |
|------|-------------|
| available | Specimen is available for processing |
| unavailable | Specimen is not available |
| unsatisfactory | Specimen quality is not acceptable |
| entered-in-error | Entry was made in error |
