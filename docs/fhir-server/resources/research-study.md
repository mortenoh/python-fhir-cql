# ResearchStudy

## Overview

The ResearchStudy resource describes a clinical trial or research study. It captures study details including phases, objectives, eligibility criteria, and study arms.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/researchstudy.html](https://hl7.org/fhir/R4/researchstudy.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier[] | Business identifiers (NCT number, etc.) |
| `title` | string | Study title |
| `protocol` | Reference(PlanDefinition)[] | Study protocol |
| `partOf` | Reference(ResearchStudy)[] | Parent study |
| `status` | code | Study status |
| `primaryPurposeType` | CodeableConcept | Primary purpose |
| `phase` | CodeableConcept | Study phase |
| `category` | CodeableConcept[] | Study category |
| `focus` | CodeableConcept[] | Focus of study |
| `condition` | CodeableConcept[] | Conditions being studied |
| `contact` | ContactDetail[] | Study contacts |
| `relatedArtifact` | RelatedArtifact[] | Related documents |
| `keyword` | CodeableConcept[] | Keywords |
| `location` | CodeableConcept[] | Study locations |
| `description` | markdown | Study description |
| `enrollment` | Reference(Group)[] | Enrollment target |
| `period` | Period | Study period |
| `sponsor` | Reference(Organization) | Sponsor |
| `principalInvestigator` | Reference(Practitioner) | Lead investigator |
| `site` | Reference(Location)[] | Study sites |
| `reasonStopped` | CodeableConcept | Why stopped |
| `note` | Annotation[] | Notes |
| `arm` | BackboneElement[] | Study arms |
| `objective` | BackboneElement[] | Study objectives |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=rs-001` |
| `identifier` | token | Business identifier | `identifier=NCT12345678` |
| `title` | string | Study title | `title=diabetes` |
| `status` | token | Study status | `status=active` |
| `phase` | token | Study phase | `phase=phase-3` |
| `category` | token | Study category | `category=interventional` |
| `condition` | token | Condition studied | `condition=44054006` |
| `date` | date | Study period | `date=ge2024-01-01` |
| `sponsor` | reference | Sponsor | `sponsor=Organization/456` |
| `principalinvestigator` | reference | Lead investigator | `principalinvestigator=Practitioner/789` |
| `site` | reference | Study site | `site=Location/loc-001` |

## Examples

### Create a ResearchStudy

```bash
curl -X POST http://localhost:8080/baseR4/ResearchStudy \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "ResearchStudy",
    "identifier": [{
      "system": "http://clinicaltrials.gov",
      "value": "NCT12345678"
    }],
    "title": "Efficacy of Novel Diabetes Treatment in Adults",
    "status": "active",
    "primaryPurposeType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        "code": "treatment",
        "display": "Treatment"
      }]
    },
    "phase": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        "code": "phase-3",
        "display": "Phase 3"
      }]
    },
    "category": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/research-study-category",
        "code": "interventional",
        "display": "Interventional"
      }]
    }],
    "condition": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "44054006",
        "display": "Type 2 diabetes mellitus"
      }]
    }],
    "description": "A Phase 3 interventional study investigating Type 2 diabetes mellitus.",
    "enrollment": [{
      "display": "Target enrollment: 250 participants"
    }],
    "period": {
      "start": "2024-01-01"
    },
    "sponsor": {
      "reference": "Organization/organization-001"
    },
    "principalInvestigator": {
      "reference": "Practitioner/practitioner-001"
    },
    "arm": [
      {
        "name": "Treatment Arm",
        "type": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/research-study-arm-type",
            "code": "experimental",
            "display": "Experimental"
          }]
        },
        "description": "Receives novel diabetes treatment"
      },
      {
        "name": "Control Arm",
        "type": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/research-study-arm-type",
            "code": "placebo-comparator",
            "display": "Placebo Comparator"
          }]
        },
        "description": "Receives placebo"
      }
    ],
    "objective": [{
      "name": "Primary Objective",
      "type": {
        "coding": [{
          "code": "primary",
          "display": "Primary"
        }]
      }
    }]
  }'
```

### Search ResearchStudies

```bash
# By status
curl "http://localhost:8080/baseR4/ResearchStudy?status=active"

# By phase
curl "http://localhost:8080/baseR4/ResearchStudy?phase=phase-3"

# By condition
curl "http://localhost:8080/baseR4/ResearchStudy?condition=44054006"

# By identifier (NCT number)
curl "http://localhost:8080/baseR4/ResearchStudy?identifier=NCT12345678"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| active | Active | Study is active |
| administratively-completed | Administratively Completed | Study administratively completed |
| approved | Approved | Study approved |
| closed-to-accrual | Closed to Accrual | Not accepting new subjects |
| closed-to-accrual-and-intervention | Closed to Accrual and Intervention | Closed |
| completed | Completed | Study completed |
| disapproved | Disapproved | Study disapproved |
| in-review | In Review | Under review |
| temporarily-closed-to-accrual | Temporarily Closed | Temporarily not accepting |
| temporarily-closed-to-accrual-and-intervention | Temporarily Closed | Temporarily closed |
| withdrawn | Withdrawn | Study withdrawn |

## Study Phases

| Code | Display |
|------|---------|
| n-a | N/A |
| early-phase-1 | Early Phase 1 |
| phase-1 | Phase 1 |
| phase-1-phase-2 | Phase 1/Phase 2 |
| phase-2 | Phase 2 |
| phase-2-phase-3 | Phase 2/Phase 3 |
| phase-3 | Phase 3 |
| phase-4 | Phase 4 |

## Study Categories

| Code | Display |
|------|---------|
| interventional | Interventional |
| observational | Observational |
| expanded-access | Expanded Access |

## Primary Purpose Types

| Code | Display |
|------|---------|
| treatment | Treatment |
| prevention | Prevention |
| diagnostic | Diagnostic |
| supportive-care | Supportive Care |
| screening | Screening |
| health-services-research | Health Services Research |
| basic-science | Basic Science |
| device-feasibility | Device Feasibility |

## Arm Types

| Code | Display |
|------|---------|
| experimental | Experimental |
| active-comparator | Active Comparator |
| placebo-comparator | Placebo Comparator |
| sham-comparator | Sham Comparator |
| no-intervention | No Intervention |
| other | Other |
