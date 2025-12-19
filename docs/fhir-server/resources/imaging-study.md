# ImagingStudy

## Overview

The ImagingStudy resource represents DICOM imaging studies such as X-rays, CT scans, MRIs, and ultrasounds. It provides access to imaging content and metadata from PACS systems.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/imagingstudy.html](https://hl7.org/fhir/R4/imagingstudy.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers (accession number, study UID) |
| `status` | code | registered, available, cancelled, entered-in-error, unknown |
| `modality` | Coding[] | DICOM modalities (CT, MR, US, DX, etc.) |
| `subject` | Reference(Patient) | Patient being imaged |
| `encounter` | Reference(Encounter) | Encounter context |
| `started` | dateTime | When study started |
| `basedOn` | Reference[] | Request fulfilled |
| `referrer` | Reference(Practitioner) | Referring physician |
| `interpreter` | Reference(Practitioner)[] | Radiologist |
| `endpoint` | Reference(Endpoint)[] | DICOM endpoints |
| `numberOfSeries` | unsignedInt | Number of series |
| `numberOfInstances` | unsignedInt | Number of instances |
| `procedureReference` | Reference(Procedure) | Related procedure |
| `procedureCode` | CodeableConcept[] | Procedure code |
| `location` | Reference(Location) | Where study was performed |
| `reasonCode` | CodeableConcept[] | Why study was performed |
| `note` | Annotation[] | Notes |
| `description` | string | Study description |
| `series` | BackboneElement[] | Series within study |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=img-001` |
| `identifier` | token | Business identifier | `identifier=ACC123456` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `subject` | reference | Subject reference | `subject=Patient/123` |
| `status` | token | Study status | `status=available` |
| `modality` | token | DICOM modality | `modality=CT` |
| `started` | date | Study start date | `started=ge2024-01-01` |
| `encounter` | reference | Encounter reference | `encounter=Encounter/456` |
| `referrer` | reference | Referring physician | `referrer=Practitioner/789` |
| `basedon` | reference | Request fulfilled | `basedon=ServiceRequest/sr-001` |

## Examples

### Create an ImagingStudy

```bash
curl -X POST http://localhost:8080/baseR4/ImagingStudy \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ImagingStudy",
    "status": "available",
    "subject": {
      "reference": "Patient/patient-001"
    },
    "started": "2024-06-15T10:30:00Z",
    "modality": [{
      "system": "http://dicom.nema.org/resources/ontology/DCM",
      "code": "CT",
      "display": "Computed Tomography"
    }],
    "description": "CT Chest with contrast",
    "numberOfSeries": 3,
    "numberOfInstances": 256,
    "procedureCode": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "169069000",
        "display": "CT of chest"
      }]
    }]
  }'
```

### Search ImagingStudies

```bash
# By patient
curl "http://localhost:8080/baseR4/ImagingStudy?patient=Patient/123"

# By modality
curl "http://localhost:8080/baseR4/ImagingStudy?modality=CT"

# By status
curl "http://localhost:8080/baseR4/ImagingStudy?status=available"

# By date range
curl "http://localhost:8080/baseR4/ImagingStudy?started=ge2024-01-01"
```

### Patient Compartment

```bash
# Get all imaging studies for a patient
curl "http://localhost:8080/baseR4/Patient/123/ImagingStudy"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| registered | Registered | Study registered but not started |
| available | Available | Study is available for viewing |
| cancelled | Cancelled | Study was cancelled |
| entered-in-error | Entered in Error | Data entry error |
| unknown | Unknown | Status unknown |

## DICOM Modalities

| Code | Display |
|------|---------|
| CT | Computed Tomography |
| MR | Magnetic Resonance |
| US | Ultrasound |
| DX | Digital Radiography |
| CR | Computed Radiography |
| NM | Nuclear Medicine |
| PT | Positron Emission Tomography |
| XA | X-Ray Angiography |
| MG | Mammography |
| RF | Radio Fluoroscopy |
