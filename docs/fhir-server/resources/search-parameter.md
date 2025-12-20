# SearchParameter

## Overview

The SearchParameter resource defines a search parameter that can be used in searches against a FHIR server. It describes how to query resources and what values to match against.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/searchparameter.html](https://hl7.org/fhir/R4/searchparameter.html)

## Maturity Level

**FMM 3** - This resource is considered stable for trial use.

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `url` | uri | Canonical identifier (required) |
| `version` | string | Business version |
| `name` | string | Computer-friendly name (required) |
| `derivedFrom` | canonical | Original definition |
| `status` | code | draft \| active \| retired \| unknown (required) |
| `experimental` | boolean | For testing purposes |
| `date` | dateTime | Date published |
| `publisher` | string | Publisher name |
| `contact` | ContactDetail[] | Contact details |
| `description` | markdown | Natural language description (required) |
| `useContext` | UsageContext[] | Context of use |
| `jurisdiction` | CodeableConcept[] | Jurisdictions |
| `purpose` | markdown | Why defined |
| `code` | code | URL code (required) |
| `base` | code[] | Resource types (required) |
| `type` | code | Parameter type (required) |
| `expression` | string | FHIRPath expression |
| `xpath` | string | XPath expression |
| `xpathUsage` | code | XPath usage mode |
| `target` | code[] | Target resources (for reference types) |
| `multipleOr` | boolean | Support OR logic |
| `multipleAnd` | boolean | Support AND logic |
| `comparator` | code[] | Supported comparators |
| `modifier` | code[] | Supported modifiers |
| `chain` | string[] | Chained parameters |
| `component` | BackboneElement[] | For composite parameters |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=sp-001` |
| `url` | uri | Canonical URL | `url=http://example.org/sp` |
| `name` | string | Name | `name=patient-name` |
| `code` | token | Parameter code | `code=name` |
| `base` | token | Resource type | `base=Patient` |
| `type` | token | Parameter type | `type=string` |
| `status` | token | Status | `status=active` |
| `version` | token | Version | `version=1.0.0` |
| `publisher` | string | Publisher | `publisher=HL7` |
| `description` | string | Description | `description=search` |
| `date` | date | Publication date | `date=ge2024-01-01` |
| `target` | token | Target type | `target=Organization` |
| `derived-from` | reference | Base parameter | `derived-from=SearchParameter/base` |

## Examples

### Create a SearchParameter

```bash
curl -X POST http://localhost:8080/baseR4/SearchParameter \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "SearchParameter",
    "url": "http://example.org/fhir/SearchParameter/patient-mrn",
    "version": "1.0.0",
    "name": "patient-mrn",
    "status": "active",
    "description": "Search Patient by MRN identifier",
    "code": "mrn",
    "base": ["Patient"],
    "type": "token",
    "expression": "Patient.identifier.where(type.coding.code = '\''MR'\'')",
    "multipleOr": true,
    "multipleAnd": true
  }'
```

### Search SearchParameters

```bash
# By base resource type
curl "http://localhost:8080/baseR4/SearchParameter?base=Patient"

# By type
curl "http://localhost:8080/baseR4/SearchParameter?type=reference"

# Active parameters
curl "http://localhost:8080/baseR4/SearchParameter?status=active"

# By code
curl "http://localhost:8080/baseR4/SearchParameter?code=name"
```

## Generator

The `SearchParameterGenerator` creates synthetic SearchParameter resources.

### Usage

```python
from fhirkit.server.generator import SearchParameterGenerator

generator = SearchParameterGenerator(seed=42)

# Generate a search parameter
param = generator.generate(
    name="custom-param",
    code="custom",
    param_type="token",
    base=["Patient"]
)

# Generate for a specific resource field
param = generator.generate_for_resource(
    resource_type="Patient",
    field_name="birthDate",
    param_type="date"
)
```

## Parameter Types

| Type | Description | Example |
|------|-------------|---------|
| number | Numeric value | Age |
| date | Date/DateTime | Birth date |
| string | Text search | Name |
| token | Code/Identifier | Status |
| reference | Resource reference | Patient |
| composite | Combined parameters | Code + date |
| quantity | Numeric with units | Weight |
| uri | URI value | URL |
| special | Special handling | Near location |

## Status Codes

| Code | Display |
|------|---------|
| draft | Draft |
| active | Active |
| retired | Retired |
| unknown | Unknown |
