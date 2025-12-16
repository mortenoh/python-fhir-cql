library TimingRelationships version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

// Basic Timing
define "Encounters":
  [Encounter] E where E.status = 'finished'

define "Conditions":
  [Condition] C where C.clinicalStatus.coding.code contains 'active'

define "Medications":
  [MedicationRequest] M where M.status = 'active'

// Conditions diagnosed during encounter
define "Encounter Diagnoses":
  from "Encounters" E, "Conditions" C
    where C.onset during E.period
    return {
      encounter: E.id,
      condition: C.code.coding.first().display,
      date: C.onset
    }

// Medications started after diagnosis
define "Post Diagnosis Medications":
  from "Conditions" C, "Medications" M
    where M.authoredOn after C.onset
    return {
      condition: C.code.coding.first().display,
      medication: M.medication.coding.first().display,
      daysBetween: days between C.onset and M.authoredOn
    }

// Time-based filtering
define "Last 30 Days":
  Interval[Today() - 30 days, Today()]

define "Last Year":
  Interval[Today() - 1 year, Today()]

define "Recent Encounters":
  "Encounters" E where E.period starts during "Last 30 Days"

// Overlapping conditions
define "Concurrent Conditions":
  from "Conditions" C1, "Conditions" C2
    where C1 != C2
    and (C1.onset same day as C2.onset
      or days between C1.onset and C2.onset < 30)
    return {
      condition1: C1.code.coding.first().display,
      condition2: C2.code.coding.first().display
    }
