# GraphQL API

## Overview

The FHIR server provides a GraphQL endpoint following the [FHIR GraphQL specification](https://hl7.org/fhir/graphql.html). This provides an alternative to the REST API with benefits like:

- Request only the fields you need
- Fetch related resources in a single request
- Strongly typed queries with introspection
- Interactive GraphiQL playground

## Endpoint

The GraphQL endpoint is available at:

```
POST /baseR4/$graphql
GET  /baseR4/$graphql  (GraphiQL playground)
```

## FHIR Specification

- [FHIR GraphQL](https://hl7.org/fhir/graphql.html) - Official FHIR GraphQL specification

## Query Patterns

### Single Resource Query

Fetch a single resource by ID using the resource type name with `_id` parameter:

```graphql
{
  Patient(_id: "patient-123") {
    id
    resourceType
    data
  }
}
```

Response:
```json
{
  "data": {
    "Patient": {
      "id": "patient-123",
      "resourceType": "Patient",
      "data": {
        "resourceType": "Patient",
        "id": "patient-123",
        "name": [{"family": "Smith", "given": ["John"]}],
        "gender": "male"
      }
    }
  }
}
```

### Generic Resource Query

Query any resource type dynamically:

```graphql
{
  resource(resourceType: "Observation", _id: "obs-123") {
    id
    resourceType
    data
  }
}
```

### List Queries

Search for resources with FHIR search parameters and offset pagination:

```graphql
{
  PatientList(
    gender: "male"
    name: "Smith"
    _count: 10
    _offset: 0
    _sort: "family"
  ) {
    id
    resourceType
    data
  }
}
```

Available parameters:
- `_count`: Maximum number of results (default: 100)
- `_offset`: Skip this many results (for pagination)
- `_sort`: Sort by field (prefix with `-` for descending)
- Resource-specific search parameters (e.g., `gender`, `name`, `birthdate`)

### Connection Queries (Cursor Pagination)

For cursor-based pagination following the GraphQL Connections spec:

```graphql
{
  PatientConnection(first: 10, after: "cursor-string") {
    edges {
      cursor
      node {
        id
        resourceType
        data
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
    total
  }
}
```

Parameters:
- `first`: Number of items to fetch
- `after`: Cursor from previous page's `endCursor`

### Reference Resolution

The `data` field returns the full FHIR resource as JSON, which you can use to access any field:

```graphql
{
  Observation(_id: "obs-123") {
    id
    data
  }
}
```

To navigate references between resources, you can use multiple queries or fetch related data in the `data` field.

## Mutations

### Create Resource

```graphql
mutation CreatePatient($data: JSON!) {
  PatientCreate(data: $data) {
    id
    resourceType
    data
  }
}
```

Variables:
```json
{
  "data": {
    "resourceType": "Patient",
    "name": [{"family": "Smith", "given": ["John"]}],
    "gender": "male"
  }
}
```

### Update Resource

```graphql
mutation UpdatePatient($id: String!, $data: JSON!) {
  PatientUpdate(_id: $id, data: $data) {
    id
    data
  }
}
```

Variables:
```json
{
  "id": "patient-123",
  "data": {
    "resourceType": "Patient",
    "id": "patient-123",
    "name": [{"family": "Updated"}],
    "gender": "male"
  }
}
```

### Delete Resource

```graphql
mutation {
  PatientDelete(_id: "patient-123") {
    id
    data
  }
}
```

### Generic Mutations

Create or update any resource type:

```graphql
mutation CreateResource($resourceType: String!, $data: JSON!) {
  resourceCreate(resourceType: $resourceType, data: $data) {
    id
    resourceType
    data
  }
}

mutation UpdateResource($resourceType: String!, $id: String!, $data: JSON!) {
  resourceUpdate(resourceType: $resourceType, _id: $id, data: $data) {
    id
    data
  }
}

mutation DeleteResource($resourceType: String!, $id: String!) {
  resourceDelete(resourceType: $resourceType, _id: $id) {
    id
  }
}
```

## Supported Resource Types

All resource types from the REST API are available in GraphQL. Each type has:

- `{Type}(_id: String!)` - Fetch single resource
- `{TypeList}(...)` - Search with offset pagination
- `{Type}Connection(...)` - Search with cursor pagination
- `{Type}Create(data: JSON!)` - Create resource
- `{Type}Update(_id: String!, data: JSON!)` - Update resource
- `{Type}Delete(_id: String!)` - Delete resource

Resource types include: Patient, Observation, Condition, Encounter, Medication, MedicationRequest, Procedure, DiagnosticReport, Immunization, AllergyIntolerance, CarePlan, CareTeam, Goal, Practitioner, PractitionerRole, Organization, Location, Device, and many more.

## Examples

### Fetch Patient with Observations

```graphql
query PatientWithData($patientId: String!) {
  patient: Patient(_id: $patientId) {
    id
    data
  }
  observations: ObservationList(patient: $patientId, _count: 10) {
    id
    data
  }
  conditions: ConditionList(patient: $patientId) {
    id
    data
  }
}
```

### Paginated Patient List

```graphql
{
  PatientConnection(first: 5) {
    edges {
      cursor
      node {
        id
        data
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    total
  }
}
```

Then fetch next page:

```graphql
{
  PatientConnection(first: 5, after: "b2Zmc2V0OjU=") {
    edges {
      cursor
      node {
        id
        data
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Create and Query

```graphql
mutation {
  PatientCreate(data: {
    resourceType: "Patient"
    name: [{family: "Test", given: ["New"]}]
    birthDate: "1990-01-15"
  }) {
    id
    resourceType
  }
}
```

## GraphiQL Playground

Access the interactive GraphiQL IDE by opening the GraphQL endpoint in a browser:

```
http://localhost:8080/baseR4/$graphql
```

Features:
- Syntax highlighting
- Auto-completion
- Query history
- Documentation explorer
- Variable editor

## cURL Examples

### Query

```bash
curl -X POST http://localhost:8080/baseR4/\$graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ PatientList(_count: 5) { id data } }"
  }'
```

### Mutation with Variables

```bash
curl -X POST http://localhost:8080/baseR4/\$graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreatePatient($data: JSON!) { PatientCreate(data: $data) { id } }",
    "variables": {
      "data": {
        "resourceType": "Patient",
        "name": [{"family": "Smith"}]
      }
    }
  }'
