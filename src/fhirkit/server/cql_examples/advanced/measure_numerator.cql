library MeasureNumerator version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

// Example: Diabetes HbA1c Control - Numerator (HbA1c < 8%)

parameter "Measurement Period" Interval<DateTime>

codesystem "LOINC": 'http://loinc.org'
code "HbA1c": '4548-4' from "LOINC"

context Patient

define "Has Diabetes":
  exists ([Condition] C
    where (C.code.coding.code contains 'E10' or C.code.coding.code contains 'E11')
    and C.clinicalStatus.coding.code contains 'active')

define "Denominator":
  AgeInYears() >= 18 and "Has Diabetes"

define "HbA1c Tests During Period":
  [Observation: "HbA1c"] O
    where O.effective during "Measurement Period"
    and O.status = 'final'

define "Most Recent HbA1c":
  Last("HbA1c Tests During Period" O sort by effective)

define "Most Recent HbA1c Value":
  ("Most Recent HbA1c").value as Quantity

define "HbA1c Less Than 8":
  ("Most Recent HbA1c Value").value < 8.0

define "Numerator":
  "Denominator" and "HbA1c Less Than 8"

define "Performance Rate":
  if "Denominator" then
    if "Numerator" then 1.0 else 0.0
  else null
