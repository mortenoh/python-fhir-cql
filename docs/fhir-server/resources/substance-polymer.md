# SubstancePolymer

## Overview

A SubstancePolymer describes a polymer substance including its structural characteristics. It provides detailed information about polymer materials used in pharmaceutical and medical applications.

This resource is essential for pharmaceutical polymer documentation and material science.

**Common use cases:**
- Drug delivery polymers
- Medical device materials
- Excipient documentation
- Coating materials
- Biodegradable polymers

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substancepolymer.html](https://hl7.org/fhir/R4/substancepolymer.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `class` | CodeableConcept | Polymer class |
| `geometry` | CodeableConcept | Polymer geometry |
| `copolymerConnectivity` | CodeableConcept[] | Copolymer connectivity |
| `modification` | string[] | Modifications |
| `monomerSet` | BackboneElement[] | Monomer sets |
| `monomerSet.ratioType` | CodeableConcept | Ratio type |
| `monomerSet.startingMaterial` | BackboneElement[] | Starting materials |
| `repeat` | BackboneElement[] | Repeat units |
| `repeat.numberOfUnits` | integer | Number of units |
| `repeat.averageMolecularFormula` | string | Average formula |
| `repeat.repeatUnitAmountType` | CodeableConcept | Amount type |
| `repeat.repeatUnit` | BackboneElement[] | Repeat unit structure |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=polymer-001` |

## Examples

### Create a SubstancePolymer

```bash
curl -X POST http://localhost:8080/baseR4/SubstancePolymer \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstancePolymer",
    "class": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/polymer-class",
        "code": "polysaccharide",
        "display": "Polysaccharide"
      }]
    },
    "geometry": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/polymer-geometry",
        "code": "linear",
        "display": "Linear"
      }]
    },
    "monomerSet": [{
      "ratioType": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/ratio-type",
          "code": "molar",
          "display": "Molar ratio"
        }]
      }
    }],
    "repeat": [{
      "numberOfUnits": 100,
      "averageMolecularFormula": "(C6H10O5)n"
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstancePolymerGenerator

generator = SubstancePolymerGenerator(seed=42)

# Generate random polymer
polymer = generator.generate()

# Generate batch
polymers = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - General substance resource
- [SubstanceSpecification](./substance-specification.md) - Detailed specifications
