library DiabetesCheck version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

codesystem "ICD10": 'http://hl7.org/fhir/sid/icd-10-cm'
codesystem "SNOMED": 'http://snomed.info/sct'

valueset "Diabetes": 'http://example.org/fhir/ValueSet/diabetes'

code "Type 1 Diabetes ICD": 'E10' from "ICD10"
code "Type 2 Diabetes ICD": 'E11' from "ICD10"
code "Diabetes SNOMED": '73211009' from "SNOMED"

context Patient

define "All Diabetes Conditions":
  [Condition] C
    where C.code.coding.code contains 'E10'
      or C.code.coding.code contains 'E11'
      or C.code.coding.code contains '73211009'
      or C.code.coding.display contains 'diabetes'

define "Has Diabetes":
  exists "All Diabetes Conditions"

define "Active Diabetes":
  "All Diabetes Conditions" C
    where C.clinicalStatus.coding.code contains 'active'

define "Has Active Diabetes":
  exists "Active Diabetes"

define "Type 1 Diabetes":
  [Condition] C where C.code.coding.code contains 'E10'

define "Type 2 Diabetes":
  [Condition] C where C.code.coding.code contains 'E11'

define "Has Type 1": exists "Type 1 Diabetes"
define "Has Type 2": exists "Type 2 Diabetes"

define "Diabetes Onset Date":
  Min("All Diabetes Conditions" C return C.onset)

define "Years With Diabetes":
  years between "Diabetes Onset Date" and Today()
