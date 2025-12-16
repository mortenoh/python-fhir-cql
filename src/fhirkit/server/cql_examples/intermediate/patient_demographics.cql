library PatientDemographics version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "Patient ID": Patient.id
define "Patient Name":
  Patient.name.first().given.first() + ' ' + Patient.name.first().family

define "Given Names": Patient.name.first().given
define "Family Name": Patient.name.first().family
define "Full Name": Patient.name.first().text

define "Gender": Patient.gender
define "Birth Date": Patient.birthDate
define "Is Male": Patient.gender = 'male'
define "Is Female": Patient.gender = 'female'

define "MRN":
  (Patient.identifier I where I.type.coding.code contains 'MR').value

define "SSN":
  (Patient.identifier I where I.system = 'http://hl7.org/fhir/sid/us-ssn').value

define "Address": Patient.address.first()
define "City": Patient.address.first().city
define "State": Patient.address.first().state
define "Zip": Patient.address.first().postalCode

define "Phone":
  (Patient.telecom T where T.system = 'phone').value
define "Email":
  (Patient.telecom T where T.system = 'email').value

define "Marital Status": Patient.maritalStatus.coding.first().display
define "Is Deceased": Patient.deceased is not null
