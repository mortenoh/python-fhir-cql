library PatientContacts version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Telecom": Patient.telecom

define "Phone Numbers":
  Patient.telecom T where T.system = 'phone' return T.value

define "Mobile Phone":
  Patient.telecom T
    where T.system = 'phone' and T.use = 'mobile'
    return T.value

define "Home Phone":
  Patient.telecom T
    where T.system = 'phone' and T.use = 'home'
    return T.value

define "Work Phone":
  Patient.telecom T
    where T.system = 'phone' and T.use = 'work'
    return T.value

define "Email Addresses":
  Patient.telecom T where T.system = 'email' return T.value

define "Primary Email":
  First(Patient.telecom T where T.system = 'email' and T.use = 'home').value

define "Has Phone": exists (Patient.telecom T where T.system = 'phone')
define "Has Email": exists (Patient.telecom T where T.system = 'email')

define "Emergency Contacts": Patient.contact
define "Emergency Contact Name": Patient.contact.first().name.text
define "Emergency Contact Phone":
  (Patient.contact.first().telecom) T where T.system = 'phone' return T.value
