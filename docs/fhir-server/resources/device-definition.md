# DeviceDefinition

## Overview

The DeviceDefinition resource describes the characteristics and capabilities of a medical device model. It represents the device catalog entry or specification, not an individual device instance.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/devicedefinition.html](https://hl7.org/fhir/R4/devicedefinition.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `udiDeviceIdentifier` | BackboneElement[] | UDI device identifiers |
| `manufacturerString` | string | Manufacturer name |
| `manufacturerReference` | Reference(Organization) | Manufacturer organization |
| `deviceName` | BackboneElement[] | Device names |
| `modelNumber` | string | Model number |
| `type` | CodeableConcept | Device type |
| `specialization` | BackboneElement[] | Specializations |
| `version` | BackboneElement[] | Version information |
| `safety` | CodeableConcept[] | Safety information |
| `shelfLifeStorage` | ProductShelfLife[] | Shelf life/storage |
| `physicalCharacteristics` | ProdCharacteristic | Physical characteristics |
| `languageCode` | CodeableConcept[] | Language of labels |
| `capability` | BackboneElement[] | Device capabilities |
| `property` | BackboneElement[] | Device properties |
| `owner` | Reference(Organization) | Owner organization |
| `contact` | ContactPoint[] | Contact details |
| `url` | uri | Device URL |
| `onlineInformation` | uri | Online info URL |
| `note` | Annotation[] | Notes |
| `quantity` | Quantity | Batch quantity |
| `parentDevice` | Reference(DeviceDefinition) | Parent device |
| `material` | BackboneElement[] | Material composition |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=dd-001` |
| `identifier` | token | Business identifier | `identifier=DD-12345` |
| `type` | token | Device type | `type=43770009` |
| `manufacturer` | string | Manufacturer | `manufacturer=Acme` |
| `parent` | reference | Parent device | `parent=DeviceDefinition/dd-parent` |

## Examples

### Create a DeviceDefinition

```bash
curl -X POST http://localhost:8080/baseR4/DeviceDefinition \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DeviceDefinition",
    "identifier": [{
      "system": "http://example.org/device-catalog",
      "value": "BPM-PRO-2000"
    }],
    "manufacturerString": "Acme Medical Devices Inc.",
    "deviceName": [{
      "name": "Blood Pressure Monitor Pro",
      "type": "user-friendly-name"
    }],
    "modelNumber": "BPM-PRO-2000",
    "type": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "43770009",
        "display": "Sphygmomanometer"
      }],
      "text": "Blood Pressure Monitor"
    },
    "version": [{
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/device-version-type",
          "code": "firmware",
          "display": "Firmware"
        }]
      },
      "value": "v2.5.1"
    }],
    "safety": [{
      "coding": [{
        "system": "urn:oid:2.16.840.1.113883.3.26.1.1",
        "code": "mr-safe",
        "display": "MR Safe"
      }]
    }],
    "capability": [{
      "type": {
        "coding": [{
          "code": "systolic",
          "display": "Measures systolic blood pressure"
        }]
      }
    }],
    "property": [{
      "type": {
        "coding": [{
          "code": "accuracy",
          "display": "Measurement accuracy"
        }]
      },
      "valueQuantity": [{
        "value": 3,
        "unit": "mmHg"
      }]
    }]
  }'
```

### Search DeviceDefinitions

```bash
# By type
curl "http://localhost:8080/baseR4/DeviceDefinition?type=43770009"

# By manufacturer
curl "http://localhost:8080/baseR4/DeviceDefinition?manufacturer=Acme"

# By identifier
curl "http://localhost:8080/baseR4/DeviceDefinition?identifier=BPM-PRO-2000"
```

## Device Types (SNOMED CT)

| Code | Display |
|------|---------|
| 43770009 | Sphygmomanometer |
| 19257004 | Defibrillator |
| 303607000 | Cochlear implant |
| 272265001 | Bone prosthesis |
| 37299003 | Glucose monitor |
| 53350007 | Pacemaker |
| 462894001 | Insulin pump |
| 360063003 | CPAP machine |

## Device Name Types

| Code | Display |
|------|---------|
| udi-label-name | UDI Label Name |
| user-friendly-name | User Friendly Name |
| patient-reported-name | Patient Reported Name |
| manufacturer-name | Manufacturer Name |
| model-name | Model Name |
| other | Other |

## Safety Codes

| Code | Display |
|------|---------|
| mr-safe | MR Safe |
| mr-conditional | MR Conditional |
| mr-unsafe | MR Unsafe |
| latex-safe | Latex Free |
