# SubstanceNucleicAcid

## Overview

A SubstanceNucleicAcid describes a nucleic acid substance including DNA and RNA. It provides detailed structural information about nucleic acid sequences used in research and pharmaceutical development.

This resource is essential for biological substance definition and pharmaceutical research.

**Common use cases:**
- Gene therapy products
- mRNA vaccine definitions
- Nucleic acid drug substances
- Research reagent documentation
- Oligonucleotide specifications

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substancenucleicacid.html](https://hl7.org/fhir/R4/substancenucleicacid.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `sequenceType` | CodeableConcept | DNA, RNA, or other |
| `numberOfSubunits` | integer | Number of subunits |
| `areaOfHybridisation` | string | Area of hybridisation |
| `oligoNucleotideType` | CodeableConcept | Oligo type |
| `subunit` | BackboneElement[] | Subunit details |
| `subunit.subunit` | integer | Subunit number |
| `subunit.sequence` | string | Nucleotide sequence |
| `subunit.length` | integer | Sequence length |
| `subunit.sequenceAttachment` | Attachment | Sequence file |
| `subunit.fivePrime` | CodeableConcept | 5' modification |
| `subunit.threePrime` | CodeableConcept | 3' modification |
| `subunit.linkage` | BackboneElement[] | Linkage information |
| `subunit.sugar` | BackboneElement[] | Sugar modifications |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=mrna-001` |

## Examples

### Create a SubstanceNucleicAcid

```bash
curl -X POST http://localhost:8080/baseR4/SubstanceNucleicAcid \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstanceNucleicAcid",
    "sequenceType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/sequence-type",
        "code": "RNA",
        "display": "RNA"
      }]
    },
    "numberOfSubunits": 1,
    "oligoNucleotideType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/oligo-type",
        "code": "AS",
        "display": "Antisense"
      }]
    },
    "subunit": [{
      "subunit": 1,
      "sequence": "AUGCUAGCUAGCUAGCUAG",
      "length": 19,
      "fivePrime": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/five-prime-nucleotide",
          "code": "cap",
          "display": "5-prime cap"
        }]
      }
    }]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstanceNucleicAcidGenerator

generator = SubstanceNucleicAcidGenerator(seed=42)

# Generate random nucleic acid
nucleic_acid = generator.generate()

# Generate batch
nucleic_acids = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - General substance resource
- [SubstanceSpecification](./substance-specification.md) - Detailed specifications
- [MedicationKnowledge](./medication-knowledge.md) - Medication knowledge
