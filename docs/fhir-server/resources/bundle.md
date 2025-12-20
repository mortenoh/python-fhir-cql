# Bundle

## Overview

The Bundle resource is a container for a collection of resources. It is used for returning search results, submitting transactions, creating documents, and sending messages.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/bundle.html](https://hl7.org/fhir/R4/bundle.html)

## Maturity Level

**Normative** - This resource is part of the normative FHIR specification.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `identifier` | Identifier | Persistent identifier |
| `type` | code | Bundle type (required) |
| `timestamp` | instant | When bundle was assembled |
| `total` | unsignedInt | Total for searchset |
| `link` | BackboneElement[] | Navigation links |
| `link.relation` | string | self \| first \| previous \| next \| last |
| `link.url` | uri | Reference URL |
| `entry` | BackboneElement[] | Entry in the bundle |
| `entry.link` | BackboneElement[] | Links for this entry |
| `entry.fullUrl` | uri | URI for resource |
| `entry.resource` | Resource | The resource in the entry |
| `entry.search` | BackboneElement | Search ranking info |
| `entry.request` | BackboneElement | Transaction request details |
| `entry.response` | BackboneElement | Transaction response details |
| `signature` | Signature | Digital signature |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=bundle-001` |
| `type` | token | Bundle type | `type=searchset` |
| `identifier` | token | Bundle identifier | `identifier=doc-123` |
| `timestamp` | date | When assembled | `timestamp=ge2024-01-01` |
| `composition` | reference | First resource if document | `composition=Composition/comp-1` |
| `message` | reference | First resource if message | `message=MessageHeader/msg-1` |

## Examples

### Create a Collection Bundle

```bash
curl -X POST http://localhost:8080/baseR4/Bundle \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Bundle",
    "type": "collection",
    "timestamp": "2024-01-15T10:30:00Z",
    "entry": [
      {
        "fullUrl": "urn:uuid:patient-1",
        "resource": {
          "resourceType": "Patient",
          "id": "patient-1",
          "name": [{"family": "Smith", "given": ["John"]}]
        }
      },
      {
        "fullUrl": "urn:uuid:condition-1",
        "resource": {
          "resourceType": "Condition",
          "id": "condition-1",
          "subject": {"reference": "Patient/patient-1"},
          "code": {"text": "Diabetes"}
        }
      }
    ]
  }'
```

### Create a Transaction Bundle

```bash
curl -X POST http://localhost:8080/baseR4 \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
      {
        "fullUrl": "urn:uuid:new-patient",
        "resource": {
          "resourceType": "Patient",
          "name": [{"family": "Doe", "given": ["Jane"]}]
        },
        "request": {
          "method": "POST",
          "url": "Patient"
        }
      }
    ]
  }'
```

### Search Bundles

```bash
# By type
curl "http://localhost:8080/baseR4/Bundle?type=document"

# By timestamp
curl "http://localhost:8080/baseR4/Bundle?timestamp=ge2024-01-01"

# By identifier
curl "http://localhost:8080/baseR4/Bundle?identifier=doc-123"
```

## Generator

The `BundleGenerator` creates synthetic Bundle resources.

### Usage

```python
from fhirkit.server.generator import BundleGenerator, PatientGenerator

bundle_gen = BundleGenerator(seed=42)
patient_gen = PatientGenerator(seed=42)

# Generate a collection bundle
patients = patient_gen.generate_batch(count=5)
bundle = bundle_gen.generate(
    bundle_type="collection",
    entries=patients
)

# Generate a searchset bundle
bundle = bundle_gen.generate_searchset(
    resources=patients,
    total=100,
    self_link="http://example.org/Patient?_count=5",
    next_link="http://example.org/Patient?_count=5&_offset=5"
)

# Generate a transaction bundle
bundle = bundle_gen.generate_transaction(resources=patients)
```

## Bundle Types

| Type | Description |
|------|-------------|
| document | Clinical document |
| message | FHIR message |
| transaction | Database transaction |
| transaction-response | Response to transaction |
| batch | Batch of requests |
| batch-response | Response to batch |
| history | Version history |
| searchset | Search results |
| collection | Collection of resources |
