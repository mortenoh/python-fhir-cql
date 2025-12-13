/*
 * CQL Example 25: Population Health and Quality Measures
 *
 * Demonstrates:
 * - Population-level definitions
 * - Quality measure patterns (IPP, Denominator, Numerator)
 * - Cohort identification
 * - Stratification patterns
 * - Aggregate calculations
 */

library PopulationHealth version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "LOINC": 'http://loinc.org'
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "CVX": 'http://hl7.org/fhir/sid/cvx'

// Measurement Period (typically a calendar year)
parameter "Measurement Period" Interval<DateTime>
  default Interval[@2024-01-01T00:00:00, @2024-12-31T23:59:59]

context Patient

// =====================================================
// Patient Demographics
// =====================================================

define PatientAge:
  AgeInYearsAt(start of "Measurement Period")

define PatientGender:
  Patient.gender

define IsAdult:
  PatientAge >= 18

define IsElderly:
  PatientAge >= 65

define IsPediatric:
  PatientAge < 18

// =====================================================
// Diabetes Quality Measure (NQF Example Pattern)
// =====================================================

// Initial Patient Population (IPP)
// Adults 18-75 with diabetes
define "Diabetes IPP":
  PatientAge >= 18
    and PatientAge <= 75
    and exists (
      [Condition] C
        where C.code.coding.code contains '73211009'  // Diabetes
          and C.clinicalStatus.coding.code contains 'active'
    )

// Denominator: IPP members
define "Diabetes Denominator":
  "Diabetes IPP"

// Denominator Exclusions
define "Diabetes Denominator Exclusions":
  exists (
    [Condition] C
      where C.code.coding.code contains '46177005'  // ESRD
        and C.clinicalStatus.coding.code contains 'active'
  )
  or exists (
    [Condition] C
      where C.code.coding.display contains 'hospice'
  )

// Numerator: Has HbA1c < 9% during measurement period
define "Diabetes Numerator":
  exists (
    [Observation] O
      where O.code.coding.code contains '4548-4'  // HbA1c
        and O.status = 'final'
        and O.effective as dateTime during "Measurement Period"
        and (O.value as Quantity).value < 9.0
  )

// Measure Result for this patient
define "Diabetes Measure Met":
  "Diabetes Denominator"
    and not "Diabetes Denominator Exclusions"
    and "Diabetes Numerator"

// =====================================================
// Hypertension Control Measure
// =====================================================

define "Hypertension IPP":
  PatientAge >= 18
    and exists (
      [Condition] C
        where C.code.coding.code contains '38341003'  // Hypertension
          and C.clinicalStatus.coding.code contains 'active'
    )

define "Hypertension Denominator":
  "Hypertension IPP"

// Most recent blood pressure in measurement period
define "Most Recent BP":
  Last(
    [Observation] O
      where O.code.coding.code contains '85354-9'  // Blood pressure panel
        and O.status = 'final'
        and O.effective as dateTime during "Measurement Period"
      sort by effective as dateTime
  )

// BP controlled (<140/90)
define "BP Controlled":
  "Most Recent BP" is not null
    and exists (
      "Most Recent BP".component C
        where C.code.coding.code contains '8480-6'  // Systolic
          and (C.value as Quantity).value < 140
    )
    and exists (
      "Most Recent BP".component C
        where C.code.coding.code contains '8462-4'  // Diastolic
          and (C.value as Quantity).value < 90
    )

define "Hypertension Numerator":
  "BP Controlled"

// =====================================================
// Colorectal Cancer Screening Measure
// =====================================================

define "CRC Screening IPP":
  PatientAge >= 45 and PatientAge <= 75

define "CRC Screening Denominator":
  "CRC Screening IPP"

// Has colonoscopy in last 10 years
define "Has Colonoscopy":
  exists (
    [Procedure] P
      where P.code.coding.code contains '73761001'  // Colonoscopy
        and P.status = 'completed'
        and P.performed as dateTime >= Today() - 10 years
  )

// Has FIT/FOBT in last year
define "Has FIT":
  exists (
    [Observation] O
      where O.code.coding.code contains '14563-1'  // FOBT
        and O.status = 'final'
        and O.effective as dateTime during "Measurement Period"
  )

define "CRC Screening Numerator":
  "Has Colonoscopy" or "Has FIT"

// =====================================================
// Influenza Immunization Measure
// =====================================================

define "Flu Vaccine IPP":
  PatientAge >= 6 months

// Flu season: August through March
define "Flu Season":
  Interval[@2024-08-01, @2025-03-31]

define "Has Flu Vaccine":
  exists (
    [Immunization] I
      where I.status = 'completed'
        and I.vaccineCode.coding.code contains '141'  // Flu vaccine
        and I.occurrence as dateTime during "Flu Season"
  )

define "Flu Vaccine Numerator":
  "Has Flu Vaccine"

// =====================================================
// Medication Adherence (Statin Therapy)
// =====================================================

