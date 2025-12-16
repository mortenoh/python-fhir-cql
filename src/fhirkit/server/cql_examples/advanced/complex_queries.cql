library ComplexQueries version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

// Multi-source queries
define "Patient Summary":
  {
    name: Patient.name.first().given.first() + ' ' + Patient.name.first().family,
    age: AgeInYears(),
    gender: Patient.gender,
    conditionCount: Count([Condition] C where C.clinicalStatus.coding.code contains 'active'),
    medicationCount: Count([MedicationRequest] M where M.status = 'active'),
    lastEncounter: Last([Encounter] E sort by period.start).period.start
  }

// Grouping
define "Observations By Category":
  from [Observation] O
    let cat: O.category.coding.first().code
    return {
      category: cat,
      count: Count([Observation] O2 where O2.category.coding.first().code = cat)
    }

// Complex filtering with multiple conditions
define "High Risk Patients Criteria":
  AgeInYears() >= 65
    and Count([Condition] C where C.clinicalStatus.coding.code contains 'active') >= 3
    and Count([MedicationRequest] M where M.status = 'active') >= 5

// Nested queries
define "Encounters With Diagnoses":
  [Encounter] E
    return {
      encounterId: E.id,
      date: E.period.start,
      type: E.type.coding.first().display,
      diagnoses: [Condition] C
        where C.encounter.reference contains E.id
        return C.code.coding.first().display
    }

// Temporal patterns
define "Readmissions Within 30 Days":
  from [Encounter] E1, [Encounter] E2
    where E1 != E2
    and E2.period.start after E1.period.end
    and days between E1.period.end and E2.period.start <= 30
    return {
      firstAdmit: E1.period.start,
      readmit: E2.period.start,
      daysBetween: days between E1.period.end and E2.period.start
    }
