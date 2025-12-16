library OpioidCheck version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

// Common opioid medication codes/names
define "Opioid Medications":
  [MedicationRequest] M
    where M.status = 'active'
      and (
        M.medication.coding.display contains 'oxycodone'
        or M.medication.coding.display contains 'hydrocodone'
        or M.medication.coding.display contains 'morphine'
        or M.medication.coding.display contains 'fentanyl'
        or M.medication.coding.display contains 'tramadol'
        or M.medication.coding.display contains 'codeine'
        or M.medication.coding.display contains 'methadone'
        or M.medication.coding.display contains 'opioid'
      )

define "On Opioids":
  exists "Opioid Medications"

define "Opioid Count":
  Count("Opioid Medications")

define "On Multiple Opioids":
  "Opioid Count" > 1

define "Benzodiazepines":
  [MedicationRequest] M
    where M.status = 'active'
      and (
        M.medication.coding.display contains 'diazepam'
        or M.medication.coding.display contains 'lorazepam'
        or M.medication.coding.display contains 'alprazolam'
        or M.medication.coding.display contains 'clonazepam'
        or M.medication.coding.display contains 'benzodiazepine'
      )

define "On Benzodiazepines":
  exists "Benzodiazepines"

define "Opioid Benzo Overlap":
  "On Opioids" and "On Benzodiazepines"

define "High Risk Combination":
  "Opioid Benzo Overlap"
