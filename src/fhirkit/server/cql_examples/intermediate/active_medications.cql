library ActiveMedications version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Medication Requests":
  [MedicationRequest]

define "Active Medications":
  [MedicationRequest] M
    where M.status = 'active'

define "Active Medication Count":
  Count("Active Medications")

define "Medication Names":
  "Active Medications" M
    return Coalesce(
      M.medication.coding.first().display,
      M.medication.text
    )

define "Medications With Dosage":
  "Active Medications" M
    return {
      name: M.medication.coding.first().display,
      dosage: M.dosageInstruction.first().text,
      frequency: M.dosageInstruction.first().timing.repeat.frequency
    }

define "On Polypharmacy":
  "Active Medication Count" >= 5

define "Stopped Medications":
  [MedicationRequest] M where M.status = 'stopped'

define "Recently Started":
  "Active Medications" M
    where M.authoredOn in Interval[Today() - 30 days, Today()]

define "Long Term Medications":
  "Active Medications" M
    where M.authoredOn before Today() - 1 year
