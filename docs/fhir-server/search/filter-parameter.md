# _filter Parameter

## Overview

The `_filter` parameter enables advanced filter expressions beyond simple search parameters. It supports complex boolean logic, comparison operators, and parentheses for grouping.

## FHIR Specification

- [Search Filter](https://hl7.org/fhir/search_filter.html) - FHIR Search Filter Parameter

## Syntax

```
_filter=<path> <operator> <value> [<logical> <path> <operator> <value>]...
```

### Comparison Operators

| Operator | Name | Description | Example |
|----------|------|-------------|---------|
| `eq` | Equals | Exact match | `gender eq male` |
| `ne` | Not equals | Does not match | `status ne active` |
| `gt` | Greater than | Value is greater | `birthDate gt 1990-01-01` |
| `lt` | Less than | Value is less | `age lt 65` |
| `ge` | Greater or equal | Value is >= | `birthDate ge 1990-01-01` |
| `le` | Less or equal | Value is <= | `birthDate le 2000-01-01` |
| `co` | Contains | String contains | `name co smith` |
| `sw` | Starts with | String starts with | `family sw Sm` |
| `ew` | Ends with | String ends with | `family ew son` |
| `sa` | Starts after | Period starts after | `date sa 2024-01-01` |
| `eb` | Ends before | Period ends before | `date eb 2024-12-31` |
| `ap` | Approximately | Approximately equal (within 10%) | `value ap 100` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Both conditions must match | `gender eq male and active eq true` |
| `or` | Either condition matches | `gender eq male or gender eq female` |
| `not` | Negates the condition | `not active eq false` |

### Grouping

Use parentheses to group expressions:

```
(gender eq male or gender eq female) and birthDate ge 1990-01-01
```

## Examples

### Basic Filtering

```bash
# Find male patients
curl "http://localhost:8080/baseR4/Patient?_filter=gender%20eq%20male"

# Find patients not named Smith
curl "http://localhost:8080/baseR4/Patient?_filter=family%20ne%20Smith"

# Find patients born after 1990
curl "http://localhost:8080/baseR4/Patient?_filter=birthDate%20ge%201990-01-01"
```

### String Matching

```bash
# Find patients with family name containing "son"
curl "http://localhost:8080/baseR4/Patient?_filter=family%20co%20son"

# Find patients with family name starting with "Sm"
curl "http://localhost:8080/baseR4/Patient?_filter=family%20sw%20Sm"

# Find patients with family name ending with "th"
curl "http://localhost:8080/baseR4/Patient?_filter=family%20ew%20th"
```

### Logical Combinations

```bash
# Find active male patients
curl "http://localhost:8080/baseR4/Patient?_filter=gender%20eq%20male%20and%20active%20eq%20true"

# Find male or female patients
curl "http://localhost:8080/baseR4/Patient?_filter=gender%20eq%20male%20or%20gender%20eq%20female"

# Find patients who are NOT inactive
curl "http://localhost:8080/baseR4/Patient?_filter=not%20active%20eq%20false"
```

### Complex Expressions

```bash
# Find active patients (male or female) born after 1980
curl "http://localhost:8080/baseR4/Patient?_filter=(gender%20eq%20male%20or%20gender%20eq%20female)%20and%20birthDate%20ge%201980-01-01%20and%20active%20eq%20true"
```

### Combined with Regular Search

```bash
# Use _filter with standard search parameters
curl "http://localhost:8080/baseR4/Patient?gender=male&_filter=active%20eq%20true"
```

## Supported Paths

The `_filter` parameter supports:

1. **Direct element paths**: `gender`, `birthDate`, `active`
2. **Nested paths**: `name.family`, `address.city`
3. **Search parameter names**: Use any defined search parameter

### Patient Paths

| Path | Description |
|------|-------------|
| `gender` | Patient gender |
| `birthDate` | Birth date |
| `active` | Active status |
| `family` / `name.family` | Family name |
| `given` / `name.given` | Given name |

### Observation Paths

| Path | Description |
|------|-------------|
| `status` | Observation status |
| `code` | Observation code |
| `valueQuantity.value` | Numeric value |

### Condition Paths

| Path | Description |
|------|-------------|
| `clinicalStatus` | Clinical status code |
| `verificationStatus` | Verification status |
| `code` | Condition code |

## Value Formats

### Strings

Strings can be quoted or unquoted:

```
gender eq "male"
gender eq male
```

Both are equivalent. Use quotes if the value contains spaces:

```
name eq "John Smith"
```

### Dates

Use ISO 8601 format:

```
birthDate ge 1990-01-01
birthDate le 2024-12-31T23:59:59
```

### Booleans

```
active eq true
active eq false
```

### Numbers

```
valueInteger gt 100
valueDecimal le 37.5
```

### Codes (CodeableConcept)

The filter automatically extracts code values:

```
code eq 8480-6
clinicalStatus eq active
```

## Error Handling

Invalid filter expressions return an OperationOutcome:

```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "invalid",
    "diagnostics": "Invalid _filter expression: Expected comparison operator, got: invalid"
  }]
}
```

## Comparison with Standard Search

| Feature | Standard Search | _filter |
|---------|-----------------|---------|
| Simple equality | `?gender=male` | `?_filter=gender eq male` |
| Multiple values | `?gender=male,female` | `?_filter=gender eq male or gender eq female` |
| Boolean logic | Limited (implicit AND) | Full (and, or, not) |
| Date comparisons | Prefix (`ge`, `le`) | Operators (ge, le, gt, lt) |
| String matching | Limited | Contains, starts with, ends with |
| Grouping | Not supported | Parentheses |

## Best Practices

1. **URL encode the filter**: Always URL-encode spaces and special characters
2. **Use standard search first**: For simple queries, standard parameters are more efficient
3. **Test expressions**: Use simpler expressions to verify behavior before building complex ones
4. **Combine wisely**: Use `_filter` with standard search parameters for efficient filtering

## Limitations

- Filter is applied after initial search results
- Large result sets may impact performance
- Some complex FHIRPath expressions are not supported
