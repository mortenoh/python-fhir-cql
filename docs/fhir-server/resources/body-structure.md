# BodyStructure

## Overview

The BodyStructure resource identifies specific anatomical locations on or in the body. It is used to describe lesions, tumors, implants, or other anatomical structures that are relevant for clinical observations, procedures, or device placement.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/bodystructure.html](https://hl7.org/fhir/R4/bodystructure.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `active` | boolean | Whether record is active |
| `morphology` | CodeableConcept | Kind of structure (lesion, tumor, etc.) |
| `location` | CodeableConcept | Body site |
| `locationQualifier` | CodeableConcept[] | Laterality, relative position |
| `description` | string | Text description |
| `image` | Attachment[] | Attached images |
| `patient` | Reference(Patient) | Patient |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=bs-001` |
| `identifier` | token | Business identifier | `identifier=BS-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `location` | token | Body location code | `location=39937001` |
| `morphology` | token | Morphology code | `morphology=4147007` |

## Examples

### Create a BodyStructure

```bash
curl -X POST http://localhost:8080/baseR4/BodyStructure \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "BodyStructure",
    "active": true,
    "morphology": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "4147007",
        "display": "Mass"
      }],
      "text": "Mass"
    },
    "location": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "39937001",
        "display": "Skin of chest"
      }],
      "text": "Skin of chest"
    },
    "locationQualifier": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "7771000",
        "display": "Left"
      }]
    }],
    "description": "2cm mass on left chest wall, noted during examination",
    "patient": {
      "reference": "Patient/patient-001"
    }
  }'
```

### Search BodyStructures

```bash
# By patient
curl "http://localhost:8080/baseR4/BodyStructure?patient=Patient/123"

# By location
curl "http://localhost:8080/baseR4/BodyStructure?location=39937001"

# By morphology
curl "http://localhost:8080/baseR4/BodyStructure?morphology=4147007"
```

### Patient Compartment

```bash
# Get all body structures for a patient
curl "http://localhost:8080/baseR4/Patient/123/BodyStructure"
```

## Common Morphologies (SNOMED CT)

| Code | Display |
|------|---------|
| 4147007 | Mass |
| 52988006 | Lesion |
| 108369006 | Tumor |
| 442083009 | Anatomical abnormality |
| 272673000 | Bone structure |
| 71388002 | Scar |
| 34823008 | Mole of skin |

## Common Body Locations (SNOMED CT)

| Code | Display |
|------|---------|
| 39937001 | Skin of chest |
| 774007 | Head and neck structure |
| 113197003 | Bone of lower limb |
| 113257007 | Structure of cardiovascular system |
| 72696002 | Knee joint structure |
| 45048000 | Neck structure |

## Location Qualifiers

| Code | Display |
|------|---------|
| 7771000 | Left |
| 24028007 | Right |
| 51440002 | Bilateral |
| 255561001 | Medial |
| 49370004 | Lateral |
| 261183002 | Upper |
| 261122009 | Lower |
