/*
 * CQL Example 19: Encounter Queries and Visit Patterns
 *
 * Demonstrates:
 * - Querying Encounter resources
 * - Visit frequency analysis
 * - Encounter type filtering
 * - Time-based encounter patterns
 */

library EncounterQueries version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "ActCode": 'http://terminology.hl7.org/CodeSystem/v3-ActCode'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "EncounterStatus": 'http://hl7.org/fhir/encounter-status'

// Encounter class codes
code "Ambulatory": 'AMB' from "ActCode"
code "Emergency": 'EMER' from "ActCode"
code "Inpatient": 'IMP' from "ActCode"
code "Virtual": 'VR' from "ActCode"

// Status codes
code "Finished": 'finished' from "EncounterStatus"
code "InProgress": 'in-progress' from "EncounterStatus"

context Patient

// =====================================================
// Basic Encounter Queries
// =====================================================

// All encounters for the patient
define AllEncounters:
  [Encounter]

// Completed encounters
define CompletedEncounters:
  [Encounter] E
    where E.status = 'finished'

// In-progress encounters (currently admitted/visiting)
define ActiveEncounters:
  [Encounter] E
    where E.status = 'in-progress'

// =====================================================
// Encounter Type Filtering
// =====================================================

// Ambulatory (outpatient) visits
define OutpatientVisits:
  CompletedEncounters E
    where E.class.code = 'AMB'

// Emergency department visits
define EmergencyVisits:
  CompletedEncounters E
    where E.class.code = 'EMER'

// Inpatient admissions
define InpatientAdmissions:
  CompletedEncounters E
    where E.class.code = 'IMP'

// Telehealth/Virtual visits
define VirtualVisits:
  CompletedEncounters E
    where E.class.code = 'VR'

// =====================================================
// Time-Based Queries
// =====================================================

// Encounters in the last year
define EncountersLastYear:
  CompletedEncounters E
    where E.period.start >= Today() - 1 year

// Encounters in the last 30 days
define EncountersLast30Days:
  CompletedEncounters E
    where E.period.start >= Today() - 30 days

// Encounters in a specific date range
define function EncountersInPeriod(startDate Date, endDate Date):
  CompletedEncounters E
    where E.period.start >= startDate
      and E.period.start <= endDate

// =====================================================
// Visit Frequency Analysis
// =====================================================

// Total encounter count
define TotalEncounterCount:
  Count(AllEncounters)

// Encounters per year (last 12 months)
define EncountersPerYear:
  Count(EncountersLastYear)

// ED utilization count (last year)
define EDVisitsLastYear:
  Count(
    EmergencyVisits E
      where E.period.start >= Today() - 1 year
  )

// High ED utilizer (4+ ED visits per year)
define IsHighEDUtilizer:
  EDVisitsLastYear >= 4

// Frequent flyer (12+ visits per year of any type)
define IsFrequentVisitor:
  EncountersPerYear >= 12

// =====================================================
// Visit Duration Analysis
// =====================================================

// Calculate visit duration in minutes
define function VisitDurationMinutes(E Encounter):
  if E.length is not null then
    E.length.value
  else if E.period.start is not null and E.period.end is not null then
    minutes between E.period.start and E.period.end
  else
    null

// Average visit duration (from encounters with length)
define AverageVisitDuration:
  Avg(
    CompletedEncounters E
      where E.length is not null
      return E.length.value
  )

// Long visits (over 60 minutes)
define LongVisits:
  CompletedEncounters E
    where E.length.value > 60

// =====================================================
// Encounter Reason Analysis
// =====================================================

// Encounters for diabetes management
define DiabetesEncounters:
  CompletedEncounters E
    where exists (
      E.reasonCode R
        where R.coding.code contains '73211009'  // SNOMED for Diabetes mellitus
    )

// Encounters for hypertension
define HypertensionEncounters:
  CompletedEncounters E
    where exists (
      E.reasonCode R
        where R.coding.code contains '38341003'  // SNOMED for Hypertension
    )

// Get all encounter reasons
define AllEncounterReasons:
  flatten (
    CompletedEncounters E
      return all E.reasonCode
  )

// =====================================================
// Hospitalization Patterns
// =====================================================

// Count of inpatient admissions
define InpatientAdmissionCount:
  Count(InpatientAdmissions)

// Any recent hospitalization (last 30 days)
define RecentlyHospitalized:
  exists (
    InpatientAdmissions E
      where E.period.end >= Today() - 30 days
  )

// Readmission within 30 days
define HasThirtyDayReadmission:
  exists (
    InpatientAdmissions A,
    InpatientAdmissions B
      where A != B
        and B.period.start >= A.period.end
        and days between A.period.end and B.period.start <= 30
  )

// =====================================================
// Most Recent Encounter
// =====================================================

// Most recent encounter date
define MostRecentEncounterDate:
  Max(CompletedEncounters E return E.period.start)

// Most recent encounter
define MostRecentEncounter:
  Last(
    CompletedEncounters E
      sort by period.start
  )

// Days since last visit
define DaysSinceLastVisit:
  days between MostRecentEncounterDate and Today()

// Overdue for visit (no visit in 6+ months)
define IsOverdueForVisit:
  DaysSinceLastVisit > 180

// =====================================================
// Care Gaps Based on Encounters
// =====================================================

// No primary care visit in last year
define NoPrimaryCareVisitLastYear:
  not exists (
    OutpatientVisits E
      where E.period.start >= Today() - 1 year
        and exists (
          E.type T
            where T.coding.code contains '185349003'  // Encounter for check up
        )
  )

// Annual wellness visit completed
define AnnualWellnessVisitCompleted:
  exists (
    OutpatientVisits E
      where E.period.start >= Today() - 1 year
        and exists (
          E.type T
            where T.coding.display contains 'wellness'
               or T.coding.display contains 'check up'
        )
  )

// =====================================================
// Summary Statistics
// =====================================================

define EncounterSummary:
  Tuple {
    totalEncounters: TotalEncounterCount,
    outpatientVisits: Count(OutpatientVisits),
    edVisits: Count(EmergencyVisits),
    inpatientAdmissions: InpatientAdmissionCount,
    virtualVisits: Count(VirtualVisits),
    lastVisitDate: MostRecentEncounterDate,
    daysSinceLastVisit: DaysSinceLastVisit
  }
