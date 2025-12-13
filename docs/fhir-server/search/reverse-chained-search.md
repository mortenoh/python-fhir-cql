# Reverse Chained Search (_has)

## Overview

Reverse chained search (using `_has`) allows you to find resources based on other resources that reference them. This is the opposite of regular chained search - instead of "find A where A references B matching criteria", it's "find A where B references A and B matches criteria".

## Syntax

```
{ResourceType}?_has:{ReferencingType}:{referenceParam}:{searchParam}={value}
```

Components:
- `{ResourceType}` - The resource type to return (e.g., Patient)
- `{ReferencingType}` - The type that references the target (e.g., Condition)
- `{referenceParam}` - The reference parameter in ReferencingType (e.g., patient)
- `{searchParam}` - Search parameter on ReferencingType (e.g., code)
- `{value}` - The value to match

## How It Works

1. The server parses the `_has` parameter format
2. Searches for all `{ReferencingType}` resources matching `{searchParam}={value}`
3. Extracts the references from `{referenceParam}` field
4. Returns only `{ResourceType}` resources that are referenced

## Examples

### Find Patients with Diabetes Diagnosis

```bash
curl "http://localhost:8000/Patient?_has:Condition:patient:code=diabetes"
```

Returns Patients who have a Condition with code containing "diabetes".

### Find Patients with Recent Observations

```bash
curl "http://localhost:8000/Patient?_has:Observation:subject:code=8480-6"
```

Returns Patients who have an Observation with LOINC code 8480-6 (Systolic BP).

### Find Practitioners with Active MedicationRequests

```bash
curl "http://localhost:8000/Practitioner?_has:MedicationRequest:requester:status=active"
```

Returns Practitioners who have written active medication prescriptions.

### Find Organizations with Encounters

```bash
curl "http://localhost:8000/Organization?_has:Encounter:serviceProvider:status=finished"
```

Returns Organizations that have finished Encounters.

### Find Patients with Specific Allergies

```bash
curl "http://localhost:8000/Patient?_has:AllergyIntolerance:patient:code=penicillin"
```

Returns Patients with penicillin allergies.

## Supported Patterns

| Target Type | Referencing Type | Reference Param | Common Search Params |
|-------------|------------------|-----------------|---------------------|
| Patient | Condition | patient, subject | code, clinical-status |
| Patient | Observation | subject | code, status |
| Patient | MedicationRequest | subject | status, medication |
| Patient | Procedure | subject | code, status |
| Patient | Encounter | subject | status, class |
| Patient | DiagnosticReport | subject | code, status |
| Patient | AllergyIntolerance | patient | code, clinical-status |
| Patient | Immunization | patient | vaccine-code, status |
| Patient | CarePlan | subject | status, category |
| Patient | Goal | subject | lifecycle-status |
| Patient | ServiceRequest | subject | status, code |
| Patient | DocumentReference | subject | type, status |
| Patient | MeasureReport | subject | status, measure |
| Practitioner | MedicationRequest | requester | status |
| Practitioner | Encounter | participant | status |
| Practitioner | Procedure | performer | status |
| Organization | Encounter | serviceProvider | status |

## Combining with Other Parameters

Reverse chained parameters can be combined with regular search and chained parameters:

```bash
# Find active Patients with diabetes
curl "http://localhost:8000/Patient?_has:Condition:patient:code=diabetes&active=true"

# Find Patients with diabetes AND hypertension
curl "http://localhost:8000/Patient?_has:Condition:patient:code=diabetes&_has:Condition:patient:code=hypertension"

# With pagination
curl "http://localhost:8000/Patient?_has:Condition:patient:code=diabetes&_count=10"
```

## Use Cases

### Clinical Decision Support
Find patients who need follow-up based on existing conditions or observations:
```bash
# Patients with HbA1c > 7%
curl "http://localhost:8000/Patient?_has:Observation:subject:code=4548-4"
```

### Population Health
Identify patient cohorts for quality measures:
```bash
# Patients with diabetes for measure evaluation
curl "http://localhost:8000/Patient?_has:Condition:patient:code=44054006"
```

### Care Coordination
Find patients with specific care needs:
```bash
# Patients with active care plans
curl "http://localhost:8000/Patient?_has:CarePlan:subject:status=active"
```

## Performance Considerations

- `_has` searches require searching the referencing resource type first
- Multiple `_has` parameters multiply the search effort
- Consider caching strategies for frequently used queries
- For large datasets, direct searches may be more efficient

## Limitations

- Only single-level reverse chaining is supported
- The referencing resource type must be supported by the server
- Complex logical combinations (OR between `_has` clauses) are not supported
- Each `_has` parameter is evaluated independently (AND logic)

## Error Handling

Invalid `_has` parameters are gracefully ignored:
- Unknown resource types
- Unknown reference parameters
- Unknown search parameters

The server continues processing with valid parameters.

## FHIR Specification

For more details on reverse chained parameters, see:
- [FHIR R4 Search - Reverse Chaining](https://hl7.org/fhir/R4/search.html#has)
