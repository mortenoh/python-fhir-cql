library Contraindications version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

// Renal Impairment
define "Has CKD":
  exists ([Condition] C
    where C.code.coding.code contains 'N18'
    and C.clinicalStatus.coding.code contains 'active')

define "Severe Renal Impairment":
  exists ([Observation] O
    where O.code.coding.code = '33914-3'  // eGFR
    and (O.value as Quantity).value < 30)

// Liver Impairment
define "Has Liver Disease":
  exists ([Condition] C
    where (C.code.coding.code contains 'K70'
      or C.code.coding.code contains 'K74')
    and C.clinicalStatus.coding.code contains 'active')

// Pregnancy
define "Is Pregnant":
  Patient.gender = 'female'
    and exists ([Condition] C
      where C.code.coding.display contains 'pregnancy'
      and C.clinicalStatus.coding.code contains 'active')

// Bleeding Risk
define "On Anticoagulant":
  exists ([MedicationRequest] M
    where M.status = 'active'
    and (M.medication.coding.display contains 'warfarin'
      or M.medication.coding.display contains 'apixaban'))

define "Has Bleeding History":
  exists ([Condition] C
    where C.code.coding.display contains 'bleed')

// Drug Contraindications
define "Metformin Contraindicated":
  "Severe Renal Impairment"

define "Statin Contraindicated":
  "Has Liver Disease" or "Is Pregnant"

define "NSAID Contraindicated":
  "Has CKD" or "On Anticoagulant"

define "Contraindication Summary": {
  metformin: "Metformin Contraindicated",
  statin: "Statin Contraindicated",
  nsaid: "NSAID Contraindicated"
}
