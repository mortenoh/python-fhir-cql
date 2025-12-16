library MeasureIPP version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

// Example: Diabetes HbA1c Control Measure - Initial Population

parameter "Measurement Period" Interval<DateTime>

context Patient

define "In Measurement Period":
  "Measurement Period"

define "Age 18 to 75":
  AgeInYearsAt(start of "Measurement Period") in Interval[18, 75]

define "Has Diabetes Diagnosis":
  exists ([Condition] C
    where C.code.coding.code contains 'E10'
      or C.code.coding.code contains 'E11'
    and C.clinicalStatus.coding.code contains 'active')

define "Had Qualifying Encounter":
  exists ([Encounter] E
    where E.period starts during "Measurement Period"
    and E.status = 'finished')

define "Initial Population":
  "Age 18 to 75"
    and "Has Diabetes Diagnosis"
    and "Had Qualifying Encounter"

define "In Initial Population":
  "Initial Population"
