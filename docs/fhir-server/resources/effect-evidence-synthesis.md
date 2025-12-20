# EffectEvidenceSynthesis

## Overview

An EffectEvidenceSynthesis presents synthesized evidence about the effect of an exposure on an outcome. It provides statistical summaries from systematic reviews and meta-analyses.

This resource is essential for evidence-based decision making and clinical guideline development.

**Common use cases:**
- Meta-analysis results
- Systematic review summaries
- Treatment effect estimates
- Risk-benefit analysis
- Guideline development

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/effectevidencesynthesis.html](https://hl7.org/fhir/R4/effectevidencesynthesis.html)

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
| `population` | Reference(EvidenceVariable) | Population studied (required) |
| `exposure` | Reference(EvidenceVariable) | Exposure/intervention (required) |
| `exposureAlternative` | Reference(EvidenceVariable) | Comparison exposure |
| `outcome` | Reference(EvidenceVariable) | Outcome measured (required) |
| `sampleSize` | BackboneElement | Sample size information |
| `resultsByExposure` | BackboneElement[] | Results by exposure |
| `effectEstimate` | BackboneElement[] | Effect estimates |
| `certainty` | BackboneElement[] | Certainty of evidence |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=statin-mortality` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/EffectEvidenceSynthesis/statins` |
| `status` | token | Status | `status=active` |

## Examples

### Create an EffectEvidenceSynthesis

```bash
curl -X POST http://localhost:8080/baseR4/EffectEvidenceSynthesis \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "EffectEvidenceSynthesis",
    "url": "http://example.org/fhir/EffectEvidenceSynthesis/aspirin-mi",
    "name": "AspirinMIEffect",
    "title": "Aspirin Effect on Myocardial Infarction",
    "status": "active",
    "population": {"reference": "EvidenceVariable/high-cvd-risk"},
    "exposure": {"reference": "EvidenceVariable/aspirin-therapy"},
    "exposureAlternative": {"reference": "EvidenceVariable/placebo"},
    "outcome": {"reference": "EvidenceVariable/myocardial-infarction"},
    "sampleSize": {
      "description": "Pooled analysis of 5 RCTs",
      "numberOfStudies": 5,
      "numberOfParticipants": 10000
    },
    "effectEstimate": [{
      "description": "Relative Risk of MI",
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/effect-estimate-type",
          "code": "relative-RR"
        }]
      },
      "value": 0.78,
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
        "from": 0.65,
        "to": 0.92
      }]
    }]
  }'
```

### Search EffectEvidenceSynthesis

```bash
# By status
curl "http://localhost:8080/baseR4/EffectEvidenceSynthesis?status=active"
```

## Generator Usage

```python
from fhirkit.server.generator import EffectEvidenceSynthesisGenerator

generator = EffectEvidenceSynthesisGenerator(seed=42)

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
- [RiskEvidenceSynthesis](./risk-evidence-synthesis.md) - Risk estimates
