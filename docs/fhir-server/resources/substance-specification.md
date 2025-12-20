# SubstanceSpecification

## Overview

A SubstanceSpecification provides detailed technical specifications for a substance, including its molecular structure, properties, and relationships to other substances.

This resource is essential for pharmaceutical substance documentation and regulatory submissions.

**Common use cases:**
- Drug substance specifications
- Molecular structure documentation
- Impurity profiling
- Regulatory submissions
- Quality standards

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substancespecification.html](https://hl7.org/fhir/R4/substancespecification.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier | Business identifier |
| `type` | CodeableConcept | Substance type |
| `status` | CodeableConcept | Status |
| `domain` | CodeableConcept | Domain (human, veterinary) |
| `description` | string | Description |
| `source` | Reference(DocumentReference)[] | Source documents |
| `comment` | string | Comments |
| `moiety` | BackboneElement[] | Moiety information |
| `property` | BackboneElement[] | Properties |
| `referenceInformation` | Reference(SubstanceReferenceInformation) | Reference info |
| `structure` | BackboneElement | Structural information |
| `code` | BackboneElement[] | Codes and identifiers |
| `name` | BackboneElement[] | Names |
| `molecularWeight` | BackboneElement[] | Molecular weight |
| `relationship` | BackboneElement[] | Relationships |
| `nucleicAcid` | Reference(SubstanceNucleicAcid) | Nucleic acid details |
| `polymer` | Reference(SubstancePolymer) | Polymer details |
| `protein` | Reference(SubstanceProtein) | Protein details |
| `sourceMaterial` | Reference(SubstanceSourceMaterial) | Source material |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=aspirin-spec` |
| `code` | token | Substance code | `code=http://www.cas.org\|50-78-2` |

## Examples

### Create a SubstanceSpecification

```bash
curl -X POST http://localhost:8080/baseR4/SubstanceSpecification \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstanceSpecification",
    "identifier": {
      "system": "http://example.org/substances",
      "value": "ASPIRIN-001"
    },
    "type": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/substance-type",
        "code": "chemical",
        "display": "Chemical"
      }]
    },
    "status": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/substance-status",
        "code": "active"
      }]
    },
    "domain": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/substance-domain",
        "code": "human",
        "display": "Human use"
      }]
    },
    "description": "Acetylsalicylic acid, a non-steroidal anti-inflammatory drug",
    "structure": {
      "molecularFormula": "C9H8O4",
      "molecularFormulaByMoiety": "C9H8O4"
    },
    "code": [{
      "code": {
        "coding": [{
          "system": "http://www.cas.org",
          "code": "50-78-2"
        }]
      }
    }],
    "name": [{
      "name": "Aspirin",
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/substance-name-type",
          "code": "scientific"
        }]
      },
      "preferred": true
    }, {
      "name": "Acetylsalicylic acid",
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/substance-name-type",
          "code": "systematic"
        }]
      }
    }],
    "molecularWeight": [{
      "amount": {
        "value": 180.16,
        "unit": "g/mol"
      }
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstanceSpecificationGenerator

generator = SubstanceSpecificationGenerator(seed=42)

# Generate random specification
spec = generator.generate()

# Generate batch
specs = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - General substance resource
- [SubstanceNucleicAcid](./substance-nucleic-acid.md) - Nucleic acid details
- [SubstancePolymer](./substance-polymer.md) - Polymer details
- [SubstanceProtein](./substance-protein.md) - Protein details
- [SubstanceSourceMaterial](./substance-source-material.md) - Source material
- [SubstanceReferenceInformation](./substance-reference-information.md) - Reference info
