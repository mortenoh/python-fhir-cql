# Endpoint

## Overview

The Endpoint resource describes a network-accessible technical destination for exchanging data. It is used to identify FHIR servers, DICOM PACS systems, HL7v2 interfaces, and other healthcare integration endpoints.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/endpoint.html](https://hl7.org/fhir/R4/endpoint.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `status` | code | active, suspended, error, off, entered-in-error, test |
| `connectionType` | Coding | Connection protocol (required) |
| `name` | string | Endpoint name |
| `managingOrganization` | Reference(Organization) | Managing organization |
| `contact` | ContactPoint[] | Contact details |
| `period` | Period | Operational period |
| `payloadType` | CodeableConcept[] | Payload types supported |
| `payloadMimeType` | code[] | MIME types supported |
| `address` | url | Endpoint URL (required) |
| `header` | string[] | HTTP headers |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=ep-001` |
| `identifier` | token | Business identifier | `identifier=EP-12345` |
| `status` | token | Endpoint status | `status=active` |
| `connection-type` | token | Connection type | `connection-type=hl7-fhir-rest` |
| `name` | string | Endpoint name | `name=Hospital` |
| `organization` | reference | Managing org | `organization=Organization/456` |
| `payload-type` | token | Payload type | `payload-type=any` |

## Examples

### Create a FHIR Endpoint

```bash
curl -X POST http://localhost:8080/baseR4/Endpoint \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Endpoint",
    "identifier": [{
      "system": "http://example.org/endpoint-ids",
      "value": "EP-FHIR-001"
    }],
    "status": "active",
    "connectionType": {
      "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
      "code": "hl7-fhir-rest",
      "display": "HL7 FHIR REST"
    },
    "name": "General Hospital FHIR Server",
    "managingOrganization": {
      "reference": "Organization/organization-001"
    },
    "contact": [{
      "system": "email",
      "value": "integration@hospital.org"
    }],
    "payloadType": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/endpoint-payload-type",
        "code": "any",
        "display": "Any"
      }]
    }],
    "payloadMimeType": [
      "application/fhir+json",
      "application/fhir+xml"
    ],
    "address": "https://fhir.hospital.org/baseR4"
  }'
```

### Create a DICOM Endpoint

```bash
curl -X POST http://localhost:8080/baseR4/Endpoint \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Endpoint",
    "status": "active",
    "connectionType": {
      "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
      "code": "dicom-wado-rs",
      "display": "DICOM WADO-RS"
    },
    "name": "Radiology PACS",
    "payloadType": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/endpoint-payload-type",
        "code": "any"
      }]
    }],
    "payloadMimeType": ["application/dicom"],
    "address": "https://pacs.hospital.org/dicom"
  }'
```

### Create an HL7v2 Endpoint

```bash
curl -X POST http://localhost:8080/baseR4/Endpoint \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Endpoint",
    "status": "active",
    "connectionType": {
      "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
      "code": "hl7v2-mllp",
      "display": "HL7 v2 MLLP"
    },
    "name": "ADT Interface",
    "payloadType": [{
      "coding": [{
        "system": "urn:hl7-org:v2",
        "code": "ADT",
        "display": "ADT Messages"
      }]
    }],
    "payloadMimeType": ["application/hl7-v2"],
    "address": "mllp://interface.hospital.org:2575"
  }'
```

### Search Endpoints

```bash
# By status
curl "http://localhost:8080/baseR4/Endpoint?status=active"

# By connection type
curl "http://localhost:8080/baseR4/Endpoint?connection-type=hl7-fhir-rest"

# By organization
curl "http://localhost:8080/baseR4/Endpoint?organization=Organization/456"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| active | Active | Endpoint is operational |
| suspended | Suspended | Temporarily unavailable |
| error | Error | Error state |
| off | Off | Not currently in use |
| entered-in-error | Entered in Error | Data entry error |
| test | Test | Test endpoint |

## Connection Types

| Code | Display | Description |
|------|---------|-------------|
| hl7-fhir-rest | HL7 FHIR REST | FHIR RESTful API |
| hl7-fhir-msg | HL7 FHIR Messaging | FHIR messaging |
| hl7v2-mllp | HL7 v2 MLLP | HL7v2 over MLLP |
| dicom-wado-rs | DICOM WADO-RS | DICOM Web Access |
| dicom-qido-rs | DICOM QIDO-RS | DICOM Query |
| dicom-stow-rs | DICOM STOW-RS | DICOM Store |
| ihe-xcpd | IHE XCPD | Cross-Community Patient Discovery |
| ihe-xca | IHE XCA | Cross-Community Access |
| ihe-xdr | IHE XDR | Cross-Enterprise Document Reliable Interchange |
| ihe-xds | IHE XDS | Cross-Enterprise Document Sharing |
| direct-project | Direct Project | Direct secure messaging |

## Common MIME Types

| MIME Type | Description |
|-----------|-------------|
| application/fhir+json | FHIR JSON |
| application/fhir+xml | FHIR XML |
| application/dicom | DICOM |
| application/hl7-v2 | HL7v2 |
| text/x-cda | CDA Documents |
| application/pdf | PDF Documents |
