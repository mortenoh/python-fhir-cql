# OrganizationAffiliation

## Overview

The OrganizationAffiliation resource describes relationships between organizations, such as when one organization provides services to another, or when organizations belong to a network. It captures the nature of the affiliation, participating roles, and applicable services.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/organizationaffiliation.html](https://hl7.org/fhir/R4/organizationaffiliation.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers |
| `active` | boolean | Whether affiliation is active |
| `period` | Period | Affiliation period |
| `organization` | Reference(Organization) | Parent organization |
| `participatingOrganization` | Reference(Organization) | Organization providing services |
| `network` | Reference(Organization)[] | Network(s) |
| `code` | CodeableConcept[] | Affiliation role codes |
| `specialty` | CodeableConcept[] | Specialties |
| `location` | Reference(Location)[] | Service locations |
| `healthcareService` | Reference(HealthcareService)[] | Services provided |
| `telecom` | ContactPoint[] | Contact details |
| `endpoint` | Reference(Endpoint)[] | Endpoints |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=oa-001` |
| `identifier` | token | Business identifier | `identifier=AFF-12345` |
| `active` | token | Active status | `active=true` |
| `date` | date | Affiliation period | `date=ge2024-01-01` |
| `email` | token | Email contact | `email=admin@hospital.org` |
| `endpoint` | reference | Endpoint | `endpoint=Endpoint/ep-001` |
| `location` | reference | Location | `location=Location/loc-001` |
| `network` | reference | Network | `network=Organization/network-001` |
| `participating-organization` | reference | Participating org | `participating-organization=Organization/456` |
| `phone` | token | Phone contact | `phone=555-1234` |
| `primary-organization` | reference | Primary org | `primary-organization=Organization/123` |
| `role` | token | Affiliation role | `role=provider` |
| `service` | reference | Service | `service=HealthcareService/hs-001` |
| `specialty` | token | Specialty | `specialty=394802001` |

## Examples

### Create an OrganizationAffiliation

```bash
curl -X POST http://localhost:8080/baseR4/OrganizationAffiliation \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "OrganizationAffiliation",
    "identifier": [{
      "system": "http://example.org/affiliation-ids",
      "value": "AFF-001"
    }],
    "active": true,
    "period": {
      "start": "2024-01-01"
    },
    "organization": {
      "reference": "Organization/hospital-network"
    },
    "participatingOrganization": {
      "reference": "Organization/community-clinic"
    },
    "code": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/organization-role",
        "code": "provider",
        "display": "Provider"
      }]
    }],
    "specialty": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "394802001",
        "display": "General medicine"
      }]
    }],
    "location": [{
      "reference": "Location/clinic-location"
    }],
    "telecom": [{
      "system": "phone",
      "value": "555-1234",
      "use": "work"
    }]
  }'
```

### Create a Network Member Affiliation

```bash
curl -X POST http://localhost:8080/baseR4/OrganizationAffiliation \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "OrganizationAffiliation",
    "active": true,
    "organization": {
      "reference": "Organization/insurance-network"
    },
    "participatingOrganization": {
      "reference": "Organization/participating-hospital"
    },
    "network": [{
      "reference": "Organization/preferred-provider-network"
    }],
    "code": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/organization-role",
        "code": "member",
        "display": "Member"
      }]
    }],
    "healthcareService": [{
      "reference": "HealthcareService/hs-primary-care"
    }]
  }'
```

### Search OrganizationAffiliations

```bash
# By primary organization
curl "http://localhost:8080/baseR4/OrganizationAffiliation?primary-organization=Organization/123"

# By participating organization
curl "http://localhost:8080/baseR4/OrganizationAffiliation?participating-organization=Organization/456"

# By role
curl "http://localhost:8080/baseR4/OrganizationAffiliation?role=provider"

# Active affiliations
curl "http://localhost:8080/baseR4/OrganizationAffiliation?active=true"

# By network
curl "http://localhost:8080/baseR4/OrganizationAffiliation?network=Organization/network-001"
```

## Affiliation Role Codes

| Code | Display | Description |
|------|---------|-------------|
| provider | Provider | Provides healthcare services |
| agency | Agency | Contracted agency |
| research | Research | Research organization |
| payer | Payer | Insurance/payer |
| diagnostics | Diagnostics | Diagnostic services |
| supplier | Supplier | Supplies goods |
| HIE/HIO | HIE/HIO | Health information exchange |
| member | Member | Network member |

## Common Specialties (SNOMED CT)

| Code | Display |
|------|---------|
| 394802001 | General medicine |
| 394579002 | Cardiology |
| 394591006 | Neurology |
| 394585009 | Obstetrics and gynecology |
| 394587001 | Psychiatry |
| 394609007 | Surgery |
| 408443003 | General medical practice |
| 419772000 | Family practice |

## Use Cases

### Hospital Network Membership
```
Organization A (hospital network) --> participatingOrganization: Organization B (hospital)
Role: member
```

### Provider Credentialing
```
Organization A (hospital) --> participatingOrganization: Organization B (medical group)
Role: provider
Specialty: Cardiology
```

### Insurance Network
```
Organization A (insurance plan) --> participatingOrganization: Organization B (provider)
Network: Preferred Provider Network
Role: member
```

### Research Collaboration
```
Organization A (research institution) --> participatingOrganization: Organization B (hospital)
Role: research
```
