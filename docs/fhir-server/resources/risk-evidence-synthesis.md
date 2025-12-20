# RiskEvidenceSynthesis

## Overview

A RiskEvidenceSynthesis presents synthesized evidence about the risk of an outcome in a population. It provides statistical summaries of baseline risk from systematic reviews.

This resource is essential for risk assessment, prognostic modeling, and clinical decision support.

**Common use cases:**
- Baseline risk estimation
- Prognosis documentation
- Risk stratification
- Epidemiological summaries
- Guideline development

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/riskevidencesynthesis.html](https://hl7.org/fhir/R4/riskevidencesynthesis.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `url` | uri | Canonical identifier |
| `identifier` | Identifier[] | Business identifiers |
| `version` | string | Business version |
| `name` | string | Computer-friendly name |
| `title` | string | Human-friendly title |
| `status` | code | draft, active, retired, unknown (required) |
| `date` | dateTime | Date last changed |
| `publisher` | string | Publisher name |
| `description` | markdown | Natural language description |
| `population` | Reference(EvidenceVariable) | Population (required) |
| `exposure` | Reference(EvidenceVariable) | Exposure |
| `outcome` | Reference(EvidenceVariable) | Outcome (required) |
| `sampleSize` | BackboneElement | Sample size information |
| `riskEstimate` | BackboneElement | Risk estimate |
| `certainty` | BackboneElement[] | Certainty of evidence |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=stroke-risk` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/RiskEvidenceSynthesis/stroke` |
| `status` | token | Status | `status=active` |

## Examples

### Create a RiskEvidenceSynthesis

```bash
curl -X POST http://localhost:8080/baseR4/RiskEvidenceSynthesis \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "RiskEvidenceSynthesis",
    "url": "http://example.org/fhir/RiskEvidenceSynthesis/stroke-risk",
    "name": "StrokeRisk",
    "title": "10-Year Stroke Risk in Hypertensive Patients",
    "status": "active",
    "population": {"reference": "EvidenceVariable/hypertensive-adults"},
    "outcome": {"reference": "EvidenceVariable/ischemic-stroke"},
    "sampleSize": {
      "description": "Pooled cohort studies",
      "numberOfStudies": 8,
      "numberOfParticipants": 50000
    },
    "riskEstimate": {
      "description": "10-year risk of ischemic stroke",
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/risk-estimate-type",
          "code": "proportion"
        }]
      },
      "value": 0.15,
      "unitOfMeasure": {
        "system": "http://unitsofmeasure.org",
        "code": "1"
      },
      "precisionEstimate": [{
        "type": {
          "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/precision-estimate-type",
            "code": "CI"
          }]
        },
        "level": 0.95,
        "from": 0.12,
        "to": 0.18
      }]
    }
  }'
```

### Search RiskEvidenceSynthesis

```bash
# By status
curl "http://localhost:8080/baseR4/RiskEvidenceSynthesis?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import RiskEvidenceSynthesisGenerator

generator = RiskEvidenceSynthesisGenerator(seed=42)

# Generate random synthesis
synthesis = generator.generate()

# Generate with specific status
active = generator.generate(status="active")

# Generate batch
syntheses = generator.generate_batch(count=5)
```

## Related Resources

- [Evidence](./evidence.md) - Individual evidence
- [EvidenceVariable](./evidence-variable.md) - Variables referenced
- [EffectEvidenceSynthesis](./effect-evidence-synthesis.md) - Effect estimates
- [RiskAssessment](./risk-assessment.md) - Individual risk assessments
