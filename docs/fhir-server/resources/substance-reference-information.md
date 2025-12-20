# SubstanceReferenceInformation

## Overview

A SubstanceReferenceInformation provides reference information about a substance, including gene sequences, targets, and classifications. It serves as a knowledge base for substance-related data.

This resource is essential for pharmaceutical knowledge management and drug development.

**Common use cases:**
- Drug target documentation
- Gene information
- Substance classification
- Pharmacological data
- Research documentation

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substancereferenceinformation.html](https://hl7.org/fhir/R4/substancereferenceinformation.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `comment` | string | General comments |
| `gene` | BackboneElement[] | Gene information |
| `gene.geneSequenceOrigin` | CodeableConcept | Gene sequence origin |
| `gene.gene` | CodeableConcept | Gene code |
| `gene.source` | Reference(DocumentReference)[] | Source documents |
| `geneElement` | BackboneElement[] | Gene element information |
| `geneElement.type` | CodeableConcept | Element type |
| `geneElement.element` | Identifier | Element identifier |
| `geneElement.source` | Reference(DocumentReference)[] | Source documents |
| `classification` | BackboneElement[] | Classification information |
| `target` | BackboneElement[] | Target information |
| `target.target` | Identifier | Target identifier |
| `target.type` | CodeableConcept | Target type |
| `target.interaction` | CodeableConcept | Interaction type |
| `target.organism` | CodeableConcept | Target organism |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=ref-info-001` |

## Examples

### Create a SubstanceReferenceInformation

```bash
curl -X POST http://localhost:8080/baseR4/SubstanceReferenceInformation \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstanceReferenceInformation",
    "comment": "Reference information for therapeutic antibody",
    "gene": [{
      "geneSequenceOrigin": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/gene-origin",
          "code": "human",
          "display": "Human"
        }]
      },
      "gene": {
        "coding": [{
          "system": "http://www.genenames.org",
          "code": "HGNC:9604",
          "display": "PDCD1"
        }]
      }
    }],
    "target": [{
      "target": {
        "system": "http://www.uniprot.org",
        "value": "Q15116"
      },
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/target-type",
          "code": "protein",
          "display": "Protein"
        }]
      },
      "interaction": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/interaction-type",
          "code": "antagonist",
          "display": "Antagonist"
        }]
      },
      "organism": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "278412004",
          "display": "Human"
        }]
      }
    }],
    "classification": [{
      "classification": {
        "coding": [{
          "system": "http://www.whocc.no/atc",
          "code": "L01XC",
          "display": "Monoclonal antibodies"
        }]
      }
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstanceReferenceInformationGenerator

generator = SubstanceReferenceInformationGenerator(seed=42)

# Generate random reference information
ref_info = generator.generate()

# Generate batch
ref_infos = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - General substance resource
- [SubstanceSpecification](./substance-specification.md) - Detailed specifications
- [DocumentReference](./document-reference.md) - Source documents
