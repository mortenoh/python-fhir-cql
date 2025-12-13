/*
 * Terminology - Working with codes and value sets in CQL
 */
library Terminology version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// Code System Definitions
// =====================================================

codesystem "LOINC": 'http://loinc.org'
codesystem "SNOMED-CT": 'http://snomed.info/sct'
codesystem "ICD-10-CM": 'http://hl7.org/fhir/sid/icd-10-cm'
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "CPT": 'http://www.ama-assn.org/go/cpt'
codesystem "CVX": 'http://hl7.org/fhir/sid/cvx'
codesystem "UCUM": 'http://unitsofmeasure.org'

// =====================================================
// Value Set Definitions
// =====================================================

// Condition value sets
valueset "Diabetes Mellitus": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.103.12.1001'
valueset "Essential Hypertension": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.104.12.1011'
valueset "Heart Failure": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.104.12.1012'
valueset "Chronic Kidney Disease": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.109.12.1028'

// Laboratory value sets
valueset "HbA1c Lab Test": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.198.12.1013'
valueset "Serum Creatinine": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.198.12.1018'
valueset "LDL Cholesterol": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.198.12.1016'
valueset "Blood Pressure": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.198.12.1009'

// Medication value sets
valueset "ACE Inhibitors": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.196.12.1003'
valueset "Statins": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.196.12.1030'
valueset "Insulin Medications": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.196.12.1017'

// Encounter value sets
valueset "Office Visit": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.101.12.1001'
valueset "Annual Wellness Visit": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.101.12.1063'
valueset "Preventive Care": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.101.12.1022'

// =====================================================
// Individual Code Definitions
// =====================================================

// LOINC codes
code "HbA1c LOINC": '4548-4' from "LOINC" display 'Hemoglobin A1c/Hemoglobin.total'
code "Glucose LOINC": '2339-0' from "LOINC" display 'Glucose [Mass/volume] in Blood'
code "Creatinine LOINC": '2160-0' from "LOINC" display 'Creatinine [Mass/volume] in Serum'
code "eGFR LOINC": '33914-3' from "LOINC" display 'GFR estimated'

// SNOMED codes
code "Type 2 Diabetes SNOMED": '44054006' from "SNOMED-CT" display 'Type 2 diabetes mellitus'
code "Type 1 Diabetes SNOMED": '46635009' from "SNOMED-CT" display 'Type 1 diabetes mellitus'
code "Hypertension SNOMED": '38341003' from "SNOMED-CT" display 'Hypertensive disorder'

// ICD-10 codes
code "Type 2 Diabetes ICD10": 'E11' from "ICD-10-CM" display 'Type 2 diabetes mellitus'
code "Hypertension ICD10": 'I10' from "ICD-10-CM" display 'Essential (primary) hypertension'

// =====================================================
// Concept Definitions
// =====================================================

// Diabetes concept (multiple coding systems)
concept "Diabetes": {
    "Type 2 Diabetes SNOMED",
    "Type 2 Diabetes ICD10"
} display 'Diabetes Mellitus'

// =====================================================
// Terminology Operations
// =====================================================

context Patient

// Check membership in value set
define HasDiabetes:
    exists([Condition: "Diabetes Mellitus"])

define HasHypertension:
    exists([Condition: "Essential Hypertension"])

// Check specific code
define HasType2Diabetes:
    exists([Condition: code in "Type 2 Diabetes SNOMED"])

// Code comparison with equivalence
define DiabetesConditions:
    [Condition] C
        where C.code ~ "Diabetes"

// =====================================================
// Using Codes in Queries
// =====================================================

// Retrieve by value set
define HbA1cResults:
    [Observation: "HbA1c Lab Test"]

// Retrieve by specific code
define GlucoseResults:
    [Observation: "Glucose LOINC"]

// =====================================================
// Unit Handling (UCUM)
// =====================================================

// Convert units
define function ConvertMgDlToMmolL(value Decimal) returns Decimal:
    value / 18.0

define function ConvertMmolLToMgDl(value Decimal) returns Decimal:
    value * 18.0

// =====================================================
// Practical Examples
// =====================================================

// Find all diabetes-related labs
define DiabetesRelatedLabs:
    [Observation: "HbA1c Lab Test"]
    union [Observation: "Glucose LOINC"]

// Find all cardiovascular conditions
define CardiovascularConditions:
    [Condition: "Essential Hypertension"]
    union [Condition: "Heart Failure"]

// Active diabetes management medications
define DiabetesMedications:
    [MedicationRequest: "Insulin Medications"]

// Multi-condition check
define HasDiabetesAndHypertension:
    HasDiabetes and HasHypertension

// Qualifying encounters for measure
define QualifyingEncounters:
    [Encounter: "Office Visit"]
    union [Encounter: "Annual Wellness Visit"]
    union [Encounter: "Preventive Care"]

// =====================================================
// Code Display Functions
// =====================================================

// Format code for display
define function FormatCode(codeValue String, systemValue String) returns String:
    codeValue + ' (' + systemValue + ')'

// Get human-readable summary
define function GetConditionDisplay(cond Condition) returns String:
    Coalesce(cond.code.text, First(cond.code.coding).display, 'Unknown')
