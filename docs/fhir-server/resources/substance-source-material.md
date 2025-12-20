# SubstanceSourceMaterial

## Overview

A SubstanceSourceMaterial describes the source material from which a substance is derived. It provides information about the biological or geographical origin of materials used in pharmaceutical manufacturing.

This resource is essential for traceability and regulatory compliance in pharmaceutical manufacturing.

**Common use cases:**
- Biological source documentation
- Raw material traceability
- Regulatory compliance
- Quality control
- Supply chain documentation

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substancesourcematerial.html](https://hl7.org/fhir/R4/substancesourcematerial.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `sourceMaterialClass` | CodeableConcept | Source class |
| `sourceMaterialType` | CodeableConcept | Source type |
| `sourceMaterialState` | CodeableConcept | Source state |
| `organismId` | Identifier | Organism identifier |
| `organismName` | string | Organism name |
| `parentSubstanceId` | Identifier[] | Parent substance IDs |
| `parentSubstanceName` | string[] | Parent substance names |
| `countryOfOrigin` | CodeableConcept[] | Country of origin |
| `geographicalLocation` | string[] | Geographic location |
| `developmentStage` | CodeableConcept | Development stage |
| `fractionDescription` | BackboneElement[] | Fraction descriptions |
| `organism` | BackboneElement | Organism details |
| `partDescription` | BackboneElement[] | Part descriptions |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=source-001` |

## Examples

### Create a SubstanceSourceMaterial

```bash
curl -X POST http://localhost:8080/baseR4/SubstanceSourceMaterial \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstanceSourceMaterial",
    "sourceMaterialClass": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/source-material-class",
        "code": "animal",
        "display": "Animal"
      }]
    },
    "sourceMaterialType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/source-material-type",
        "code": "mammal",
        "display": "Mammalian"
      }]
    },
    "sourceMaterialState": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/source-material-state",
        "code": "fresh",
        "display": "Fresh"
      }]
    },
    "organismId": {
      "system": "http://www.ncbi.nlm.nih.gov/taxonomy",
      "value": "9606"
    },
    "organismName": "Homo sapiens",
    "countryOfOrigin": [{
      "coding": [{
        "system": "urn:iso:std:iso:3166",
        "code": "US",
        "display": "United States"
      }]
    }],
    "organism": {
      "family": {
        "coding": [{
          "system": "http://www.ncbi.nlm.nih.gov/taxonomy",
          "code": "9604",
          "display": "Hominidae"
        }]
      },
      "genus": {
        "coding": [{
          "system": "http://www.ncbi.nlm.nih.gov/taxonomy",
          "code": "9605",
          "display": "Homo"
        }]
      },
      "species": {
        "coding": [{
          "system": "http://www.ncbi.nlm.nih.gov/taxonomy",
          "code": "9606",
          "display": "Homo sapiens"
        }]
      }
    },
    "partDescription": [{
      "part": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "87612001",
          "display": "Blood"
        }]
      }
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstanceSourceMaterialGenerator

generator = SubstanceSourceMaterialGenerator(seed=42)

# Generate random source material
source = generator.generate()

# Generate batch
sources = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - Derived substances
- [SubstanceSpecification](./substance-specification.md) - Substance specifications
- [BiologicallyDerivedProduct](./biologically-derived-product.md) - Derived products
