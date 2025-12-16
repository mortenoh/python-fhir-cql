library MeasureExclusions version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

// Common Exclusion Criteria for Quality Measures

parameter "Measurement Period" Interval<DateTime>

context Patient

// Hospice Exclusion
define "Hospice Care":
  exists ([Encounter] E
    where E.type.coding.code contains 'hospice'
    and E.period overlaps "Measurement Period")

define "Hospice Order":
  exists ([ServiceRequest] S
    where S.code.coding.code contains 'hospice'
    and S.authoredOn during "Measurement Period")

define "Hospice Exclusion":
  "Hospice Care" or "Hospice Order"

// Palliative Care
define "Palliative Care":
  exists ([Encounter] E
    where E.type.coding.display contains 'palliative'
    and E.period overlaps "Measurement Period")

// Advanced Illness
define "Frailty":
  exists ([Condition] C
    where C.code.coding.display contains 'frailty'
    and C.clinicalStatus.coding.code contains 'active')

define "Dementia":
  exists ([Condition] C
    where C.code.coding.code contains 'F03'
    and C.clinicalStatus.coding.code contains 'active')

define "Advanced Illness Exclusion":
  AgeInYears() >= 66 and ("Frailty" or "Dementia")

// Combined Exclusions
define "Denominator Exclusion":
  "Hospice Exclusion"
    or "Palliative Care"
    or "Advanced Illness Exclusion"