define "Needs Statin Therapy":
  exists (
    [Condition] C
      where (C.code.coding.code contains '414545008'  // Ischemic heart disease
         or C.code.coding.code contains '22298006')    // MI
        and C.clinicalStatus.coding.code contains 'active'
  )

define "On Statin":
  exists (
    [MedicationRequest] M
      where M.status = 'active'
        and M.medication.coding.display contains 'statin'
  )

define "Statin Therapy Appropriate":
  not "Needs Statin Therapy"
    or "On Statin"

// =====================================================
// Care Gap Identification
// =====================================================

define "Diabetes Care Gaps":
  Tuple {
    needsHbA1c: "Diabetes Denominator" and not exists (
      [Observation] O
        where O.code.coding.code contains '4548-4'
          and O.effective as dateTime during "Measurement Period"
    ),
    needsEyeExam: "Diabetes Denominator" and not exists (
      [Procedure] P
        where P.code.coding.code contains '36228006'  // Eye exam
          and P.performed as dateTime >= Today() - 1 year
    ),
    needsFootExam: "Diabetes Denominator" and not exists (
      [Procedure] P
        where P.code.coding.display contains 'foot exam'
          and P.performed as dateTime >= Today() - 1 year
    )
  }

define "Prevention Care Gaps":
  Tuple {
    needsFluVaccine: "Flu Vaccine IPP" and not "Has Flu Vaccine",
    needsCRCScreening: "CRC Screening Denominator" and not "CRC Screening Numerator",
    needsStatinReview: "Needs Statin Therapy" and not "On Statin"
  }

// =====================================================
// Risk Stratification
// =====================================================

define "Chronic Condition Count":
  Count(
    [Condition] C
      where C.clinicalStatus.coding.code contains 'active'
  )

define "Risk Tier":
  case
    when "Chronic Condition Count" >= 5 then 'Very High'
    when "Chronic Condition Count" >= 3 then 'High'
    when "Chronic Condition Count" >= 1 then 'Moderate'
    else 'Low'
  end

// ED utilization last year
define "ED Visits Last Year":
  Count(
    [Encounter] E
      where E.class.code = 'EMER'
        and E.status = 'finished'
        and E.period.start during "Measurement Period"
  )

define "High ED Utilizer":
  "ED Visits Last Year" >= 4

// Hospitalization last year
define "Inpatient Admissions Last Year":
  Count(
    [Encounter] E
      where E.class.code = 'IMP'
        and E.status = 'finished'
        and E.period.start during "Measurement Period"
  )

define "Frequent Hospitalizations":
  "Inpatient Admissions Last Year" >= 2

// =====================================================
// Age Group Stratification
// =====================================================

define "Age Group":
  case
    when PatientAge < 18 then 'Pediatric'
    when PatientAge >= 18 and PatientAge < 40 then 'Young Adult'
    when PatientAge >= 40 and PatientAge < 65 then 'Middle Age'
    when PatientAge >= 65 and PatientAge < 75 then 'Young Elderly'
    else 'Elderly 75+'
  end

// =====================================================
// Multi-Measure Dashboard
// =====================================================

define "Quality Measure Summary":
  Tuple {
    diabetes: if "Diabetes IPP" then
      Tuple {
        inDenominator: "Diabetes Denominator" and not "Diabetes Denominator Exclusions",
        measureMet: "Diabetes Measure Met"
      }
    else null,
    hypertension: if "Hypertension IPP" then
      Tuple {
        inDenominator: true,
        measureMet: "Hypertension Numerator"
      }
    else null,
    crcScreening: if "CRC Screening IPP" then
      Tuple {
        inDenominator: true,
        measureMet: "CRC Screening Numerator"
      }
    else null,
    fluVaccine: if "Flu Vaccine IPP" then
      Tuple {
        inDenominator: true,
        measureMet: "Flu Vaccine Numerator"
      }
    else null
  }

// =====================================================
// Population Health Summary
// =====================================================

define "Patient Summary":
  Tuple {
    age: PatientAge,
    gender: PatientGender,
    ageGroup: "Age Group",
    riskTier: "Risk Tier",
    chronicConditionCount: "Chronic Condition Count",
    edVisitsLastYear: "ED Visits Last Year",
    inpatientAdmissionsLastYear: "Inpatient Admissions Last Year",
    highUtilizer: "High ED Utilizer" or "Frequent Hospitalizations"
  }

// =====================================================
// Cohort Definitions (for population queries)
// =====================================================

// Patients eligible for diabetes management program
define "Diabetes Program Eligible":
  "Diabetes IPP"
    and "Chronic Condition Count" >= 2
    and (
      not "Diabetes Numerator"  // HbA1c not controlled
      or "ED Visits Last Year" >= 2
    )

// High-risk patients for care management
define "Care Management Eligible":
  "Risk Tier" in {'High', 'Very High'}
    and ("High ED Utilizer" or "Frequent Hospitalizations")

// Patients due for preventive care outreach
define "Preventive Care Outreach":
  not "Has Flu Vaccine"
    or ("CRC Screening IPP" and not "CRC Screening Numerator")
