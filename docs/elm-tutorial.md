# ELM Tutorial

A step-by-step guide to working with ELM (Expression Logical Model).

## What You'll Learn

1. Loading ELM files
2. Evaluating definitions
3. Working with parameters
4. Using patient data
5. Converting CQL to ELM
6. Building an evaluation pipeline

---

## Part 1: Your First ELM File

### What is ELM?

ELM (Expression Logical Model) is the compiled representation of CQL. When CQL source code is compiled, it produces ELM JSON that can be:

- **Executed** by any ELM-compatible engine
- **Shared** between systems without recompilation
- **Stored** for efficient repeated execution

### Creating a Simple ELM File

Create a file called `hello.elm.json`:

```json
{
    "library": {
        "identifier": {
            "id": "HelloWorld",
            "version": "1.0"
        },
        "statements": {
            "def": [
                {
                    "name": "Greeting",
                    "expression": {
                        "type": "Literal",
                        "valueType": "{urn:hl7-org:elm-types:r1}String",
                        "value": "Hello, ELM!"
                    }
                },
                {
                    "name": "Answer",
                    "expression": {
                        "type": "Literal",
                        "valueType": "{urn:hl7-org:elm-types:r1}Integer",
                        "value": "42"
                    }
                }
            ]
        }
    }
}
```

### Loading and Evaluating

**Using the CLI:**

```bash
# Load and show info
fhir elm load hello.elm.json

# Evaluate a definition
fhir elm eval hello.elm.json Greeting
# Output: Hello, ELM!

fhir elm eval hello.elm.json Answer
# Output: 42

# Evaluate all definitions
fhir elm run hello.elm.json
```

**Using Python:**

```python
from fhirkit.engine.elm import ELMEvaluator

evaluator = ELMEvaluator()

# Load the ELM file
library = evaluator.load("hello.elm.json")

# Evaluate definitions
greeting = evaluator.evaluate_definition("Greeting")
print(greeting)  # Hello, ELM!

answer = evaluator.evaluate_definition("Answer")
print(answer)  # 42
```

---

## Part 2: Arithmetic Operations

### Adding Numbers

Create `math.elm.json`:

```json
{
    "library": {
        "identifier": {"id": "MathExamples", "version": "1.0"},
        "statements": {
            "def": [
                {
                    "name": "Sum",
                    "expression": {
                        "type": "Add",
                        "operand": [
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "10"},
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "20"}
                        ]
                    }
                },
                {
                    "name": "Product",
                    "expression": {
                        "type": "Multiply",
                        "operand": [
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "6"},
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "7"}
                        ]
                    }
                },
                {
                    "name": "Complex",
                    "expression": {
                        "type": "Add",
                        "operand": [
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "1"},
                            {
                                "type": "Multiply",
                                "operand": [
                                    {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "2"},
                                    {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "3"}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
}
```

**Try it:**

```python
evaluator = ELMEvaluator()
evaluator.load("math.elm.json")

print(evaluator.evaluate_definition("Sum"))      # 30
print(evaluator.evaluate_definition("Product"))  # 42
print(evaluator.evaluate_definition("Complex"))  # 7 (1 + 2*3)
```

### Exercise 1

Create an ELM file that calculates:
- `Difference`: 100 - 37
- `Quotient`: 144 / 12
- `Power`: 2^10

---

## Part 3: Working with Parameters

### Defining Parameters

Parameters allow runtime configuration. Create `params.elm.json`:

```json
{
    "library": {
        "identifier": {"id": "ParameterExample", "version": "1.0"},
        "parameters": [
            {
                "name": "Multiplier",
                "parameterType": "{urn:hl7-org:elm-types:r1}Integer",
                "default": {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "10"}
            },
            {
                "name": "BaseValue",
                "parameterType": "{urn:hl7-org:elm-types:r1}Integer"
            }
        ],
        "statements": {
            "def": [
                {
                    "name": "Result",
                    "expression": {
                        "type": "Multiply",
                        "operand": [
                            {"type": "ParameterRef", "name": "BaseValue"},
                            {"type": "ParameterRef", "name": "Multiplier"}
                        ]
                    }
                }
            ]
        }
    }
}
```

### Using Parameters

**CLI:**

```bash
fhir elm eval params.elm.json Result --param BaseValue=5
# Output: 50 (5 * 10, using default Multiplier)

fhir elm eval params.elm.json Result --param BaseValue=5 --param Multiplier=3
# Output: 15
```

**Python:**

```python
evaluator = ELMEvaluator()
evaluator.load("params.elm.json")

# Use default multiplier
result = evaluator.evaluate_definition("Result", parameters={"BaseValue": 5})
print(result)  # 50

# Override multiplier
result = evaluator.evaluate_definition("Result", parameters={
    "BaseValue": 5,
    "Multiplier": 3
})
print(result)  # 15
```

---

## Part 4: Referencing Definitions

Definitions can reference each other. Create `references.elm.json`:

