library ActiveConditions version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Conditions":
  [Condition]

define "Condition Count":
  Count([Condition])

define "Active Conditions":
  [Condition] C
    where C.clinicalStatus.coding.code contains 'active'

define "Resolved Conditions":
  [Condition] C
    where C.clinicalStatus.coding.code contains 'resolved'

define "Inactive Conditions":
  [Condition] C
    where C.clinicalStatus.coding.code contains 'inactive'

define "Confirmed Conditions":
  [Condition] C
    where C.verificationStatus.coding.code contains 'confirmed'

define "Problem List":
  [Condition] C
    where C.category.coding.code contains 'problem-list-item'
      and C.clinicalStatus.coding.code contains 'active'

define "Encounter Diagnoses":
  [Condition] C
    where C.category.coding.code contains 'encounter-diagnosis'

define "Active Problem List":
  "Problem List" C
    where C.clinicalStatus.coding.code contains 'active'

define "Condition Names":
  "Active Conditions" C return C.code.coding.first().display

define "Conditions By Onset":
  "Active Conditions" C sort by onset
