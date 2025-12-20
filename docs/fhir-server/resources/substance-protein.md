# SubstanceProtein

## Overview

A SubstanceProtein describes a protein substance including its sequence and structural characteristics. It provides detailed information about protein-based therapeutics and biological materials.

This resource is essential for biopharmaceutical development and protein characterization.

**Common use cases:**
- Therapeutic proteins
- Antibody documentation
- Enzyme characterization
- Vaccine antigens
- Recombinant proteins

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/substanceprotein.html](https://hl7.org/fhir/R4/substanceprotein.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `sequenceType` | CodeableConcept | Protein type |
| `numberOfSubunits` | integer | Number of subunits |
| `disulfideLinkage` | string[] | Disulfide linkages |
| `subunit` | BackboneElement[] | Subunit information |
| `subunit.subunit` | integer | Subunit number |
| `subunit.sequence` | string | Amino acid sequence |
| `subunit.length` | integer | Sequence length |
| `subunit.sequenceAttachment` | Attachment | Sequence file |
| `subunit.nTerminalModificationId` | Identifier | N-terminal modification |
| `subunit.nTerminalModification` | string | N-terminal modification description |
| `subunit.cTerminalModificationId` | Identifier | C-terminal modification |
| `subunit.cTerminalModification` | string | C-terminal modification description |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=antibody-001` |

## Examples

### Create a SubstanceProtein

```bash
curl -X POST http://localhost:8080/baseR4/SubstanceProtein \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SubstanceProtein",
    "sequenceType": {
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/protein-type",
        "code": "antibody",
        "display": "Antibody"
      }]
    },
    "numberOfSubunits": 4,
    "disulfideLinkage": [
      "HC1:Cys-22 to LC1:Cys-88",
      "HC1:Cys-96 to HC1:Cys-147"
    ],
    "subunit": [
      {
        "subunit": 1,
        "sequence": "EVQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSS",
        "length": 121,
        "nTerminalModification": "Pyroglutamate"
      },
      {
        "subunit": 2,
        "sequence": "DIQMTQSPSSLSASVGDRVTITCRASQGIRNDLGWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCLQHNSYPLTFGQGTKVEIK",
        "length": 107
      }
    ]
  }'
```

## Generator Usage

```python
from fhirkit.server.generator import SubstanceProteinGenerator

generator = SubstanceProteinGenerator(seed=42)

# Generate random protein
protein = generator.generate()

# Generate batch
proteins = generator.generate_batch(count=5)
```

## Related Resources

- [Substance](./substance.md) - General substance resource
- [SubstanceSpecification](./substance-specification.md) - Detailed specifications
- [MedicationKnowledge](./medication-knowledge.md) - Medication knowledge
