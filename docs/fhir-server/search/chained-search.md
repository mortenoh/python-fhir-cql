# Chained Search Parameters

## Overview

Chained search parameters allow you to search for resources based on properties of referenced resources. This enables complex queries across resource relationships without multiple API calls.

## Syntax

```
{ResourceType}?{referenceParam}:{TargetType}.{targetParam}={value}
```

Components:
- `{ResourceType}` - The resource type to search (e.g., Condition)
- `{referenceParam}` - The reference parameter name (e.g., subject)
- `{TargetType}` - The type of referenced resource (e.g., Patient)
- `{targetParam}` - Search parameter on the target resource (e.g., name)
- `{value}` - The value to match

## How It Works

1. The server parses the chained parameter format
2. Finds all resources of `{TargetType}` matching `{targetParam}={value}`
3. Collects their resource IDs
4. Returns only resources where `{referenceParam}` points to one of those IDs

## Examples

### Find Conditions for Patients Named "Smith"

```bash
curl "http://localhost:8000/Condition?subject:Patient.name=Smith"
```

Returns all Conditions where the referenced Patient has "Smith" in their name.

### Find Observations for Patients with Specific Identifier

```bash
curl "http://localhost:8000/Observation?subject:Patient.identifier=12345"
```

Returns all Observations for Patients with identifier containing "12345".

### Find MedicationRequests by Practitioner Name

```bash
curl "http://localhost:8000/MedicationRequest?requester:Practitioner.name=Johnson"
```

Returns MedicationRequests where the requesting Practitioner has "Johnson" in their name.

### Find Encounters at Specific Organization

```bash
curl "http://localhost:8000/Encounter?serviceProvider:Organization.name=General%20Hospital"
```

Returns Encounters at organizations with "General Hospital" in the name.

## Supported Resources

| Source Resource | Reference Parameter | Target Types |
|-----------------|---------------------|--------------|
| Condition | subject | Patient |
| Condition | encounter | Encounter |
| Observation | subject | Patient |
| Observation | encounter | Encounter |
| Observation | performer | Practitioner |
| MedicationRequest | subject | Patient |
| MedicationRequest | requester | Practitioner |
| MedicationRequest | encounter | Encounter |
| Procedure | subject | Patient |
| Procedure | encounter | Encounter |
| Procedure | performer | Practitioner |
| Encounter | subject | Patient |
| Encounter | participant | Practitioner |
| DiagnosticReport | subject | Patient |
| DiagnosticReport | performer | Practitioner |
| AllergyIntolerance | patient | Patient |
| Immunization | patient | Patient |
| CarePlan | subject | Patient |
| Goal | subject | Patient |
| ServiceRequest | subject | Patient |
| DocumentReference | subject | Patient |
| MeasureReport | subject | Patient |

## Combining with Other Parameters

Chained parameters can be combined with regular search parameters:

```bash
# Find active Conditions for Patients named "Smith"
curl "http://localhost:8000/Condition?subject:Patient.name=Smith&clinical-status=active"

# With pagination
curl "http://localhost:8000/Condition?subject:Patient.name=Smith&_count=10&_offset=0"

# With sorting
curl "http://localhost:8000/Condition?subject:Patient.name=Smith&_sort=-recordedDate"
```

## Performance Considerations

- Chained searches require resolving referenced resources, which adds processing overhead
- For large datasets, consider using direct searches when possible
- The server caches resolved references within a single request

## Limitations

- Only single-level chaining is supported (not `A.B.C`)
- The target resource type must be explicitly specified
- Both the source and target resource types must be supported by the server
- Case-insensitive matching is used for string parameters

## Error Handling

Invalid chained parameters are gracefully ignored:
- Unknown resource types
- Unknown reference parameters
- Unknown target parameters

The server will return results based on valid parameters only.

## FHIR Specification

For more details on chained parameters, see:
- [FHIR R4 Search - Chained Parameters](https://hl7.org/fhir/R4/search.html#chaining)
