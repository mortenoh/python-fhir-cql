/*
 * CQL Example 26: International Patient Summary (IPS)
 *
 * Demonstrates:
 * - Querying all IPS section data
 * - IPS completeness validation
 * - Clinical summary generation
 * - Cross-border data exchange readiness
 *
 * Based on: http://hl7.org/fhir/uv/ips/
 */

library IPSSummary version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "LOINC": 'http://loinc.org'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "ObservationCategory": 'http://terminology.hl7.org/CodeSystem/observation-category'
codesystem "AllergyIntoleranceClinical": 'http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical'
codesystem "ConditionClinical": 'http://terminology.hl7.org/CodeSystem/condition-clinical'
codesystem "MedicationRequestStatus": 'http://hl7.org/fhir/CodeSystem/medicationrequest-status'

// IPS Section LOINC Codes
code "IPS Allergies Section": '48765-2' from "LOINC" display 'Allergies and adverse reactions Document'
code "IPS Medications Section": '10160-0' from "LOINC" display 'History of Medication use Narrative'
code "IPS Problems Section": '11450-4' from "LOINC" display 'Problem list - Reported'
code "IPS Immunizations Section": '11369-6' from "LOINC" display 'History of Immunization Narrative'
code "IPS Procedures Section": '47519-4' from "LOINC" display 'History of Procedures Document'
code "IPS Results Section": '30954-2' from "LOINC" display 'Relevant diagnostic tests/laboratory data Narrative'
code "IPS Vital Signs Section": '8716-3' from "LOINC" display 'Vital signs'

context Patient

// =====================================================
// IPS SECTION 1: ALLERGIES (Required)
// LOINC: 48765-2
// =====================================================

// All allergies for the patient
define AllAllergies:
  [AllergyIntolerance]

// Active allergies (required for IPS)
define IPSAllergies:
  [AllergyIntolerance] A
    where A.clinicalStatus.coding.code contains 'active'

// Medication allergies
define IPSMedicationAllergies:
  IPSAllergies A
    where A.category contains 'medication'

// High criticality allergies (important for safety)
define HighCriticalityAllergies:
  IPSAllergies A
    where A.criticality = 'high'

// Allergies with severe reactions
define SevereReactionAllergies:
  IPSAllergies A
    where exists (A.reaction R where R.severity = 'severe')

// Has any documented allergies
define HasDocumentedAllergies:
  exists IPSAllergies

// No known allergies flag
define NoKnownAllergies:
  not exists [AllergyIntolerance]

// =====================================================
// IPS SECTION 2: MEDICATIONS (Required)
// LOINC: 10160-0
// =====================================================

// All medication requests
define AllMedicationRequests:
  [MedicationRequest]

// Active medications (required for IPS)
define IPSMedications:
  [MedicationRequest] M
    where M.status = 'active'

// Chronic medications (long-term)
define ChronicMedications:
  IPSMedications M
    where M.dispenseRequest.numberOfRepeatsAllowed > 0
      or M.dispenseRequest.validityPeriod.end > Today() + 30 days

// Recent prescriptions (last 6 months)
define RecentPrescriptions:
  [MedicationRequest] M
    where M.authoredOn >= Today() - 6 months

// Medication count
define ActiveMedicationCount:
  Count(IPSMedications)

// Has current medications
define HasActiveMedications:
  exists IPSMedications

// =====================================================
// IPS SECTION 3: PROBLEMS/CONDITIONS (Required)
// LOINC: 11450-4
// =====================================================

// All conditions
define AllConditions:
  [Condition]

// Active problems (required for IPS)
define IPSProblems:
  [Condition] C
    where C.clinicalStatus.coding.code contains 'active'

// Chronic conditions
define ChronicConditions:
  IPSProblems C
    where C.onset as dateTime < Today() - 3 months

// Resolved conditions (optional for context)
define ResolvedConditions:
  [Condition] C
    where C.clinicalStatus.coding.code contains 'resolved'
      and C.abatement as dateTime >= Today() - 1 year

// Primary diagnoses
define PrimaryDiagnoses:
  IPSProblems C
    where exists (
      C.category Cat
        where Cat.coding.code contains 'encounter-diagnosis'
           or Cat.coding.code contains 'problem-list-item'
    )

// Has active problems
define HasActiveProblems:
  exists IPSProblems

// =====================================================
// IPS SECTION 4: IMMUNIZATIONS (Recommended)
// LOINC: 11369-6
// =====================================================

// All immunizations
define AllImmunizations:
  [Immunization]

// Completed immunizations (for IPS)
define IPSImmunizations:
  [Immunization] I
    where I.status = 'completed'

// Recent immunizations (last 5 years)
define RecentImmunizations:
  IPSImmunizations I
    where I.occurrence as dateTime >= Today() - 5 years

// COVID-19 vaccines
define CovidVaccinations:
  IPSImmunizations I
    where I.vaccineCode.coding.code contains '207'  // Moderna
       or I.vaccineCode.coding.code contains '208'  // Pfizer
       or I.vaccineCode.coding.code contains '212'  // J&J
       or I.vaccineCode.text contains 'COVID'