```json
{
    "library": {
        "identifier": {"id": "ReferenceExample", "version": "1.0"},
        "statements": {
            "def": [
                {
                    "name": "A",
                    "expression": {
                        "type": "Literal",
                        "valueType": "{urn:hl7-org:elm-types:r1}Integer",
                        "value": "10"
                    }
                },
                {
                    "name": "B",
                    "expression": {
                        "type": "Literal",
                        "valueType": "{urn:hl7-org:elm-types:r1}Integer",
                        "value": "20"
                    }
                },
                {
                    "name": "Sum",
                    "expression": {
                        "type": "Add",
                        "operand": [
                            {"type": "ExpressionRef", "name": "A"},
                            {"type": "ExpressionRef", "name": "B"}
                        ]
                    }
                },
                {
                    "name": "Product",
                    "expression": {
                        "type": "Multiply",
                        "operand": [
                            {"type": "ExpressionRef", "name": "A"},
                            {"type": "ExpressionRef", "name": "B"}
                        ]
                    }
                },
                {
                    "name": "Average",
                    "expression": {
                        "type": "Divide",
                        "operand": [
                            {"type": "ExpressionRef", "name": "Sum"},
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Decimal", "value": "2.0"}
                        ]
                    }
                }
            ]
        }
    }
}
```

**Evaluate all:**

```python
evaluator = ELMEvaluator()
evaluator.load("references.elm.json")

results = evaluator.evaluate_all_definitions()
for name, value in results.items():
    print(f"{name}: {value}")

# Output:
# A: 10
# B: 20
# Sum: 30
# Product: 200
# Average: 15.0
```

---

## Part 5: Conditionals

### If-Then-Else

Create `conditionals.elm.json`:

```json
{
    "library": {
        "identifier": {"id": "ConditionalExample", "version": "1.0"},
        "parameters": [
            {
                "name": "Age",
                "parameterType": "{urn:hl7-org:elm-types:r1}Integer"
            }
        ],
        "statements": {
            "def": [
                {
                    "name": "IsAdult",
                    "expression": {
                        "type": "GreaterOrEqual",
                        "operand": [
                            {"type": "ParameterRef", "name": "Age"},
                            {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "18"}
                        ]
                    }
                },
                {
                    "name": "Category",
                    "expression": {
                        "type": "If",
                        "condition": {
                            "type": "Less",
                            "operand": [
                                {"type": "ParameterRef", "name": "Age"},
                                {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "18"}
                            ]
                        },
                        "then": {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}String", "value": "Minor"},
                        "else": {
                            "type": "If",
                            "condition": {
                                "type": "Less",
                                "operand": [
                                    {"type": "ParameterRef", "name": "Age"},
                                    {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}Integer", "value": "65"}
                                ]
                            },
                            "then": {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}String", "value": "Adult"},
                            "else": {"type": "Literal", "valueType": "{urn:hl7-org:elm-types:r1}String", "value": "Senior"}
                        }
                    }
                }
            ]
        }
    }
}
```

**Try different ages:**

```python
evaluator = ELMEvaluator()
evaluator.load("conditionals.elm.json")

for age in [15, 30, 70]:
    is_adult = evaluator.evaluate_definition("IsAdult", parameters={"Age": age})
    category = evaluator.evaluate_definition("Category", parameters={"Age": age})
    print(f"Age {age}: IsAdult={is_adult}, Category={category}")

# Output:
# Age 15: IsAdult=False, Category=Minor
# Age 30: IsAdult=True, Category=Adult
# Age 70: IsAdult=True, Category=Senior
```

---

## Part 6: Patient Data

### Using Patient Context

Create `patient.elm.json`:

```json
{
    "library": {
        "identifier": {"id": "PatientExample", "version": "1.0"},
        "usings": [
            {
                "localIdentifier": "FHIR",
                "uri": "http://hl7.org/fhir",
                "version": "4.0.1"
            }
        ],
        "contexts": [
            {"name": "Patient"}
        ],
        "statements": {
            "def": [
                {
                    "name": "PatientGender",
                    "context": "Patient",
                    "expression": {
                        "type": "Property",
                        "path": "gender",
                        "source": {"type": "ExpressionRef", "name": "Patient"}
                    }
                },
                {
                    "name": "PatientBirthDate",
                    "context": "Patient",
                    "expression": {
                        "type": "Property",
                        "path": "birthDate",
                        "source": {"type": "ExpressionRef", "name": "Patient"}
                    }
                }
            ]
        }
    }
}
```

**Evaluate with patient:**

```python
evaluator = ELMEvaluator()
evaluator.load("patient.elm.json")

patient = {
    "resourceType": "Patient",
    "id": "example",
    "gender": "male",
    "birthDate": "1990-05-15",
    "name": [{"family": "Smith", "given": ["John"]}]
}

gender = evaluator.evaluate_definition("PatientGender", resource=patient)
birthdate = evaluator.evaluate_definition("PatientBirthDate", resource=patient)

print(f"Gender: {gender}")       # male
print(f"Birth Date: {birthdate}")  # 1990-05-15
```

---

## Part 7: Converting CQL to ELM

The easiest way to create ELM is to write CQL and convert it.

