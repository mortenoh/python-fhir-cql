/*
 * CQL Example 22: Care Coordination and Care Plans
 *
 * Demonstrates:
 * - Querying CarePlan resources
 * - Care team member analysis
 * - Goal tracking and progress
 * - Care gap identification
 * - Transitions of care
 */

library CareCoordination version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "CarePlanStatus": 'http://hl7.org/fhir/request-status'
codesystem "GoalStatus": 'http://hl7.org/fhir/goal-status'
codesystem "CarePlanCategory": 'http://hl7.org/fhir/us/core/CodeSystem/careplan-category'

context Patient

// =====================================================
// Care Plan Queries
// =====================================================

// All care plans for the patient
define AllCarePlans:
  [CarePlan]

// Active care plans
define ActiveCarePlans:
  [CarePlan] CP
    where CP.status = 'active'

// Completed care plans
define CompletedCarePlans:
  [CarePlan] CP
    where CP.status = 'completed'

// Revoked or cancelled care plans
define InactiveCarePlans:
  [CarePlan] CP
    where CP.status in {'revoked', 'cancelled', 'entered-in-error'}

// =====================================================
// Care Plan Categories
// =====================================================

// Assessment and Plan care plans (US Core)
define AssessmentAndPlanCarePlans:
  ActiveCarePlans CP
    where exists (
      CP.category C
        where C.coding.code contains 'assess-plan'
    )

// Disease-specific care plans
define DiabetesCarePlans:
  ActiveCarePlans CP
    where exists (
      CP.addresses A
        where A.display contains 'Diabetes'
           or A.display contains 'diabetes'
    )

define HeartFailureCarePlans:
  ActiveCarePlans CP
    where exists (
      CP.addresses A
        where A.display contains 'Heart Failure'
           or A.display contains 'heart failure'
    )

// =====================================================
// Care Plan Activities
// =====================================================

// Get all activities from active care plans
define AllCarePlanActivities:
  flatten (
    ActiveCarePlans CP
      return all CP.activity
  )

// Scheduled activities
define ScheduledActivities:
  AllCarePlanActivities A
    where A.detail.status = 'scheduled'

// In-progress activities
define InProgressActivities:
  AllCarePlanActivities A
    where A.detail.status = 'in-progress'

// Completed activities
define CompletedActivities:
  AllCarePlanActivities A
    where A.detail.status = 'completed'

// Overdue activities (not completed, past scheduled date)
define NotStartedActivities:
  AllCarePlanActivities A
    where A.detail.status = 'not-started'

// Count of pending activities
define PendingActivityCount:
  Count(ScheduledActivities) + Count(NotStartedActivities)

// =====================================================
// Goals and Targets
// =====================================================

// All patient goals
define AllGoals:
  [Goal]

// Active goals
define ActiveGoals:
  [Goal] G
    where G.lifecycleStatus in {'active', 'on-hold'}

// Achieved goals
define AchievedGoals:
  [Goal] G
    where G.lifecycleStatus = 'achieved'

// Goals by achievement status
define GoalsOnTrack:
  ActiveGoals G
    where G.achievementStatus.coding.code contains 'on-track'
       or G.achievementStatus.coding.code contains 'ahead-of-target'

define GoalsBehind:
  ActiveGoals G
    where G.achievementStatus.coding.code contains 'behind-target'
       or G.achievementStatus.coding.code contains 'not-attainable'

// HbA1c specific goal
define HbA1cGoal:
  First(
    ActiveGoals G
      where G.description.text contains 'HbA1c'
         or G.description.text contains 'A1C'
  )

// Weight management goal
define WeightGoal:
  First(
    ActiveGoals G
      where G.description.text contains 'weight'
         or G.description.text contains 'Weight'
  )

// Blood pressure goal
define BloodPressureGoal:
  First(
    ActiveGoals G
      where G.description.text contains 'blood pressure'
         or G.description.text contains 'Blood Pressure'
         or G.description.text contains 'BP'
  )

// =====================================================
// Care Team Analysis
// =====================================================

// All care teams
define AllCareTeams:
  [CareTeam]

// Active care teams
define ActiveCareTeams:
  [CareTeam] CT
    where CT.status = 'active'

// Get care team members
define CareTeamMembers:
  flatten (
    ActiveCareTeams CT
      return all CT.participant
  )

// Primary care provider
define PrimaryCareProvider:
  First(
    CareTeamMembers P
      where exists (
        P.role R
          where R.coding.code contains '446050000'  // Primary care physician
             or R.coding.display contains 'primary care'
      )
  )

// Specialists on care team
define Specialists:
  CareTeamMembers P
    where exists (
      P.role R
        where R.coding.display contains 'specialist'
           or R.coding.display contains 'Specialist'
    )

// Count of care team members
define CareTeamMemberCount:
  Count(CareTeamMembers)

// Has assigned care manager
define HasCareManager:
  exists (
    CareTeamMembers P
      where exists (
        P.role R
          where R.coding.display contains 'care manager'
             or R.coding.display contains 'Care Manager'
             or R.coding.code contains '768820003'
        )
  )

