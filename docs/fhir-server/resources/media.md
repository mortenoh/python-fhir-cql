# Media

## Overview

The Media resource contains a photo, video, or audio recording acquired or used in healthcare. Common uses include clinical photographs, diagnostic images, audio recordings, and video recordings.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/media.html](https://hl7.org/fhir/R4/media.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | preparation, in-progress, not-done, on-hold, stopped, completed, entered-in-error, unknown |
| `type` | CodeableConcept | image, video, audio |
| `modality` | CodeableConcept | DICOM modality (DX, CT, MR, etc.) |
| `view` | CodeableConcept | Imaging view (AP, PA, lateral, etc.) |
| `subject` | Reference(Patient) | Who/what the media is about |
| `encounter` | Reference(Encounter) | Related encounter |
| `createdDateTime` | dateTime | When media was created |
| `issued` | instant | When media was issued |
| `operator` | Reference(Practitioner) | Who created the media |
| `reasonCode` | CodeableConcept[] | Why the media was created |
| `bodySite` | CodeableConcept | Body part shown |
| `deviceName` | string | Device used |
| `height` | positiveInt | Height in pixels |
| `width` | positiveInt | Width in pixels |
| `content` | Attachment | Actual media content |
| `note` | Annotation[] | Comments |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=media-001` |
| `patient` | reference | Patient subject | `patient=Patient/123` |
| `subject` | reference | Subject (alias) | `subject=Patient/123` |
| `status` | token | Media status | `status=completed` |
| `type` | token | Media type | `type=image` |
| `modality` | token | DICOM modality | `modality=DX` |
| `created` | date | When created | `created=2024-01-15` |
| `site` | token | Body site | `site=http://snomed.info/sct\|51185008` |
| `operator` | reference | Who created | `operator=Practitioner/tech-1` |

## Examples

### Create a Media

```bash
curl -X POST http://localhost:8080/baseR4/Media \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Media",
    "status": "completed",
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/media-type",
        "code": "image",
        "display": "Image"
      }]
    },
    "modality": {
      "coding": [{
        "system": "http://dicom.nema.org/resources/ontology/DCM",
        "code": "DX",
        "display": "Digital Radiography"
      }]
    },
    "view": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "399162004",
        "display": "Postero-anterior"
      }]
    },
    "subject": {"reference": "Patient/patient-1"},
    "createdDateTime": "2024-01-15T11:00:00Z",
    "operator": {"reference": "Practitioner/rad-tech-1"},
    "bodySite": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "51185008",
        "display": "Thoracic structure"
      }]
    },
    "deviceName": "Philips DigitalDiagnost",
    "height": 3000,
    "width": 2500,
    "content": {
      "contentType": "image/jpeg",
      "url": "http://imaging.example.org/images/chest-xray-001.jpg",
      "title": "Chest X-ray PA view"
    }
  }'
```

### Search Media

```bash
# By patient
curl "http://localhost:8080/baseR4/Media?patient=Patient/patient-1"

# By type
curl "http://localhost:8080/baseR4/Media?type=image"

# By modality
curl "http://localhost:8080/baseR4/Media?modality=DX"

# By date
curl "http://localhost:8080/baseR4/Media?created=2024-01-15"
```

## Media Types

| Code | Display |
|------|---------|
| image | Image |
| video | Video |
| audio | Audio |

## DICOM Modalities

| Code | Display |
|------|---------|
| DX | Digital Radiography |
| CR | Computed Radiography |
| CT | Computed Tomography |
| MR | Magnetic Resonance |
| US | Ultrasound |
| NM | Nuclear Medicine |
| PT | PET |
| XA | X-Ray Angiography |
| ES | Endoscopy |

## Status Codes

| Code | Description |
|------|-------------|
| preparation | Being prepared |
| in-progress | In progress |
| not-done | Not done |
| on-hold | On hold |
| stopped | Stopped |
| completed | Completed |
| entered-in-error | Entry was made in error |
| unknown | Unknown |