// Flu vaccines
define FluVaccinations:
  IPSImmunizations I
    where I.vaccineCode.coding.code contains '140'
       or I.vaccineCode.coding.code contains '141'
       or I.vaccineCode.text contains 'Influenza'

// Has immunization records
define HasImmunizationRecords:
  exists IPSImmunizations

// =====================================================
// IPS SECTION 5: PROCEDURES (Recommended)
// LOINC: 47519-4
// =====================================================

// All procedures
define AllProcedures:
  [Procedure]

// Completed procedures (for IPS)
define IPSProcedures:
  [Procedure] P
    where P.status = 'completed'

// Recent procedures (last 2 years)
define RecentProcedures:
  IPSProcedures P
    where P.performed as dateTime >= Today() - 2 years

// Surgical procedures
define SurgicalProcedures:
  IPSProcedures P
    where exists (
      P.category Cat
        where Cat.coding.code contains '387713003'  // Surgical procedure
    ) or P.code.text contains 'surgery'
      or P.code.text contains 'operation'

// Has procedure history
define HasProcedureHistory:
  exists IPSProcedures

// =====================================================
// IPS SECTION 6: RESULTS (Recommended)
// LOINC: 30954-2
// =====================================================

// All observations
define AllObservations:
  [Observation]

// Laboratory results (for IPS)
define IPSLabResults:
  [Observation] O
    where O.status in {'final', 'amended', 'corrected'}
      and exists (
        O.category Cat
          where Cat.coding.code contains 'laboratory'
      )

// Recent lab results (last 6 months)
define RecentLabResults:
  IPSLabResults O
    where O.effective as dateTime >= Today() - 6 months

// Most recent lab of each type
define LatestLabResults:
  IPSLabResults O
    where O.effective as dateTime >= Today() - 6 months

// Common IPS labs: HbA1c
define HbA1cResults:
  IPSLabResults O
    where O.code.coding.code contains '4548-4'
       or O.code.text contains 'HbA1c'
       or O.code.text contains 'Hemoglobin A1c'

// Common IPS labs: Creatinine
define CreatinineResults:
  IPSLabResults O
    where O.code.coding.code contains '2160-0'
       or O.code.text contains 'Creatinine'

// Common IPS labs: Lipid Panel
define LipidResults:
  IPSLabResults O
    where O.code.coding.code contains '2093-3'  // Cholesterol
       or O.code.coding.code contains '2571-8'  // Triglycerides
       or O.code.coding.code contains '2085-9'  // HDL
       or O.code.coding.code contains '2089-1'  // LDL

// Has lab results
define HasLabResults:
  exists IPSLabResults

// =====================================================
// IPS SECTION 7: VITAL SIGNS (Recommended)
// LOINC: 8716-3
// =====================================================

// Vital sign observations
define IPSVitalSigns:
  [Observation] O
    where O.status in {'final', 'amended', 'corrected'}
      and exists (
        O.category Cat
          where Cat.coding.code contains 'vital-signs'
      )

// Recent vital signs (last 30 days)
define RecentVitalSigns:
  IPSVitalSigns O
    where O.effective as dateTime >= Today() - 30 days

// Latest blood pressure
define LatestBloodPressure:
  First(
    IPSVitalSigns O
      where O.code.coding.code contains '85354-9'
         or O.code.text contains 'Blood pressure'
      sort by (effective as dateTime) desc
  )

// Latest heart rate
define LatestHeartRate:
  First(
    IPSVitalSigns O
      where O.code.coding.code contains '8867-4'
         or O.code.text contains 'Heart rate'
      sort by (effective as dateTime) desc
  )

// Latest body weight
define LatestWeight:
  First(
    IPSVitalSigns O
      where O.code.coding.code contains '29463-7'
         or O.code.text contains 'Body weight'
      sort by (effective as dateTime) desc
  )

// Latest BMI
define LatestBMI:
  First(
    IPSVitalSigns O
      where O.code.coding.code contains '39156-5'
         or O.code.text contains 'Body mass index'
      sort by (effective as dateTime) desc
  )

// Has vital signs
define HasVitalSigns:
  exists IPSVitalSigns

// =====================================================
// IPS COMPLETENESS CHECK
// =====================================================

// Required sections status
define RequiredSectionsComplete:
  Tuple {
    allergies: HasDocumentedAllergies or NoKnownAllergies,
    medications: HasActiveMedications,
    problems: HasActiveProblems
  }

// All required sections have data
define HasAllRequiredSections:
  (HasDocumentedAllergies or NoKnownAllergies)
    and (HasActiveMedications or not exists AllMedicationRequests)
    and (HasActiveProblems or not exists AllConditions)

// Recommended sections status
define RecommendedSectionsComplete:
  Tuple {
    immunizations: HasImmunizationRecords,
    procedures: HasProcedureHistory,
    results: HasLabResults,
    vitalSigns: HasVitalSigns
  }