### Using the CLI

```bash
# Convert CQL to ELM
fhir elm convert library.cql -o library.elm.json

# Or use the CQL export command
fhir cql export library.cql -o library.elm.json
```

### Using Python

```python
from fhirkit.engine.elm import ELMSerializer

serializer = ELMSerializer()

cql_source = """
    library MyLibrary version '1.0'
    using FHIR version '4.0.1'

    context Patient

    define PatientAge: AgeInYears()
    define IsAdult: PatientAge >= 18

    define AgeCategory:
        case
            when PatientAge < 18 then 'Pediatric'
            when PatientAge < 65 then 'Adult'
            else 'Senior'
        end
"""

# Convert to ELM JSON
elm_json = serializer.serialize_library_json(cql_source, indent=2)
print(elm_json)

# Save to file
with open("mylibrary.elm.json", "w") as f:
    f.write(elm_json)
```

### Using CQLEvaluator

```python
from fhirkit.engine.cql import CQLEvaluator

evaluator = CQLEvaluator()

# Compile CQL
library = evaluator.compile("""
    library Example version '1.0'
    define Sum: 1 + 2 + 3
    define Greeting: 'Hello!'
""")

# Export to ELM
elm_json = evaluator.to_elm_json(indent=2)
elm_dict = evaluator.to_elm_dict()
elm_model = evaluator.to_elm()
```

---

## Part 8: Building an Evaluation Pipeline

### Complete Example

```python
from fhirkit.engine.elm import ELMEvaluator, ELMSerializer
from fhirkit.engine.cql import InMemoryDataSource
import json

# Step 1: Define CQL logic
cql_source = """
    library RiskAssessment version '1.0'
    using FHIR version '4.0.1'

    parameter "Risk Threshold" Integer default 3

    context Patient

    define PatientAge: AgeInYears()

    define HasDiabetes:
        exists([Condition] C where C.code.coding.code = '44054006')

    define HasHypertension:
        exists([Condition] C where C.code.coding.code = '38341003')

    define RiskScore:
        (if PatientAge >= 50 then 1 else 0) +
        (if HasDiabetes then 2 else 0) +
        (if HasHypertension then 1 else 0)

    define IsHighRisk:
        RiskScore >= "Risk Threshold"
"""

# Step 2: Convert to ELM
serializer = ELMSerializer()
elm_json = serializer.serialize_library_json(cql_source)

# Step 3: Create data source with patient data
data_source = InMemoryDataSource()

# Add patient
patient = {
    "resourceType": "Patient",
    "id": "patient-1",
    "birthDate": "1965-03-15",
    "gender": "male"
}
data_source.add_resource(patient)

# Add conditions
data_source.add_resource({
    "resourceType": "Condition",
    "id": "cond-1",
    "subject": {"reference": "Patient/patient-1"},
    "code": {"coding": [{"code": "44054006", "system": "http://snomed.info/sct"}]}
})

# Step 4: Evaluate
evaluator = ELMEvaluator(data_source=data_source)
evaluator.load(elm_json)

results = evaluator.evaluate_all_definitions(resource=patient)

print("Risk Assessment Results:")
print(f"  Patient Age: {results.get('PatientAge')}")
print(f"  Has Diabetes: {results.get('HasDiabetes')}")
print(f"  Has Hypertension: {results.get('HasHypertension')}")
print(f"  Risk Score: {results.get('RiskScore')}")
print(f"  Is High Risk: {results.get('IsHighRisk')}")
```

**Output:**
```
Risk Assessment Results:
  Patient Age: 59
  Has Diabetes: True
  Has Hypertension: False
  Risk Score: 3
  Is High Risk: True
```

---

## Part 9: Exercises

### Exercise 1: Temperature Converter

Create an ELM file that:
1. Takes a `Celsius` parameter
2. Calculates `Fahrenheit` using the formula: F = C * 9/5 + 32
3. Determines if it's `Freezing` (below 0C), `Cold` (0-15C), `Warm` (15-25C), or `Hot` (above 25C)

### Exercise 2: BMI Calculator

Create CQL that:
1. Takes `WeightKg` and `HeightCm` parameters
2. Calculates BMI: weight / (height/100)^2
3. Returns a category: Underweight (<18.5), Normal (18.5-25), Overweight (25-30), Obese (>30)

Convert it to ELM and evaluate with different values.

### Exercise 3: Patient Risk Assessment

Using the pipeline from Part 8:
1. Add more risk factors (smoking, family history)
2. Add weighted scoring
3. Evaluate across multiple patients

---

## Summary

You've learned how to:

1. **Load ELM** from files and JSON strings
2. **Evaluate definitions** with and without parameters
3. **Use patient data** for clinical logic
4. **Convert CQL to ELM** using CLI and Python
5. **Build pipelines** for real-world applications

## Next Steps

- [ELM Guide](elm-guide.md) - Conceptual overview
- [ELM API](elm-api.md) - Complete Python API
- [ELM Reference](elm-reference.md) - All expression types
- [CQL Tutorial](cql-tutorial.md) - Learn CQL syntax
