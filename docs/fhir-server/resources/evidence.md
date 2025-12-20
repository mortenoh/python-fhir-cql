# Evidence

## Overview

An Evidence resource describes clinical evidence that supports or refutes a claim. It provides a structured representation of research findings, statistical analyses, and scientific evidence.

This resource is essential for evidence-based medicine, clinical decision support, and research documentation.

**Common use cases:**
- Clinical evidence documentation
- Research findings representation
- Systematic reviews
- Clinical guideline support
- Decision support evidence

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/evidence.html](https://hl7.org/fhir/R4/evidence.html)

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
| `exposureBackground` | Reference(EvidenceVariable) | Background population (required) |
| `exposureVariant` | Reference(EvidenceVariable)[] | Exposure being compared |
| `outcome` | Reference(EvidenceVariable)[] | Outcome being evaluated |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=statin-cvd-evidence` |
| `url` | uri | Canonical URL | `url=http://example.org/fhir/Evidence/statin-benefit` |
| `status` | token | Status | `status=active` |
| `title` | string | Title | `title=Statin` |

## Examples

### Create an Evidence

```bash
curl -X POST http://localhost:8080/baseR4/Evidence \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Evidence",
    "url": "http://example.org/fhir/Evidence/aspirin-stroke-prevention",
    "name": "AspirinStrokePrevention",
    "title": "Aspirin for Stroke Prevention",
    "status": "active",
    "description": "Evidence for aspirin use in secondary stroke prevention",
    "exposureBackground": {
      "reference": "EvidenceVariable/stroke-patients"
    },
    "exposureVariant": [{
      "reference": "EvidenceVariable/aspirin-therapy"
    }],
    "outcome": [{
      "reference": "EvidenceVariable/recurrent-stroke"
    }]
  }'
```

### Search Evidence

```bash
# By status
curl "http://localhost:8080/baseR4/Evidence?status=active"

# By title
curl "http://localhost:8080/baseR4/Evidence?title:contains=aspirin"
```

## Generator Usage

```python
from fhirkit.server.generator import EvidenceGenerator

generator = EvidenceGenerator(seed=42)

# Generate random evidence
evidence = generator.generate()

# Generate with specific status
active_evidence = generator.generate(status="active")

# Generate batch
evidences = generator.generate_batch(count=10)
```

## Related Resources

- [EvidenceVariable](./evidence-variable.md) - Variables referenced
- [EffectEvidenceSynthesis](./effect-evidence-synthesis.md) - Synthesized evidence
- [ResearchDefinition](./research-definition.md) - Research definitions