// IPS readiness score (0-7 sections complete)
define IPSReadinessScore:
  (if HasDocumentedAllergies or NoKnownAllergies then 1 else 0)
  + (if HasActiveMedications then 1 else 0)
  + (if HasActiveProblems then 1 else 0)
  + (if HasImmunizationRecords then 1 else 0)
  + (if HasProcedureHistory then 1 else 0)
  + (if HasLabResults then 1 else 0)
  + (if HasVitalSigns then 1 else 0)

// Missing sections
define MissingSections:
  List<String> {
    if not (HasDocumentedAllergies or NoKnownAllergies) then 'Allergies' else null,
    if not HasActiveMedications then 'Medications' else null,
    if not HasActiveProblems then 'Problems' else null,
    if not HasImmunizationRecords then 'Immunizations' else null,
    if not HasProcedureHistory then 'Procedures' else null,
    if not HasLabResults then 'Lab Results' else null,
    if not HasVitalSigns then 'Vital Signs' else null
  }

define ActualMissingSections:
  MissingSections S where S is not null

// =====================================================
// IPS SECTION COUNTS
// =====================================================

define IPSSectionCounts:
  Tuple {
    allergies: Count(IPSAllergies),
    medications: Count(IPSMedications),
    problems: Count(IPSProblems),
    immunizations: Count(IPSImmunizations),
    procedures: Count(IPSProcedures),
    labResults: Count(RecentLabResults),
    vitalSigns: Count(RecentVitalSigns)
  }

// Total entries across all sections
define TotalIPSEntries:
  Count(IPSAllergies)
  + Count(IPSMedications)
  + Count(IPSProblems)
  + Count(IPSImmunizations)
  + Count(IPSProcedures)
  + Count(RecentLabResults)
  + Count(RecentVitalSigns)

// =====================================================
// CLINICAL ALERTS FOR IPS GENERATION
// =====================================================

// Important clinical flags
define ClinicalAlerts:
  List<String> {
    if exists HighCriticalityAllergies then 'High criticality allergy documented' else null,
    if exists SevereReactionAllergies then 'History of severe allergic reaction' else null,
    if ActiveMedicationCount > 10 then 'Polypharmacy: ' + ToString(ActiveMedicationCount) + ' active medications' else null,
    if Count(ChronicConditions) > 5 then 'Multiple chronic conditions' else null
  }

define ActiveClinicalAlerts:
  ClinicalAlerts A where A is not null

// =====================================================
// IPS SUMMARY OUTPUT
// =====================================================

define IPSSummary:
  Tuple {
    // Completeness
    readinessScore: IPSReadinessScore,
    maxScore: 7,
    percentComplete: (IPSReadinessScore * 100) / 7,
    hasRequiredSections: HasAllRequiredSections,
    missingSections: ActualMissingSections,

    // Section counts
    sectionCounts: IPSSectionCounts,
    totalEntries: TotalIPSEntries,

    // Key clinical data
    highCriticalityAllergies: Count(HighCriticalityAllergies),
    activeMedications: ActiveMedicationCount,
    activeProblems: Count(IPSProblems),

    // Alerts
    alerts: ActiveClinicalAlerts
  }

// =====================================================
// IPS GENERATION READINESS MESSAGE
// =====================================================

define IPSReadinessMessage:
  if IPSReadinessScore = 7 then
    'Patient record is complete for IPS generation. All 7 sections have data.'
  else if IPSReadinessScore >= 5 then
    'Patient record is mostly complete. ' + ToString(7 - IPSReadinessScore) + ' section(s) missing optional data.'
  else if HasAllRequiredSections then
    'Required IPS sections are complete. ' + ToString(7 - IPSReadinessScore) + ' recommended sections missing data.'
  else
    'Patient record is incomplete for IPS. Missing required sections. Score: ' + ToString(IPSReadinessScore) + '/7'

// =====================================================
// CROSS-BORDER CONSIDERATIONS
// =====================================================

// Check for coded vs text-only data (important for interoperability)
define AllergiesWithCoding:
  IPSAllergies A
    where exists (A.code.coding)

define MedicationsWithCoding:
  IPSMedications M
    where exists (M.medication.coding)
       or exists (M.medication.reference)

define ConditionsWithCoding:
  IPSProblems C
    where exists (C.code.coding)

// Interoperability score (percentage of coded data)
define CodingCompleteness:
  Tuple {
    allergiesCoded: if Count(IPSAllergies) > 0 then (Count(AllergiesWithCoding) * 100) / Count(IPSAllergies) else 100,
    medicationsCoded: if Count(IPSMedications) > 0 then (Count(MedicationsWithCoding) * 100) / Count(IPSMedications) else 100,
    conditionsCoded: if Count(IPSProblems) > 0 then (Count(ConditionsWithCoding) * 100) / Count(IPSProblems) else 100
  }

// Ready for cross-border exchange
define ReadyForCrossBorderExchange:
  HasAllRequiredSections
    and Count(AllergiesWithCoding) = Count(IPSAllergies)
    and Count(ConditionsWithCoding) = Count(IPSProblems)
