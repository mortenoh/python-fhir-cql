# NutritionOrder

## Overview

The NutritionOrder resource represents a request for oral diets, nutritional supplements, enteral nutrition, or infant formula. It captures diet orders and restrictions for patients.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/nutritionorder.html](https://hl7.org/fhir/R4/nutritionorder.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `status` | code | draft, active, on-hold, revoked, completed, entered-in-error, unknown |
| `intent` | code | proposal, plan, directive, order, etc. |
| `patient` | Reference(Patient) | Patient the order is for |
| `encounter` | Reference(Encounter) | Encounter for this order |
| `dateTime` | dateTime | Date and time order was created |
| `orderer` | Reference(Practitioner) | Who ordered the diet |
| `foodPreferenceModifier` | CodeableConcept[] | Food preferences (kosher, halal, etc.) |
| `excludeFoodModifier` | CodeableConcept[] | Foods to exclude (allergies) |
| `oralDiet` | BackboneElement | Oral diet specifications |
| `supplement` | BackboneElement[] | Nutritional supplements |
| `enteralFormula` | BackboneElement | Enteral nutrition |
| `note` | Annotation[] | Additional notes |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=no-001` |
| `patient` | reference | Patient | `patient=Patient/123` |
| `status` | token | Order status | `status=active` |
| `datetime` | date | Order date | `datetime=2024-01-15` |
| `orderer` | reference | Who ordered | `orderer=Practitioner/doc-1` |
| `encounter` | reference | Related encounter | `encounter=Encounter/enc-1` |

## Examples

### Create a NutritionOrder

```bash
curl -X POST http://localhost:8080/baseR4/NutritionOrder \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "NutritionOrder",
    "status": "active",
    "intent": "order",
    "patient": {"reference": "Patient/patient-1"},
    "dateTime": "2024-01-15T09:00:00Z",
    "orderer": {"reference": "Practitioner/doc-1"},
    "foodPreferenceModifier": [{
      "coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/diet",
        "code": "kosher",
        "display": "Kosher"
      }]
    }],
    "excludeFoodModifier": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "227493005",
        "display": "Shellfish"
      }],
      "text": "Shellfish (patient allergy)"
    }],
    "oralDiet": {
      "type": [{
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "160670007",
          "display": "Diabetic diet"
        }]
      }],
      "nutrient": [{
        "modifier": {
          "coding": [{
            "system": "http://snomed.info/sct",
            "code": "2331003",
            "display": "Carbohydrate"
          }]
        },
        "amount": {
          "value": 75,
          "unit": "grams"
        }
      }],
      "instruction": "Limit carbohydrates to 75g per meal"
    }
  }'
```

### Search NutritionOrders

```bash
# By patient
curl "http://localhost:8080/baseR4/NutritionOrder?patient=Patient/patient-1"

# Active orders
curl "http://localhost:8080/baseR4/NutritionOrder?status=active"

# By orderer
curl "http://localhost:8080/baseR4/NutritionOrder?orderer=Practitioner/doc-1"
```

## Diet Types (SNOMED CT)

| Code | Display |
|------|---------|
| 160670007 | Diabetic diet |
| 226358006 | Low fat diet |
| 1156074008 | Low sodium diet |
| 160661001 | High fiber diet |
| 160669005 | Low residue diet |
| 38903004 | Gluten-free diet |
| 226351003 | Lactose-free diet |
| 228049004 | Soft diet |
| 439021000124105 | Pureed diet |

## Status Codes

| Code | Description |
|------|-------------|
| draft | Being developed |
| active | Currently active |
| on-hold | Temporarily paused |
| revoked | Order revoked |
| completed | Order completed |
| entered-in-error | Entry was made in error |
| unknown | Status unknown |
