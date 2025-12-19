# HealthcareService

## Overview

The HealthcareService resource describes the services provided by an organization at a location. It includes information about availability, specialties, and how to access the service.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/healthcareservice.html](https://hl7.org/fhir/R4/healthcareservice.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `active` | boolean | Whether the service is currently active |
| `providedBy` | Reference(Organization) | Organization providing the service |
| `category` | CodeableConcept[] | Broad category of service |
| `type` | CodeableConcept[] | Type of service |
| `specialty` | CodeableConcept[] | Specialties handled |
| `location` | Reference(Location)[] | Location(s) where service is provided |
| `name` | string | Service name |
| `comment` | string | Additional description |
| `telecom` | ContactPoint[] | Contact details |
| `serviceProvisionCode` | CodeableConcept[] | Conditions under which service is available |
| `program` | CodeableConcept[] | Programs/initiatives this service is part of |
| `characteristic` | CodeableConcept[] | Special characteristics |
| `referralMethod` | CodeableConcept[] | How to get referred |
| `appointmentRequired` | boolean | Whether appointment is required |
| `availableTime` | BackboneElement[] | Times the service is available |
| `notAvailable` | BackboneElement[] | Not available during these periods |
| `availabilityExceptions` | string | Availability exceptions description |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=hcs-001` |
| `active` | token | Active status | `active=true` |
| `name` | string | Service name | `name=Internal+Medicine` |
| `organization` | reference | Provider org | `organization=Organization/hosp-1` |
| `location` | reference | Location | `location=Location/clinic-1` |
| `service-category` | token | Category | `service-category=17` |
| `service-type` | token | Type | `service-type=394802001` |
| `specialty` | token | Specialty | `specialty=394814009` |

## Examples

### Create a HealthcareService

```bash
curl -X POST http://localhost:8080/baseR4/HealthcareService \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "HealthcareService",
    "active": true,
    "providedBy": {"reference": "Organization/hospital-1"},
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/service-category",
        "code": "17",
        "display": "General Practice"
      }]
    }],
    "type": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "394802001",
        "display": "General medicine"
      }]
    }],
    "specialty": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "394814009",
        "display": "General practice"
      }]
    }],
    "location": [{"reference": "Location/clinic-1"}],
    "name": "Internal Medicine Clinic",
    "comment": "Comprehensive internal medicine services",
    "telecom": [{
      "system": "phone",
      "value": "(555) 123-4567",
      "use": "work"
    }],
    "appointmentRequired": true,
    "availableTime": [{
      "daysOfWeek": ["mon", "tue", "wed", "thu", "fri"],
      "availableStartTime": "08:00:00",
      "availableEndTime": "17:00:00"
    }],
    "availabilityExceptions": "Closed on federal holidays"
  }'
```

### Search HealthcareServices

```bash
# Active services
curl "http://localhost:8080/baseR4/HealthcareService?active=true"

# By organization
curl "http://localhost:8080/baseR4/HealthcareService?organization=Organization/hospital-1"

# By specialty
curl "http://localhost:8080/baseR4/HealthcareService?specialty=394814009"

# By name
curl "http://localhost:8080/baseR4/HealthcareService?name=Internal+Medicine"
```

## Service Categories

| Code | Display |
|------|---------|
| 1 | Aged Care |
| 2 | Allied Health |
| 8 | Counseling |
| 9 | Dental |
| 17 | General Practice |
| 27 | Medical Specialists |
| 31 | Pharmacy |
| 35 | Radiology |
| 36 | Rehabilitation |

## Referral Methods

| Code | Display |
|------|---------|
| phone | Phone |
| fax | Fax |
| elec | Electronic |
| mail | Mail |
| semail | Secure Email |

## Days of Week

| Code | Display |
|------|---------|
| mon | Monday |
| tue | Tuesday |
| wed | Wednesday |
| thu | Thursday |
| fri | Friday |
| sat | Saturday |
| sun | Sunday |
