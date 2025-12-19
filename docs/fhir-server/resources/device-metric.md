# DeviceMetric

## Overview

The DeviceMetric resource describes measurement or calculation capabilities of a medical device. It represents the metrics that a device can report, such as heart rate, blood oxygen, or battery level.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/devicemetric.html](https://hl7.org/fhir/R4/devicemetric.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `type` | CodeableConcept | Metric type (required) |
| `unit` | CodeableConcept | Unit of measurement |
| `source` | Reference(Device) | Source device |
| `parent` | Reference(Device) | Parent device |
| `operationalStatus` | code | on, off, standby, entered-in-error |
| `color` | code | Display color |
| `category` | code | measurement, setting, calculation, unspecified |
| `measurementPeriod` | Timing | Measurement frequency |
| `calibration` | BackboneElement[] | Calibration information |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=dm-001` |
| `identifier` | token | Business identifier | `identifier=DM-12345` |
| `type` | token | Metric type | `type=150456` |
| `source` | reference | Source device | `source=Device/123` |
| `parent` | reference | Parent device | `parent=Device/456` |
| `category` | token | Metric category | `category=measurement` |

## Examples

### Create a DeviceMetric

```bash
curl -X POST http://localhost:8080/baseR4/DeviceMetric \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DeviceMetric",
    "identifier": [{
      "system": "http://example.org/device-metrics",
      "value": "HR-METRIC-001"
    }],
    "type": {
      "coding": [{
        "system": "urn:iso:std:iso:11073:10101",
        "code": "150456",
        "display": "Heart rate"
      }],
      "text": "Heart Rate"
    },
    "unit": {
      "coding": [{
        "system": "http://unitsofmeasure.org",
        "code": "/min",
        "display": "beats per minute"
      }]
    },
    "source": {
      "reference": "Device/patient-monitor-001"
    },
    "operationalStatus": "on",
    "category": "measurement",
    "measurementPeriod": {
      "repeat": {
        "frequency": 1,
        "period": 5,
        "periodUnit": "s"
      }
    },
    "calibration": [{
      "type": "two-point",
      "state": "calibrated",
      "time": "2024-06-15T08:00:00Z"
    }]
  }'
```

### Create a Battery Level Metric

```bash
curl -X POST http://localhost:8080/baseR4/DeviceMetric \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "DeviceMetric",
    "type": {
      "coding": [{
        "system": "urn:iso:std:iso:11073:10101",
        "code": "67996",
        "display": "Battery level"
      }]
    },
    "unit": {
      "coding": [{
        "system": "http://unitsofmeasure.org",
        "code": "%",
        "display": "percent"
      }]
    },
    "source": {
      "reference": "Device/insulin-pump-001"
    },
    "operationalStatus": "on",
    "category": "setting"
  }'
```

### Search DeviceMetrics

```bash
# By source device
curl "http://localhost:8080/baseR4/DeviceMetric?source=Device/123"

# By type
curl "http://localhost:8080/baseR4/DeviceMetric?type=150456"

# By category
curl "http://localhost:8080/baseR4/DeviceMetric?category=measurement"
```

## Operational Status

| Code | Display | Description |
|------|---------|-------------|
| on | On | Metric is operating |
| off | Off | Metric is not operating |
| standby | Standby | Metric is in standby |
| entered-in-error | Entered in Error | Data entry error |

## Category Codes

| Code | Display | Description |
|------|---------|-------------|
| measurement | Measurement | Device measurement |
| setting | Setting | Device setting |
| calculation | Calculation | Derived/calculated value |
| unspecified | Unspecified | Not specified |

## Calibration Types

| Code | Display |
|------|---------|
| unspecified | Unspecified |
| offset | Offset (single point) |
| gain | Gain |
| two-point | Two-point calibration |

## Calibration States

| Code | Display |
|------|---------|
| not-calibrated | Not Calibrated |
| calibration-required | Calibration Required |
| calibrated | Calibrated |
| unspecified | Unspecified |

## Common Metric Types (IEEE 11073)

| Code | Display |
|------|---------|
| 150456 | Heart rate |
| 150020 | SpO2 (oxygen saturation) |
| 150021 | Pulse rate |
| 150084 | Respiratory rate |
| 150016 | Blood pressure systolic |
| 150017 | Blood pressure diastolic |
| 160368 | Body temperature |
| 67996 | Battery level |

## Display Colors

| Code | Display |
|------|---------|
| black | Black |
| red | Red |
| green | Green |
| yellow | Yellow |
| blue | Blue |
| magenta | Magenta |
| cyan | Cyan |
| white | White |
