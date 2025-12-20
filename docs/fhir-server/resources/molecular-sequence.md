# MolecularSequence

## Overview

A MolecularSequence resource describes a genetic sequence including DNA, RNA, or amino acid sequences. It provides a structured representation of genomic data with quality metrics and variant information.

This resource is essential for genomic medicine, genetic testing, and precision medicine applications.

**Common use cases:**
- Genetic test results
- Variant documentation
- Genomic sequencing data
- Pharmacogenomics
- Cancer genomics

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/molecularsequence.html](https://hl7.org/fhir/R4/molecularsequence.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `identifier` | Identifier[] | Business identifiers |
| `type` | code | aa, dna, rna |
| `coordinateSystem` | integer | Coordinate system (0 or 1) (required) |
| `patient` | Reference(Patient) | Patient reference |
| `specimen` | Reference(Specimen) | Specimen used |
| `device` | Reference(Device) | Sequencing device |
| `performer` | Reference(Organization) | Lab performing test |
| `quantity` | Quantity | Quantity of the sequence |
| `referenceSeq` | BackboneElement | Reference sequence |
| `variant` | BackboneElement[] | Variant information |
| `observedSeq` | string | Observed sequence |
| `quality` | BackboneElement[] | Quality scores |
| `readCoverage` | integer | Average read depth |
| `repository` | BackboneElement[] | External repositories |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=seq-001` |
| `identifier` | token | Sequence identifier | `identifier=SEQ-12345` |
| `patient` | reference | Patient reference | `patient=Patient/123` |
| `type` | token | Sequence type | `type=dna` |

## Examples

### Create a MolecularSequence

```bash
curl -X POST http://localhost:8080/baseR4/MolecularSequence \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MolecularSequence",
    "identifier": [{
      "system": "http://example.org/sequences",
      "value": "SEQ-2024-001"
    }],
    "type": "dna",
    "coordinateSystem": 0,
    "patient": {"reference": "Patient/123"},
    "specimen": {"reference": "Specimen/blood-sample-001"},
    "referenceSeq": {
      "chromosome": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/chromosome-human",
          "code": "7"
        }]
      },
      "genomeBuild": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "LA26806-2",
          "display": "GRCh38"
        }]
      },
      "referenceSeqId": {
        "coding": [{
          "system": "http://www.ncbi.nlm.nih.gov/nuccore",
          "code": "NC_000007.14"
        }]
      },
      "windowStart": 117120016,
      "windowEnd": 117120216
    },
    "variant": [{
      "start": 117120148,
      "end": 117120149,
      "observedAllele": "T",
      "referenceAllele": "G",
      "cigar": "1M"
    }],
    "quality": [{
      "type": "snp",
      "standardSequence": {
        "coding": [{
          "system": "http://www.ncbi.nlm.nih.gov/projects/SNP",
          "code": "rs113488022"
        }]
      },
      "score": {"value": 99.5}
    }]
  }'
```

### Search MolecularSequences

```bash
# By patient
curl "http://localhost:8080/baseR4/MolecularSequence?patient=Patient/123"

# By type
curl "http://localhost:8080/baseR4/MolecularSequence?type=dna"
```

## Generator Usage

```python
from fhirkit.server.generator import MolecularSequenceGenerator

generator = MolecularSequenceGenerator(seed=42)

# Generate random sequence
sequence = generator.generate()

# Generate DNA sequence
dna = generator.generate(type="dna")

# Generate batch
sequences = generator.generate_batch(count=10)
```

## Type Codes

| Code | Description |
|------|-------------|
| aa | Amino acid sequence |
| dna | DNA sequence |
| rna | RNA sequence |

## Related Resources

- [Patient](./patient.md) - Patient with genetic data
- [Specimen](./specimen.md) - Specimen tested
- [Observation](./observation.md) - Genetic observations
- [DiagnosticReport](./diagnostic-report.md) - Genetic test reports
