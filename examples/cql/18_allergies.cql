/*
 * CQL Example 18: Allergy Checking and Drug Safety
 *
 * Demonstrates:
 * - Querying AllergyIntolerance resources
 * - Checking for active allergies
 * - Drug class allergy detection
 * - Medication safety checks
 */

library AllergyChecking version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "AllergyIntolerance Clinical": 'http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical'
codesystem "AllergyIntolerance Verification": 'http://terminology.hl7.org/CodeSystem/allergyintolerance-verification'

// Codes
code "Active": 'active' from "AllergyIntolerance Clinical"
code "Confirmed": 'confirmed' from "AllergyIntolerance Verification"
code "Penicillin": '7980' from "RxNorm"
code "Amoxicillin": '723' from "RxNorm"
code "Ampicillin": '733' from "RxNorm"

// Value Sets (inline definitions for demonstration)
valueset "Penicillin Class Medications": 'http://example.org/fhir/ValueSet/penicillin-class'

context Patient

// =====================================================
// Basic Allergy Queries
// =====================================================

// Get all allergies for the patient
define AllAllergies:
  [AllergyIntolerance]

// Get only active allergies
define ActiveAllergies:
  [AllergyIntolerance] A
    where A.clinicalStatus.coding.code contains 'active'

// Get confirmed allergies
define ConfirmedAllergies:
  [AllergyIntolerance] A
    where A.verificationStatus.coding.code contains 'confirmed'

// Get active AND confirmed allergies
define ActiveConfirmedAllergies:
  ActiveAllergies A
    where A.verificationStatus.coding.code contains 'confirmed'

// =====================================================
// Allergy Classification
// =====================================================

// Medication allergies
define MedicationAllergies:
  ActiveConfirmedAllergies A
    where A.category contains 'medication'

// Food allergies
define FoodAllergies:
  ActiveConfirmedAllergies A
    where A.category contains 'food'

// Environmental allergies
define EnvironmentalAllergies:
  ActiveConfirmedAllergies A
    where A.category contains 'environment'

// High criticality allergies
define HighCriticalityAllergies:
  ActiveConfirmedAllergies A
    where A.criticality = 'high'

// =====================================================
// Specific Drug Allergy Checks
// =====================================================

// Check for penicillin allergy
define HasPenicillinAllergy:
  exists (
    MedicationAllergies A
      where A.code.coding.code contains '7980'  // RxNorm code for Penicillin
         or A.code.coding.display contains 'Penicillin'
         or A.code.text contains 'penicillin'
  )

// Check for sulfa allergy
define HasSulfaAllergy:
  exists (
    MedicationAllergies A
      where A.code.coding.display contains 'Sulfa'
         or A.code.coding.display contains 'Sulfon'
         or A.code.text contains 'sulfa'
  )

// Check for aspirin allergy
define HasAspirinAllergy:
  exists (
    MedicationAllergies A
      where A.code.coding.code contains '1191'  // RxNorm for aspirin
         or A.code.coding.display contains 'Aspirin'
  )

// =====================================================
// Reaction Severity Analysis
// =====================================================

// Allergies with severe reactions
define AllergiesWithSevereReactions:
  ActiveConfirmedAllergies A
    where exists (A.reaction R where R.severity = 'severe')

// Allergies with anaphylaxis history
define AllergiesWithAnaphylaxis:
  ActiveConfirmedAllergies A
    where exists (
      A.reaction R
        where exists (
          R.manifestation M
            where M.coding.code contains '39579001'  // SNOMED for anaphylaxis
               or M.text contains 'anaphyla'
        )
    )

// Get all reaction manifestations
define AllReactionManifestations:
  flatten (
    ActiveConfirmedAllergies A
      return all (
        flatten (A.reaction R return all R.manifestation)
      )
  )

// =====================================================
// Medication Safety Functions
// =====================================================

// Check if a medication code is safe for this patient
define function IsMedicationSafe(medCode String):
  not exists (
    MedicationAllergies A
      where A.code.coding.code contains medCode
  )

// Example: Is Amoxicillin safe?
// (Should be unsafe for patients with penicillin allergy due to cross-reactivity)
define IsAmoxicillinSafe:
  not HasPenicillinAllergy

// =====================================================
// Penicillin Cross-Reactivity Check
// =====================================================

// Beta-lactam antibiotics that may cross-react with penicillin
define PenicillinCrossReactants:
  {'723', '733', '1592', '2563'}  // Amoxicillin, Ampicillin, Cephalexin, etc.

define HasBetaLactamAllergy:
  HasPenicillinAllergy  // Simplified: if allergic to penicillin, avoid all beta-lactams

// =====================================================
// Allergy Summary
// =====================================================

// Count of allergies by type
define MedicationAllergyCount:
  Count(MedicationAllergies)

define FoodAllergyCount:
  Count(FoodAllergies)

define EnvironmentalAllergyCount:
  Count(EnvironmentalAllergies)

// Total allergy count
define TotalActiveAllergyCount:
  Count(ActiveConfirmedAllergies)

// Has any allergies?
define HasDocumentedAllergies:
  exists ActiveConfirmedAllergies

// No known allergies?
define NoKnownAllergies:
  not exists [AllergyIntolerance]

// =====================================================
// Recent Allergy Documentation
// =====================================================

// Allergies recorded in the last year
define RecentlyRecordedAllergies:
  ActiveConfirmedAllergies A
    where A.recordedDate >= Today() - 1 year

// Last allergy recorded date
define MostRecentAllergyDate:
  Max([AllergyIntolerance] A return A.recordedDate)

// =====================================================
// Allergy Alert Messages
// =====================================================

define AllergyAlertMessage:
  if HasPenicillinAllergy then
    'ALERT: Patient has documented penicillin allergy. Avoid penicillin and related beta-lactam antibiotics.'
  else if HasSulfaAllergy then
    'ALERT: Patient has documented sulfa allergy. Avoid sulfonamide medications.'
  else if TotalActiveAllergyCount > 0 then
    'Patient has ' + ToString(TotalActiveAllergyCount) + ' documented allergies. Review before prescribing.'
  else
    'No active allergies documented.'
