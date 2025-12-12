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
    from O in [Observation: "Blood Glucose Tests"]
    where O.effective during "Measurement Period"
    return O.value

// Return tuples
define GlucoseSummary:
    from O in [Observation: "Blood Glucose Tests"]
    where O.effective during "Measurement Period"
    return Tuple {
        date: O.effective,
        value: O.value,
        code: O.code.coding[0].code
    }

// Return all (preserve duplicates)
define AllGlucoseValues:
    from O in [Observation: "Blood Glucose Tests"]
    return all O.value

// Return distinct
define DistinctGlucoseDates:
    distinct (
        from O in [Observation: "Blood Glucose Tests"]
        return date from O.effective
    )

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
// Multi-Source Queries
// =====================================================

// Join conditions with medications
define DiabetesWithMedication:
    from C in [Condition: "Diabetes Diagnosis"],
         M in [MedicationRequest: "Antidiabetic Medications"]
    where C.clinicalStatus ~ 'active'
        and M.status = 'active'
    return Tuple {
        conditionCode: C.code,
        medication: M.medication,
        authoredOn: M.authoredOn
    }

// Observations with encounter context
define GlucoseWithEncounter:
    from O in [Observation: "Blood Glucose Tests"],
         E in [Encounter]
    where O.encounter = E.id
        and O.effective during "Measurement Period"
    return Tuple {
        glucoseValue: O.value,
        encounterType: E.type,
        encounterDate: E.period.start
    }

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

// Average value
define AverageGlucose:
    Avg(
        from O in [Observation: "Blood Glucose Tests"]
        where O.effective during "Measurement Period"
        return O.value.value
    )

// Min/Max values
define MinGlucose:
    Min(
        from O in [Observation: "Blood Glucose Tests"]
        return O.value.value
    )

define MaxGlucose:
    Max(
        from O in [Observation: "Blood Glucose Tests"]
        return O.value.value
    )

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
// Complex Clinical Patterns
// =====================================================

// Find lab trend (improving/worsening)
define GlucoseTrend:
    let recentValues:
        from O in [Observation: "Blood Glucose Tests"]
        where O.effective during "Measurement Period"
        sort by effective
        return O.value.value
    return if Count(recentValues) < 2 then 'Insufficient data'
           else if Last(recentValues) < First(recentValues) then 'Improving'
           else if Last(recentValues) > First(recentValues) then 'Worsening'
           else 'Stable'

// Find gaps in care (no tests for 90+ days)
define HasTestingGap:
    exists(
        from O1 in [Observation: "Blood Glucose Tests"],
             O2 in [Observation: "Blood Glucose Tests"]
        where O1.effective < O2.effective
            and days between O1.effective and O2.effective > 90
            and not exists(
                [Observation: "Blood Glucose Tests"] O3
                    where O3.effective > O1.effective
                        and O3.effective < O2.effective
            )
        return true
    )

// Calculate medication adherence (simplified)
define MedicationAdherence:
    let totalDays: days between start of "Measurement Period" and end of "Measurement Period",
        daysWithMed: Count(
            distinct (
                from M in [MedicationStatement: "Antidiabetic Medications"]
                where M.effective overlaps "Measurement Period"
                return date from M.effective
            )
        )
    return if totalDays > 0 then (daysWithMed / totalDays) * 100 else null
