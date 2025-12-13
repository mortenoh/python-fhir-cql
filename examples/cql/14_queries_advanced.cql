/*
 * Advanced Queries - Complex query patterns in CQL
 */
library AdvancedQueries version '1.0.0'

using FHIR version '4.0.1'

// Code systems and value sets
codesystem "LOINC": 'http://loinc.org'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "ICD10": 'http://hl7.org/fhir/sid/icd-10-cm'

valueset "Diabetes Diagnosis": 'http://example.org/ValueSet/diabetes'
valueset "Blood Glucose Tests": 'http://example.org/ValueSet/glucose-tests'
valueset "Antidiabetic Medications": 'http://example.org/ValueSet/antidiabetic-meds'

// Parameters
parameter "Measurement Period" Interval<DateTime>
    default Interval[@2024-01-01T00:00:00, @2024-12-31T23:59:59]

context Patient

// =====================================================
// Basic Retrieve
// =====================================================

// Get all conditions
define AllConditions:
    [Condition]

// Get conditions by value set
define DiabetesConditions:
    [Condition: "Diabetes Diagnosis"]

// Get observations by value set
define GlucoseTests:
    [Observation: "Blood Glucose Tests"]

// =====================================================
// Simple Filtering
// =====================================================

// Active conditions only
define ActiveDiabetes:
    [Condition: "Diabetes Diagnosis"] C
        where C.clinicalStatus ~ 'active'

// Observations in measurement period
define GlucoseInPeriod:
    [Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"

// Medications with specific status
define ActiveMedications:
    [MedicationRequest] M
        where M.status in {'active', 'completed'}

// =====================================================
// Query with Multiple Conditions
// =====================================================

// High glucose readings (>= 126 mg/dL)
define HighGlucose:
    [Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
            and O.value >= 126 'mg/dL'

// Recent abnormal results
define RecentAbnormalGlucose:
    [Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
            and O.status = 'final'
            and O.value >= 126 'mg/dL'
        sort by effective desc

// =====================================================
// Let Clauses
// =====================================================

// Extract and compute in queries
define GlucoseWithAge:
    [Observation: "Blood Glucose Tests"] O
        let ageAtTest: years between Patient.birthDate and O.effective
        where O.effective during "Measurement Period"
        return Tuple {
            value: O.value,
            date: O.effective,
            patientAge: ageAtTest
        }

// Multiple let clauses
define AnalyzedGlucose:
    [Observation: "Blood Glucose Tests"] O
        let value: O.value.value,
            unit: O.value.unit,
            isHigh: O.value >= 126 'mg/dL',
            isLow: O.value < 70 'mg/dL'
        where O.effective during "Measurement Period"
        return Tuple {
            observationDate: O.effective,
            glucoseValue: value,
            glucoseUnit: unit,
            status: if isHigh then 'High'
                    else if isLow then 'Low'
                    else 'Normal'
        }

// =====================================================
// Return Clauses
// =====================================================

// Return specific elements
define GlucoseValues:
    [Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
        return O.value

// Return tuples
define GlucoseSummary:
    [Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
        return Tuple {
            date: O.effective,
            value: O.value,
            code: O.code.coding[0].code
        }

// =====================================================
// Sorting
// =====================================================

// Sort by single field ascending
define GlucoseByDate:
    [Observation: "Blood Glucose Tests"] O
        sort by effective

// Sort descending
define GlucoseByDateDesc:
    [Observation: "Blood Glucose Tests"] O
        sort by effective desc

// Sort by multiple fields
define GlucoseSorted:
    [Observation: "Blood Glucose Tests"] O
        sort by status, effective desc

// =====================================================
// With/Without Clauses
// =====================================================

// Patients with diabetes who have glucose tests
define DiabeticsWithGlucoseTests:
    [Condition: "Diabetes Diagnosis"] C
        with [Observation: "Blood Glucose Tests"] O
            such that O.effective during "Measurement Period"
        where C.clinicalStatus ~ 'active'

// Diabetics without recent glucose tests
define DiabeticsWithoutRecentTests:
    [Condition: "Diabetes Diagnosis"] C
        without [Observation: "Blood Glucose Tests"] O
            such that O.effective during "Measurement Period"
        where C.clinicalStatus ~ 'active'

// =====================================================
// Aggregate Queries
// =====================================================

// Count results
define GlucoseTestCount:
    Count([Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period")

// =====================================================
// First/Last with Sort
// =====================================================

// Most recent glucose test
define MostRecentGlucose:
    Last([Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
        sort by effective)

// First glucose test in period
define FirstGlucoseInPeriod:
    First([Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
        sort by effective)

// =====================================================
// Existence Checks
// =====================================================

// Has any glucose test
define HasGlucoseTest:
    exists([Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period")

// Has high glucose
define HasHighGlucose:
    exists([Observation: "Blood Glucose Tests"] O
        where O.effective during "Measurement Period"
            and O.value >= 126 'mg/dL')

// Has active diabetes
define HasActiveDiabetes:
    exists([Condition: "Diabetes Diagnosis"] C
        where C.clinicalStatus ~ 'active')

// =====================================================
// Practical Examples
// =====================================================

// Check if patient needs screening
define NeedsGlucoseScreening:
    AgeInYears() >= 45
        and not exists([Observation: "Blood Glucose Tests"] O
            where O.effective during "Measurement Period")

// Calculate days since last test
define DaysSinceLastGlucoseTest:
    days between
        (Last([Observation: "Blood Glucose Tests"] O
            where O.effective during "Measurement Period"
            sort by effective)).effective
        and Today()
