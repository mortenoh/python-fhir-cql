library MeasureDenominator version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

// Example: Diabetes HbA1c Control - Denominator

parameter "Measurement Period" Interval<DateTime>

context Patient

define "Age 18 to 75":
  AgeInYearsAt(start of "Measurement Period") in Interval[18, 75]

define "Has Diabetes":
  exists ([Condition] C
    where (C.code.coding.code contains 'E10' or C.code.coding.code contains 'E11')
    and C.clinicalStatus.coding.code contains 'active')

define "Initial Population":
  "Age 18 to 75" and "Has Diabetes"

define "Denominator":
  "Initial Population"

define "Hospice":
  exists ([Encounter] E
    where E.type.coding.code contains 'hospice')

define "Denominator Exclusion":
  "Hospice"

define "In Denominator":
  "Denominator" and not "Denominator Exclusion"
