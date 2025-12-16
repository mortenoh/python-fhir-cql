# _total Search Parameter

## Overview

The `_total` parameter controls whether and how the server calculates and returns the total count of matching resources in search results.

## FHIR Specification

- [_total](https://hl7.org/fhir/R4/search.html#total) - Control total count behavior

## Values

| Value | Description |
|-------|-------------|
| `accurate` | Return an accurate total count (default behavior) |
| `estimate` | Return an estimated count (currently returns accurate count) |
| `none` | Do not return a total count |

## Usage

```bash
# Default behavior - returns accurate total
GET /Patient

# Explicitly request accurate total
GET /Patient?_total=accurate

# Skip total calculation (useful for performance on large datasets)
GET /Patient?_total=none

# Request estimated total (currently same as accurate)
GET /Patient?_total=estimate
```

## Response Examples

### With total (default or `_total=accurate`)

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 42,
  "entry": [...]
}
```

### Without total (`_total=none`)

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "entry": [...]
}
```

## Performance Considerations

- **`accurate`**: Server counts all matching resources. For small datasets, this has minimal impact.
- **`estimate`**: Currently returns the same as accurate. Future optimization may use sampling for large datasets.
- **`none`**: Skips including the total in the response. The server still performs the search but doesn't report the count.

## Combining with Other Parameters

The `_total` parameter can be combined with:

- **Pagination**: `?_total=none&_count=10&_offset=20`
- **Sorting**: `?_total=accurate&_sort=-birthDate`
- **_elements/_summary**: `?_total=none&_elements=name,birthDate`
- **_include/_revinclude**: `?_total=none&_include=Condition:subject`

## Use Cases

### Performance optimization

When you only need results and don't care about the total count:

```bash
curl "http://localhost:8000/Observation?_total=none&_count=50"
```

### Pagination with known total

When you need accurate pagination information:

```bash
curl "http://localhost:8000/Patient?_total=accurate&_count=20&_offset=40"
```

### Quick data retrieval

Fetch first page quickly without counting all matches:

```bash
curl "http://localhost:8000/Condition?patient=Patient/123&_total=none&_count=10"
```

## Notes

- When `_total` is not specified, the default behavior is `accurate`
- The `_summary=count` parameter takes precedence and always returns a count-only bundle
- Pagination links are still included regardless of `_total` setting
