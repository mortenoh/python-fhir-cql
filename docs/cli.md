# CLI Reference

## FHIRPath CLI

### eval

Evaluate a FHIRPath expression against a FHIR resource.

```bash
fhirpath eval <expression> -r <resource.json>
fhirpath eval <expression> --json '<inline-json>'
```

**Options:**

| Option | Description |
|--------|-------------|
| `-r, --resource` | Path to FHIR JSON resource file |
| `--json` | Inline JSON resource |
| `--json-output` | Output result as JSON |

**Examples:**

```bash
# Basic navigation
fhirpath eval "Patient.name.family" -r patient.json

# Filtering
fhirpath eval "Patient.name.where(use = 'official').given" -r patient.json

# Boolean expression
fhirpath eval "Patient.gender = 'male'" -r patient.json

# JSON output
fhirpath eval "Patient.name.given" -r patient.json --json-output
```

### eval-file

Evaluate multiple expressions from a file.

```bash
fhirpath eval-file <expressions.fhirpath> -r <resource.json>
```

### parse

Validate FHIRPath syntax.

```bash
fhirpath parse <expression>
fhirpath parse <expression> -q  # quiet mode
```

### ast

Display the Abstract Syntax Tree.

```bash
fhirpath ast <expression>
fhirpath ast <expression> --depth 5  # limit depth
```

### tokens

Show the token stream.

```bash
fhirpath tokens <expression>
fhirpath tokens <expression> --limit 20
```

### parse-file

Parse multiple expressions from a file.

```bash
fhirpath parse-file <file.fhirpath>
```

### repl

Start interactive REPL.

```bash
fhirpath repl
fhirpath repl -r patient.json  # with resource loaded
```

**REPL Commands:**

- Type expression to evaluate
- `ast <expr>` - show AST
- `tokens <expr>` - show tokens
- `quit` or `exit` - exit REPL

### show

Display a file with syntax highlighting.

```bash
fhirpath show <file.fhirpath>
```

---

## CQL CLI

### eval

Evaluate a CQL expression directly.

```bash
cql eval <expression>
cql eval <expression> --library <file.cql>
cql eval <expression> --data <resource.json>
```

**Options:**

| Option | Description |
|--------|-------------|
| `-l, --library` | CQL library file for context (definitions, functions) |
| `-d, --data` | JSON data file for context (patient, resources) |

**Examples:**

```bash
# Simple arithmetic
cql eval "1 + 2 * 3"
# Output: 7

# String operations
cql eval "Upper('hello')"
# Output: 'HELLO'

cql eval "Combine({'a', 'b', 'c'}, ', ')"
# Output: 'a, b, c'

# Date operations
cql eval "Today()"
cql eval "Today() + 30 days"
cql eval "years between @1990-01-01 and Today()"

# List operations
cql eval "Sum({1, 2, 3, 4, 5})"
cql eval "Avg({10, 20, 30})"
cql eval "First({1, 2, 3})"

# Math functions
cql eval "Round(3.14159, 2)"
cql eval "Sqrt(16)"
cql eval "Power(2, 10)"

# Evaluate definition from library
cql eval "Sum" --library examples/cql/01_hello_world.cql

# With patient data
cql eval "Patient.birthDate" --data patient.json
```

### run

Run a CQL library and evaluate definitions.

```bash
cql run <file.cql>
cql run <file.cql> --definition <name>
cql run <file.cql> --data <resource.json>
cql run <file.cql> --output <results.json>
```

**Options:**

| Option | Description |
|--------|-------------|
| `-e, --definition` | Specific definition to evaluate |
| `-d, --data` | JSON data file for context |
| `-o, --output` | Output file for results (JSON format) |

**Examples:**

```bash
# Run all definitions in library
cql run examples/cql/01_hello_world.cql

# Evaluate specific definition
cql run examples/cql/01_hello_world.cql --definition Sum

# Run with patient data
cql run library.cql --data patient.json

# Run with patient bundle
cql run library.cql --data examples/fhir/bundle_patient_diabetic.json

# Save results to JSON file
cql run library.cql --output results.json
```

