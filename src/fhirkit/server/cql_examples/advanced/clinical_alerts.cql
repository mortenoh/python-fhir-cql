library ClinicalAlerts version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

codesystem "LOINC": 'http://loinc.org'
code "Potassium": '2823-3' from "LOINC"
code "Creatinine": '2160-0' from "LOINC"
code "eGFR": '33914-3' from "LOINC"

context Patient

// Critical Lab Value Alerts
define "Latest Potassium":
  Last([Observation: "Potassium"] O sort by effective)

define "Critical Potassium":
  ("Latest Potassium").value as Quantity

define "Potassium Alert":
  ("Critical Potassium").value < 3.0 or ("Critical Potassium").value > 6.0

// Kidney Function Alerts
define "Latest eGFR":
  (Last([Observation: "eGFR"] O sort by effective)).value as Quantity

define "Severe CKD Alert":
  ("Latest eGFR").value < 30

define "Moderate CKD Alert":
  ("Latest eGFR").value < 60 and ("Latest eGFR").value >= 30

// Drug-Disease Interactions
define "On NSAIDs":
  exists ([MedicationRequest] M
    where M.status = 'active'
    and (M.medication.coding.display contains 'ibuprofen'
      or M.medication.coding.display contains 'naproxen'))

define "CKD With NSAID Alert":
  "Moderate CKD Alert" and "On NSAIDs"

// Allergy Alerts
define "Has Penicillin Allergy":
  exists ([AllergyIntolerance] A
    where A.code.coding.display contains 'penicillin')

// Summary
define "Active Alerts":
  (if "Potassium Alert" then { 'Critical Potassium' } else { })
    union (if "Severe CKD Alert" then { 'Severe CKD' } else { })
    union (if "CKD With NSAID Alert" then { 'NSAID with CKD' } else { })