```

## Python Client Example

```python
import requests

GRAPHQL_URL = "http://localhost:8080/baseR4/$graphql"

# Query
response = requests.post(GRAPHQL_URL, json={
    "query": """
    {
        PatientList(_count: 10) {
            id
            data
        }
    }
    """
})
patients = response.json()["data"]["PatientList"]

# Mutation
response = requests.post(GRAPHQL_URL, json={
    "query": """
    mutation CreatePatient($data: JSON!) {
        PatientCreate(data: $data) {
            id
            resourceType
        }
    }
    """,
    "variables": {
        "data": {
            "resourceType": "Patient",
            "name": [{"family": "New", "given": ["Patient"]}]
        }
    }
})
created = response.json()["data"]["PatientCreate"]
```

## Error Handling

GraphQL errors are returned in the `errors` field:

```json
{
  "data": null,
  "errors": [
    {
      "message": "Resource not found",
      "locations": [{"line": 2, "column": 3}],
      "path": ["Patient"]
    }
  ]
}
```

Common errors:
- Unknown argument or field names
- Invalid resource type
- Missing required arguments
- Resource not found (for mutations)

## Comparison: REST vs GraphQL

| Feature | REST | GraphQL |
|---------|------|---------|
| Fetch single resource | `GET /Patient/123` | `Patient(_id: "123")` |
| Search resources | `GET /Patient?name=Smith` | `PatientList(name: "Smith")` |
| Create resource | `POST /Patient` | `PatientCreate(data: {...})` |
| Update resource | `PUT /Patient/123` | `PatientUpdate(_id: "123", data: {...})` |
| Delete resource | `DELETE /Patient/123` | `PatientDelete(_id: "123")` |
| Field selection | `_elements=id,name` | Request specific fields in query |
| Multiple resources | Multiple requests | Single query with multiple fields |
