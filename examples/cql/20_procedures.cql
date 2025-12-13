/*
 * CQL Example 20: Procedure History and Surgical Queries
 *
 * Demonstrates:
 * - Querying Procedure resources
 * - Surgical history analysis
 * - Complication tracking
 * - Preventive procedure status
 */

library ProcedureQueries version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "CPT": 'http://www.ama-assn.org/go/cpt'
codesystem "ProcedureStatus": 'http://hl7.org/fhir/event-status'

// Status codes
code "Completed": 'completed' from "ProcedureStatus"

// Common procedure codes (SNOMED)
code "Colonoscopy": '73761001' from "SNOMED"
code "Mammogram": '71651007' from "SNOMED"
code "Appendectomy": '80146002' from "SNOMED"
code "Cholecystectomy": '38102005' from "SNOMED"
code "Cesarean Section": '11466000' from "SNOMED"
code "Cardiac Catheterization": '41976001' from "SNOMED"
code "Knee Replacement": '179344006' from "SNOMED"
code "Hip Replacement": '52734007' from "SNOMED"

context Patient

// =====================================================
// Basic Procedure Queries
// =====================================================

// All procedures
define AllProcedures:
  [Procedure]

// Completed procedures only
define CompletedProcedures:
  [Procedure] P
    where P.status = 'completed'

// In-progress procedures
define OngoingProcedures:
  [Procedure] P
    where P.status = 'in-progress'

// =====================================================
// Procedure Category Filtering
// =====================================================

// Surgical procedures
define SurgicalProcedures:
  CompletedProcedures P
    where exists (
      P.category C
        where C.coding.code contains '387713003'  // SNOMED: Surgical procedure
    )

// Diagnostic procedures
define DiagnosticProcedures:
  CompletedProcedures P
    where exists (
      P.category C
        where C.coding.code contains '103693007'  // SNOMED: Diagnostic procedure
    )

// Therapeutic procedures
define TherapeuticProcedures:
  CompletedProcedures P
    where exists (
      P.category C
        where C.coding.code contains '277132007'  // SNOMED: Therapeutic procedure
    )

// =====================================================
// Time-Based Queries
// =====================================================

// Procedures in the last year
define ProceduresLastYear:
  CompletedProcedures P
    where P.performed as dateTime >= Today() - 1 year
       or (P.performed as Period).start >= Today() - 1 year

// Procedures in the last 5 years
define ProceduresLast5Years:
  CompletedProcedures P
    where P.performed as dateTime >= Today() - 5 years
       or (P.performed as Period).start >= Today() - 5 years

// =====================================================
// Preventive Care Procedures
// =====================================================

// Colonoscopy screening
define ColonoscopyProcedures:
  CompletedProcedures P
    where P.code.coding.code contains '73761001'  // SNOMED: Colonoscopy
       or P.code.coding.code contains '45378'     // CPT: Colonoscopy

// Most recent colonoscopy
define MostRecentColonoscopy:
  Last(
    ColonoscopyProcedures P
      sort by (performed as dateTime)
  )

// Colonoscopy due (none in last 10 years, age 45+)
define ColonoscopyDue:
  not exists (
    ColonoscopyProcedures P
      where P.performed as dateTime >= Today() - 10 years
  )

// Mammogram procedures
define MammogramProcedures:
  CompletedProcedures P
    where P.code.coding.code contains '71651007'  // SNOMED: Mammography
       or P.code.coding.code contains '77067'     // CPT: Bilateral mammogram

// Mammogram due (for women, none in last 2 years)
define MammogramDue:
  not exists (
    MammogramProcedures P
      where P.performed as dateTime >= Today() - 2 years
  )

// =====================================================
// Surgical History
// =====================================================

// Has had appendectomy
define HasHadAppendectomy:
  exists (
    CompletedProcedures P
      where P.code.coding.code contains '80146002'
  )

// Has had cholecystectomy (gallbladder removal)
define HasHadCholecystectomy:
  exists (
    CompletedProcedures P
      where P.code.coding.code contains '38102005'
  )

// Has had C-section
define HasHadCesareanSection:
  exists (
    CompletedProcedures P
      where P.code.coding.code contains '11466000'
  )

// Joint replacement history
define HasJointReplacement:
  exists (
    CompletedProcedures P
      where P.code.coding.code contains '179344006'  // Knee
         or P.code.coding.code contains '52734007'   // Hip
  )

// Cardiac procedure history
define HasCardiacProcedureHistory:
  exists (
    CompletedProcedures P
      where P.code.coding.code contains '41976001'   // Cardiac cath
         or P.code.coding.code contains '232717009'  // CABG
         or P.code.coding.code contains '175898006'  // Stent
  )

// =====================================================
// Procedure Outcomes
// =====================================================

// Successful procedures
define SuccessfulProcedures:
  CompletedProcedures P
    where P.outcome.coding.code contains '385669000'  // Successful

// Procedures with complications
define ProceduresWithComplications:
  CompletedProcedures P
    where exists P.complication

// Get all complications
define AllComplications:
  flatten (
    CompletedProcedures P
      where exists P.complication
      return all P.complication
  )

// =====================================================
// Body Site Analysis
// =====================================================

// Procedures on the colon
define ColonProcedures:
  CompletedProcedures P
    where exists (
      P.bodySite B
        where B.coding.code contains '71854001'  // Colon structure
    )

// Cardiac procedures
define CardiacProcedures:
  CompletedProcedures P
    where exists (
      P.bodySite B
        where B.coding.code contains '80891009'  // Heart structure
    )

// =====================================================
// Follow-up Analysis
// =====================================================

// Procedures requiring follow-up
define ProceduresNeedingFollowUp:
  CompletedProcedures P
    where exists P.followUp

// Overdue follow-ups
define OverdueFollowUps:
  ProceduresNeedingFollowUp P
    where exists (
      P.followUp F
        where F.coding.display contains 'year'
        // Simplified: would need more complex logic for actual date calculation
    )

// =====================================================
// Statistics
// =====================================================

// Total procedure count
define TotalProcedureCount:
  Count(CompletedProcedures)

// Surgical procedure count
define SurgicalProcedureCount:
  Count(SurgicalProcedures)

// Procedures by year
define ProceduresThisYear:
  Count(
    CompletedProcedures P
      where year from (P.performed as dateTime) = year from Today()
  )

// Has extensive surgical history (5+ procedures)
define HasExtensiveSurgicalHistory:
  Count(SurgicalProcedures) >= 5

// =====================================================
// Procedure Summary
// =====================================================

define ProcedureSummary:
  Tuple {
    totalProcedures: TotalProcedureCount,
    surgicalCount: SurgicalProcedureCount,
    diagnosticCount: Count(DiagnosticProcedures),
    lastProcedureDate: Max(CompletedProcedures P return P.performed as dateTime),
    colonoscopyDue: ColonoscopyDue,
    mammogramDue: MammogramDue,
    hasComplications: exists ProceduresWithComplications
  }
