library VitalSigns version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

codesystem "LOINC": 'http://loinc.org'

code "Heart Rate": '8867-4' from "LOINC"
code "Respiratory Rate": '9279-1' from "LOINC"
code "Body Temperature": '8310-5' from "LOINC"
code "Blood Pressure Panel": '85354-9' from "LOINC"
code "Systolic BP Component": '8480-6' from "LOINC"
code "Diastolic BP Component": '8462-4' from "LOINC"
code "Oxygen Saturation": '2708-6' from "LOINC"
code "Body Weight": '29463-7' from "LOINC"
code "Body Height": '8302-2' from "LOINC"
code "BMI": '39156-5' from "LOINC"

context Patient

define "All Vital Signs":
  [Observation: category in "vital-signs"]

define "Heart Rate Observations":
  [Observation: "Heart Rate"]

define "Latest Heart Rate":
  Last([Observation: "Heart Rate"] O sort by effective)

define "Latest Heart Rate Value":
  ("Latest Heart Rate").value as Quantity

define "Blood Pressure Observations":
  [Observation: "Blood Pressure Panel"]

define "Latest BP Observation":
  Last([Observation: "Blood Pressure Panel"] O sort by effective)

define "Latest Systolic BP":
  (singleton from (
    ("Latest BP Observation".component) C
    where C.code ~ "Systolic BP Component"
  )).valueQuantity

define "Latest Diastolic BP":
  (singleton from (
    ("Latest BP Observation".component) C
    where C.code ~ "Diastolic BP Component"
  )).valueQuantity

define "Latest Temperature":
  (Last([Observation: "Body Temperature"] O sort by effective)).value as Quantity

define "Latest Weight":
  (Last([Observation: "Body Weight"] O sort by effective)).value as Quantity

define "Latest Height":
  (Last([Observation: "Body Height"] O sort by effective)).value as Quantity

define "Latest BMI":
  (Last([Observation: "BMI"] O sort by effective)).value as Quantity
