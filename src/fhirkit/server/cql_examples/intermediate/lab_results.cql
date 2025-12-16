library LabResults version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

codesystem "LOINC": 'http://loinc.org'

code "Hemoglobin A1c": '4548-4' from "LOINC"
code "LDL Cholesterol": '13457-7' from "LOINC"
code "HDL Cholesterol": '2085-9' from "LOINC"
code "Total Cholesterol": '2093-3' from "LOINC"
code "Triglycerides": '2571-8' from "LOINC"
code "Creatinine": '2160-0' from "LOINC"
code "eGFR": '33914-3' from "LOINC"
code "Glucose": '2345-7' from "LOINC"
code "Potassium": '2823-3' from "LOINC"
code "Sodium": '2951-2' from "LOINC"
code "WBC": '6690-2' from "LOINC"
code "Hemoglobin": '718-7' from "LOINC"
code "Platelets": '777-3' from "LOINC"

context Patient

define "All Lab Results":
  [Observation: category in "laboratory"]

define "HbA1c Results":
  [Observation: "Hemoglobin A1c"]

define "Latest HbA1c":
  Last([Observation: "Hemoglobin A1c"] O sort by effective)

define "Latest HbA1c Value":
  ("Latest HbA1c").value as Quantity

define "HbA1c In Control":
  ("Latest HbA1c Value").value < 7.0

define "Cholesterol Panel":
  [Observation: "Total Cholesterol"]
    union [Observation: "LDL Cholesterol"]
    union [Observation: "HDL Cholesterol"]
    union [Observation: "Triglycerides"]

define "Latest LDL":
  (Last([Observation: "LDL Cholesterol"] O sort by effective)).value as Quantity

define "LDL At Goal":
  ("Latest LDL").value < 100

define "Latest eGFR":
  (Last([Observation: "eGFR"] O sort by effective)).value as Quantity

define "Has CKD Stage 3+":
  ("Latest eGFR").value < 60