**Output Format:**

The `run` command displays a table with all definition results:

```
Library: HelloWorld v1.0.0

┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Definition       ┃ Value                   ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ HelloMessage     │ 'Hello, World!'         │
│ Sum              │ 6                       │
│ IsTrue           │ true                    │
└──────────────────┴─────────────────────────┘
```

### parse

Parse a CQL file and report syntax errors.

```bash
cql parse <file.cql>
cql parse <file.cql> -q  # quiet mode
```

### ast

Display the Abstract Syntax Tree.

```bash
cql ast <file.cql>
cql ast <file.cql> --depth 5
```

### tokens

Show the token stream.

```bash
cql tokens <file.cql>
cql tokens <file.cql> --limit 50
```

### validate

Validate multiple CQL files.

```bash
cql validate file1.cql file2.cql
cql validate examples/cql/*.cql
```

**Output:**

```
[ OK ] 01_hello_world.cql
[ OK ] 02_patient_queries.cql
[ OK ] 03_observations.cql
...

Results: 17/17 passed, 0/17 failed
```

### definitions

List library definitions.

```bash
cql definitions <file.cql>
```

**Output includes:**

- Library name and version
- Using declarations (FHIR version)
- Parameters
- Value sets and code systems
- Codes and concepts
- Named expressions
- Functions

### show

Display a file with syntax highlighting.

```bash
cql show <file.cql>
```

---

## Quick Reference

### FHIRPath Commands

| Command | Description |
|---------|-------------|
| `fhirpath eval` | Evaluate expression against resource |
| `fhirpath eval-file` | Evaluate expressions from file |
| `fhirpath parse` | Validate syntax |
| `fhirpath ast` | Show Abstract Syntax Tree |
| `fhirpath tokens` | Show token stream |
| `fhirpath parse-file` | Parse expressions from file |
| `fhirpath repl` | Interactive REPL mode |
| `fhirpath show` | Display file with highlighting |

### CQL Commands

| Command | Description |
|---------|-------------|
| `cql eval` | Evaluate expression |
| `cql run` | Run library and evaluate definitions |
| `cql parse` | Parse and validate file |
| `cql ast` | Show Abstract Syntax Tree |
| `cql tokens` | Show token stream |
| `cql validate` | Validate multiple files |
| `cql definitions` | List library definitions |
| `cql show` | Display file with highlighting |

---

## Common Patterns

### Evaluate arithmetic

```bash
cql eval "1 + 2 * 3"           # 7
cql eval "10 / 3"              # 3.333...
cql eval "10 div 3"            # 3 (integer division)
cql eval "10 mod 3"            # 1 (modulo)
```

### Work with strings

```bash
cql eval "'Hello' + ' ' + 'World'"
cql eval "Upper('hello')"
cql eval "Substring('Hello World', 0, 5)"
cql eval "Split('a,b,c', ',')"
```

### Work with dates

```bash
cql eval "Today()"
cql eval "Now()"
cql eval "@2024-06-15 + 30 days"
cql eval "years between @1990-01-01 and Today()"
```

### Work with lists

```bash
cql eval "{1, 2, 3, 4, 5}"
cql eval "Sum({1, 2, 3})"
cql eval "First({1, 2, 3})"
cql eval "from n in {1,2,3,4,5} where n > 2 return n * 2"
```

### Work with intervals

```bash
cql eval "Interval[1, 10] contains 5"
cql eval "5 in Interval[1, 10]"
cql eval "Interval[1, 5] overlaps Interval[3, 8]"
```

### Run example libraries

```bash
# Hello World basics
cql run examples/cql/01_hello_world.cql

# String functions
cql run examples/cql/09_string_functions.cql

# Math functions
cql run examples/cql/10_math_functions.cql

# Date/time operations
cql run examples/cql/12_date_time_operations.cql

# Clinical calculations
cql run examples/cql/16_clinical_calculations.cql
```
