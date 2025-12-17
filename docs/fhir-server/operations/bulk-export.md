# Bulk Data Export ($export)

## Overview

The FHIR server implements the [FHIR Bulk Data Access IG](http://hl7.org/fhir/uv/bulkdata/) for asynchronous export of large datasets in NDJSON format.

## FHIR Specification

- [Bulk Data Access IG](http://hl7.org/fhir/uv/bulkdata/)
- [System Export](http://hl7.org/fhir/uv/bulkdata/OperationDefinition-export.html)
- [Patient Export](http://hl7.org/fhir/uv/bulkdata/OperationDefinition-patient-export.html)
- [Group Export](http://hl7.org/fhir/uv/bulkdata/OperationDefinition-group-export.html)

## Export Types

### System Export

Export all resources from the server.

```http
GET /$export
Accept: application/fhir+ndjson
Prefer: respond-async
```

### Patient Export

Export Patient resources and all related clinical data.

```http
GET /Patient/$export
Accept: application/fhir+ndjson
Prefer: respond-async
```

### Group Export

Export data for all patients in a specified Group.

```http
GET /Group/{id}/$export
Accept: application/fhir+ndjson
Prefer: respond-async
```

## Required Headers

| Header | Value | Description |
|--------|-------|-------------|
| `Accept` | `application/fhir+ndjson` | Request NDJSON format |
| `Prefer` | `respond-async` | Required for async processing |

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `_type` | string | Comma-separated list of resource types to export |
| `_since` | instant | Only export resources updated after this datetime |

## Workflow

### 1. Initiate Export

```bash
curl -X GET "http://localhost:8080/baseR4/\$export" \
  -H "Accept: application/fhir+ndjson" \
  -H "Prefer: respond-async"
```

Response (202 Accepted):
```
Content-Location: http://localhost:8080/baseR4/bulk-status/abc123-uuid
```

### 2. Poll for Status

```bash
curl http://localhost:8080/baseR4/bulk-status/abc123-uuid
```

**In Progress** (202 Accepted):
```
X-Progress: 50%
Retry-After: 1
```

**Complete** (200 OK):
```json
{
  "transactionTime": "2024-12-17T10:00:00Z",
  "request": "http://localhost:8080/baseR4/$export",
  "requiresAccessToken": false,
  "output": [
    {
      "type": "Patient",
      "url": "http://localhost:8080/baseR4/bulk-output/abc123-uuid/Patient.ndjson",
      "count": 100
    },
    {
      "type": "Observation",
      "url": "http://localhost:8080/baseR4/bulk-output/abc123-uuid/Observation.ndjson",
      "count": 500
    }
  ],
  "error": []
}
```

### 3. Download Output Files

```bash
curl http://localhost:8080/baseR4/bulk-output/abc123-uuid/Patient.ndjson \
  -o patients.ndjson
```

Returns NDJSON (one JSON object per line):
```
{"resourceType":"Patient","id":"p1","name":[{"family":"Smith"}]}
{"resourceType":"Patient","id":"p2","name":[{"family":"Doe"}]}
{"resourceType":"Patient","id":"p3","name":[{"family":"Johnson"}]}
```

### 4. Delete Job (Optional)

```bash
curl -X DELETE http://localhost:8080/baseR4/bulk-status/abc123-uuid
```

Returns 204 No Content on success.

## Examples

### Export All Patients

```bash
curl -X GET "http://localhost:8080/baseR4/Patient/\$export" \
  -H "Prefer: respond-async"
```

### Export Specific Resource Types

```bash
curl -X GET "http://localhost:8080/baseR4/\$export?_type=Patient,Condition,Observation" \
  -H "Prefer: respond-async"
```

### Export Resources Updated Since Date

```bash
curl -X GET "http://localhost:8080/baseR4/\$export?_since=2024-12-01T00:00:00Z" \
  -H "Prefer: respond-async"
```

### Export Group Members

```bash
curl -X GET "http://localhost:8080/baseR4/Group/diabetes-cohort/\$export" \
  -H "Prefer: respond-async"
```

### Full Export Workflow Script

```bash
#!/bin/bash
BASE_URL="http://localhost:8080/baseR4"

# Start export
RESPONSE=$(curl -sI -X GET "$BASE_URL/\$export?_type=Patient,Observation" \
  -H "Prefer: respond-async")

# Extract job URL
STATUS_URL=$(echo "$RESPONSE" | grep -i "Content-Location" | cut -d' ' -f2 | tr -d '\r')
echo "Job started: $STATUS_URL"

# Poll until complete
while true; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$STATUS_URL")
  if [ "$STATUS" = "200" ]; then
    echo "Export complete!"
    break
  elif [ "$STATUS" = "202" ]; then
    echo "In progress..."
    sleep 1
  else
    echo "Error: HTTP $STATUS"
    exit 1
  fi
done

# Get manifest and download files
MANIFEST=$(curl -s "$STATUS_URL")
echo "$MANIFEST" | jq -r '.output[].url' | while read URL; do
  FILENAME=$(basename "$URL")
  echo "Downloading $FILENAME..."
  curl -s "$URL" -o "$FILENAME"
done
```

## Default Resource Types

### Patient Export Types

| Resource Type |
|---------------|
| Patient |
| Observation |
| Condition |
| Encounter |
| MedicationRequest |
| Procedure |
| DiagnosticReport |
| AllergyIntolerance |
| Immunization |
| CarePlan |
| Goal |
| ServiceRequest |
| DocumentReference |

### System Export Types

Includes all patient export types plus:

| Resource Type |
|---------------|
| Practitioner |
| Organization |
| Medication |
| Measure |
| MeasureReport |
| Group |

## Response Status Codes

| Status | Endpoint | Meaning |
|--------|----------|---------|
| 202 | `$export` | Export job started |
| 202 | `bulk-status` | Job in progress |
| 200 | `bulk-status` | Job complete (returns manifest) |
| 200 | `bulk-output` | File download |
| 400 | `$export` | Missing Prefer header or invalid parameters |
| 404 | `bulk-status` | Job not found |
| 404 | `bulk-output` | Job or file not found |
| 422 | `Group/$export` | Group has no patient members |
| 500 | `bulk-status` | Job failed |

## NDJSON Format

NDJSON (Newline Delimited JSON) contains one JSON object per line:

```
{"resourceType":"Patient","id":"1","name":[{"family":"Smith"}]}
{"resourceType":"Patient","id":"2","name":[{"family":"Doe"}]}
```

Benefits:
- Streamable - process line by line without loading entire file
- Memory efficient for large datasets
- Standard format for bulk data interchange

## Group Export Filtering

When exporting via Group, only resources related to the patients in the group are included:

1. Patient resources matching group member IDs
2. Resources with `subject` or `patient` references to those patients

```json
{
  "resourceType": "Group",
  "type": "person",
  "actual": true,
  "member": [
    {"entity": {"reference": "Patient/p1"}},
    {"entity": {"reference": "Patient/p2"}}
  ]
}
```

## Error Handling

### Missing Prefer Header

```bash
curl http://localhost:8080/baseR4/\$export
```

Response (400):
```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "required",
    "diagnostics": "Bulk export requires 'Prefer: respond-async' header"
  }]
}
```

### Invalid _since Format

```bash
curl "http://localhost:8080/baseR4/\$export?_since=invalid" \
  -H "Prefer: respond-async"
```

Response (400):
```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "invalid",
    "diagnostics": "Invalid _since datetime: invalid"
  }]
}
```

### Job Failed

```bash
curl http://localhost:8080/baseR4/bulk-status/failed-job-id
```

Response (500):
```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "exception",
    "diagnostics": "Export job failed: [error details]"
  }]
}
```

## Python API

```python
from fhirkit.server.api.bulk import (
    create_export_job,
    run_export,
    get_export_job,
    delete_export_job,
    resources_to_ndjson,
    PATIENT_EXPORT_TYPES,
    ALL_EXPORT_TYPES,
)

# Create and run export
job = create_export_job(
    resource_types=["Patient", "Observation"],
    patient_ids=["p1", "p2"],  # Optional filter
    since=datetime(2024, 1, 1),  # Optional since filter
)

await run_export(job, store)

# Check status
job = get_export_job(job.id)
if job.status == "complete":
    for resource_type, resources in job.output_files.items():
        ndjson = resources_to_ndjson(resources)
        print(f"{resource_type}: {len(resources)} resources")

# Cleanup
delete_export_job(job.id)
```

## Notes

- Export jobs are stored in memory and cleared on server restart
- The server processes exports synchronously (fast for in-memory store)
- For large exports, consider using pagination with `_since` to export incrementally
- Binary resources are included as base64-encoded NDJSON entries
