library CareReminders version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

codesystem "LOINC": 'http://loinc.org'
code "HbA1c": '4548-4' from "LOINC"
code "LDL": '13457-7' from "LOINC"

context Patient

// Diabetes Care Reminders
define "Has Diabetes":
  exists ([Condition] C
    where (C.code.coding.code contains 'E10' or C.code.coding.code contains 'E11')
    and C.clinicalStatus.coding.code contains 'active')

define "Last HbA1c Date":
  (Last([Observation: "HbA1c"] O sort by effective)).effective

define "HbA1c Due":
  "Has Diabetes" and (
    "Last HbA1c Date" is null
    or "Last HbA1c Date" before Today() - 3 months
  )

// Cholesterol Screening
define "Last LDL Date":
  (Last([Observation: "LDL"] O sort by effective)).effective

define "LDL Due":
  "Last LDL Date" is null
    or "Last LDL Date" before Today() - 1 year

// Cancer Screening (age-based)
define "Mammogram Due":
  Patient.gender = 'female'
    and AgeInYears() >= 50
    and not exists ([DiagnosticReport] D
      where D.code.coding.display contains 'mammogram'
      and D.effective after Today() - 2 years)

define "Colonoscopy Due":
  AgeInYears() >= 50
    and not exists ([Procedure] P
      where P.code.coding.display contains 'colonoscopy'
      and P.performed after Today() - 10 years)

// Immunization Reminders
define "Flu Shot Due":
  not exists ([Immunization] I
    where I.vaccineCode.coding.display contains 'influenza'
    and I.occurrence after Today() - 1 year)

// Summary
define "Care Gaps":
  (if "HbA1c Due" then { 'HbA1c Test Due' } else { })
    union (if "LDL Due" then { 'Lipid Panel Due' } else { })
    union (if "Mammogram Due" then { 'Mammogram Due' } else { })
    union (if "Colonoscopy Due" then { 'Colonoscopy Due' } else { })
    union (if "Flu Shot Due" then { 'Flu Vaccine Due' } else { })
