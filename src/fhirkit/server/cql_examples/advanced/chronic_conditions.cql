library ChronicConditions version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Active Conditions":
  [Condition] C
    where C.clinicalStatus.coding.code contains 'active'

define "Chronic Conditions":
  "All Active Conditions" C
    where C.code.coding.display contains 'chronic'
      or years between C.onset and Today() >= 1

define "Has Hypertension":
  exists ([Condition] C
    where C.code.coding.code contains 'I10'
      or C.code.coding.display contains 'hypertension')

define "Has Heart Disease":
  exists ([Condition] C
    where C.code.coding.code contains 'I25'
      or C.code.coding.display contains 'coronary'
      or C.code.coding.display contains 'heart disease')

define "Has COPD":
  exists ([Condition] C
    where C.code.coding.code contains 'J44'
      or C.code.coding.display contains 'COPD')

define "Has Asthma":
  exists ([Condition] C
    where C.code.coding.code contains 'J45'
      or C.code.coding.display contains 'asthma')

define "Has CKD":
  exists ([Condition] C
    where C.code.coding.code contains 'N18'
      or C.code.coding.display contains 'kidney disease')

define "Chronic Condition Count":
  Count("Chronic Conditions")

define "Has Multiple Chronic":
  "Chronic Condition Count" >= 2
