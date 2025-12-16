library DrugClassCheck version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "Active Medications":
  [MedicationRequest] M where M.status = 'active'

define "Antihypertensives":
  "Active Medications" M
    where M.medication.coding.display contains 'lisinopril'
      or M.medication.coding.display contains 'amlodipine'
      or M.medication.coding.display contains 'metoprolol'
      or M.medication.coding.display contains 'losartan'
      or M.medication.coding.display contains 'hydrochlorothiazide'

define "Statins":
  "Active Medications" M
    where M.medication.coding.display contains 'atorvastatin'
      or M.medication.coding.display contains 'simvastatin'
      or M.medication.coding.display contains 'rosuvastatin'
      or M.medication.coding.display contains 'pravastatin'

define "Anticoagulants":
  "Active Medications" M
    where M.medication.coding.display contains 'warfarin'
      or M.medication.coding.display contains 'apixaban'
      or M.medication.coding.display contains 'rivaroxaban'
      or M.medication.coding.display contains 'dabigatran'

define "Antiplatelets":
  "Active Medications" M
    where M.medication.coding.display contains 'aspirin'
      or M.medication.coding.display contains 'clopidogrel'
      or M.medication.coding.display contains 'ticagrelor'

define "NSAIDs":
  "Active Medications" M
    where M.medication.coding.display contains 'ibuprofen'
      or M.medication.coding.display contains 'naproxen'
      or M.medication.coding.display contains 'diclofenac'

define "On Anticoagulant": exists "Anticoagulants"
define "On NSAID": exists "NSAIDs"
define "Bleeding Risk": "On Anticoagulant" and "On NSAID"

define "On Statin": exists "Statins"
define "Statin Needed": not "On Statin"