// =====================================================
// Referrals and Service Requests
// =====================================================

// Active referrals
define ActiveReferrals:
  [ServiceRequest] SR
    where SR.status = 'active'
      and SR.intent = 'order'

// Pending specialist referrals
define PendingSpecialistReferrals:
  ActiveReferrals SR
    where SR.category.coding.code contains '103696004'  // Patient referral

// Completed referrals
define CompletedReferrals:
  [ServiceRequest] SR
    where SR.status = 'completed'
      and SR.intent = 'order'

// Outstanding referrals (not completed within 30 days)
define OutstandingReferrals:
  ActiveReferrals SR
    where SR.authoredOn < Today() - 30 days

// =====================================================
// Transitions of Care
// =====================================================

// Recent discharges (last 30 days)
define RecentDischarges:
  [Encounter] E
    where E.class.code = 'IMP'
      and E.status = 'finished'
      and E.period.end >= Today() - 30 days

// Has recent hospital discharge
define HasRecentDischarge:
  exists RecentDischarges

// Discharge without follow-up appointment
define DischargeWithoutFollowUp:
  exists RecentDischarges
    and not exists (
      [Appointment] A
        where A.status in {'booked', 'pending'}
          and A.start >= Today()
    )

// Post-discharge medication reconciliation needed
define NeedsMedicationReconciliation:
  HasRecentDischarge
    and not exists (
      [Procedure] P
        where P.code.coding.code contains '430193006'  // Medication reconciliation
          and P.performed as dateTime >= Today() - 7 days
    )

// =====================================================
// Care Gaps
// =====================================================

// No active care plan
define NeedsCarePlan:
  not exists ActiveCarePlans

// Care plan without recent review
define CarePlanNeedsReview:
  exists (
    ActiveCarePlans CP
      where CP.period.start < Today() - 6 months
  )
    and not exists (
      ActiveCarePlans CP
        where CP.created >= Today() - 6 months
    )

// Has goals without care plan activities
define GoalsWithoutActivities:
  exists ActiveGoals
    and not exists InProgressActivities

// No care team assigned
define NeedsCareTeam:
  not exists ActiveCareTeams

// =====================================================
// Communication and Follow-up
// =====================================================

// Recent communications about patient
define RecentCommunications:
  [Communication] C
    where C.sent >= Today() - 30 days
      and C.status = 'completed'

// Scheduled appointments
define UpcomingAppointments:
  [Appointment] A
    where A.status in {'booked', 'pending'}
      and A.start >= Today()

// Next appointment date
define NextAppointmentDate:
  Min(
    UpcomingAppointments A
      return A.start as dateTime
  )

// Days until next appointment
define DaysToNextAppointment:
  if NextAppointmentDate is not null then
    days between Today() and NextAppointmentDate
  else
    null

// No upcoming appointments
define NeedsAppointment:
  not exists UpcomingAppointments

// =====================================================
// Care Coordination Metrics
// =====================================================

define CareCoordinationMetrics:
  Tuple {
    activeCarePlans: Count(ActiveCarePlans),
    pendingActivities: PendingActivityCount,
    activeGoals: Count(ActiveGoals),
    goalsOnTrack: Count(GoalsOnTrack),
    goalsBehind: Count(GoalsBehind),
    careTeamMembers: CareTeamMemberCount,
    hasCareManager: HasCareManager,
    pendingReferrals: Count(ActiveReferrals),
    daysToNextAppointment: DaysToNextAppointment
  }

// =====================================================
// Care Coordination Summary
// =====================================================

define CareCoordinationSummary:
  Tuple {
    hasActiveCarePlan: exists ActiveCarePlans,
    carePlanNeedsReview: CarePlanNeedsReview,
    hasActiveGoals: exists ActiveGoals,
    hasCareTeam: exists ActiveCareTeams,
    hasRecentDischarge: HasRecentDischarge,
    needsFollowUp: DischargeWithoutFollowUp,
    needsMedReconciliation: NeedsMedicationReconciliation,
    nextAppointment: NextAppointmentDate
  }

// =====================================================
// Care Coordination Alerts
// =====================================================

define CareCoordinationAlerts:
  List<String> {
    if NeedsCarePlan then 'Patient needs an active care plan' else null,
    if CarePlanNeedsReview then 'Care plan needs review (>6 months old)' else null,
    if NeedsCareTeam then 'Patient needs assigned care team' else null,
    if DischargeWithoutFollowUp then 'Recent discharge without follow-up scheduled' else null,
    if NeedsMedicationReconciliation then 'Post-discharge medication reconciliation needed' else null,
    if Count(GoalsBehind) > 0 then 'Goals behind target - review needed' else null,
    if Count(OutstandingReferrals) > 0 then 'Outstanding referrals >30 days' else null,
    if NeedsAppointment then 'No upcoming appointments scheduled' else null
  }

define ActiveAlerts:
  CareCoordinationAlerts A where A is not null
