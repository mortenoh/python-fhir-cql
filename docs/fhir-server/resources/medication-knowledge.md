# MedicationKnowledge

## Overview

The MedicationKnowledge resource provides drug reference information including dosing guidelines, administration instructions, drug costs, and packaging information. It is used by clinical decision support systems and pharmacy applications.

## FHIR R4 Specification

See the official HL7 specification: [https://hl7.org/fhir/R4/medicationknowledge.html](https://hl7.org/fhir/R4/medicationknowledge.html)

## Supported Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Logical ID of the resource |
| `meta` | Meta | Resource metadata |
| `code` | CodeableConcept | Medication code (RxNorm) |
| `status` | code | active, inactive, entered-in-error |
| `manufacturer` | Reference(Organization) | Drug manufacturer |
| `doseForm` | CodeableConcept | Dose form (tablet, capsule, etc.) |
| `amount` | Quantity | Amount of drug in package |
| `synonym` | string[] | Additional names |
| `relatedMedicationKnowledge` | BackboneElement[] | Related medications |
| `associatedMedication` | Reference(Medication)[] | Associated medication |
| `productType` | CodeableConcept[] | Product type |
| `monograph` | BackboneElement[] | Drug monograph |
| `ingredient` | BackboneElement[] | Active ingredients |
| `preparationInstruction` | markdown | Preparation instructions |
| `intendedRoute` | CodeableConcept[] | Route of administration |
| `cost` | BackboneElement[] | Drug costs |
| `monitoringProgram` | BackboneElement[] | REMS programs |
| `administrationGuidelines` | BackboneElement[] | Dosing guidelines |
| `medicineClassification` | BackboneElement[] | Drug classification |
| `packaging` | BackboneElement | Packaging details |
| `drugCharacteristic` | BackboneElement[] | Drug characteristics |
| `contraindication` | Reference(DetectedIssue)[] | Contraindications |
| `regulatory` | BackboneElement[] | Regulatory info |
| `kinetics` | BackboneElement[] | Pharmacokinetics |

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `_id` | token | Resource ID | `_id=mk-001` |
| `code` | token | Drug code | `code=860975` |
| `status` | token | Status | `status=active` |
| `doseform` | token | Dose form | `doseform=385055001` |
| `manufacturer` | reference | Manufacturer | `manufacturer=Organization/456` |
| `classification` | token | Drug class | `classification=N06AB03` |
| `ingredient` | reference | Ingredient | `ingredient=Substance/123` |
| `ingredient-code` | token | Ingredient code | `ingredient-code=387458008` |
| `monograph-type` | token | Monograph type | `monograph-type=LOINC` |

## Examples

### Create MedicationKnowledge

```bash
curl -X POST http://localhost:8080/baseR4/MedicationKnowledge \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "MedicationKnowledge",
    "code": {
      "coding": [{
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "860975",
        "display": "Metformin hydrochloride 500 MG Oral Tablet"
      }],
      "text": "Metformin 500mg"
    },
    "status": "active",
    "doseForm": {
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "385055001",
        "display": "Tablet"
      }]
    },
    "amount": {
      "value": 100,
      "unit": "tablets",
      "system": "http://unitsofmeasure.org",
      "code": "{tablet}"
    },
    "synonym": ["Glucophage", "Metformin HCl"],
    "intendedRoute": [{
      "coding": [{
        "system": "http://snomed.info/sct",
        "code": "26643006",
        "display": "Oral route"
      }]
    }],
    "administrationGuidelines": [{
      "dosage": [{
        "type": {
          "coding": [{
            "code": "ordered",
            "display": "Ordered"
          }]
        },
        "dosage": [{
          "text": "Take 1 tablet twice daily with meals"
        }]
      }]
    }],
    "packaging": {
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-package-type",
          "code": "bot",
          "display": "Bottle"
        }]
      },
      "quantity": {
        "value": 100,
        "unit": "tablets"
      }
    }
  }'
```

### Search MedicationKnowledge

```bash
# By drug code
curl "http://localhost:8080/baseR4/MedicationKnowledge?code=860975"

# By status
curl "http://localhost:8080/baseR4/MedicationKnowledge?status=active"

# By dose form
curl "http://localhost:8080/baseR4/MedicationKnowledge?doseform=385055001"

# By drug class
curl "http://localhost:8080/baseR4/MedicationKnowledge?classification=A10BA02"
```

## Status Codes

| Code | Display | Description |
|------|---------|-------------|
| active | Active | Available for prescribing |
| inactive | Inactive | Not available |
| entered-in-error | Entered in Error | Data entry error |

## Common Dose Forms (SNOMED CT)

| Code | Display |
|------|---------|
| 385055001 | Tablet |
| 385049006 | Capsule |
| 385023001 | Oral solution |
| 385220007 | Injection solution |
| 421720008 | Spray |
| 385099005 | Cream |
| 385043007 | Ointment |

## Common Routes (SNOMED CT)

| Code | Display |
|------|---------|
| 26643006 | Oral route |
| 47625008 | Intravenous route |
| 78421000 | Intramuscular route |
| 45890007 | Transdermal route |
| 6064005 | Topical route |
| 46713006 | Nasal route |

## Drug Classifications (ATC)

| Code | Display |
|------|---------|
| A10BA02 | Metformin |
| C10AA | HMG CoA reductase inhibitors |
| N02BE01 | Paracetamol |
| N06AB03 | Fluoxetine |
| C09AA | ACE inhibitors |
