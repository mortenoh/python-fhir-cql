/*
 * CQL Example 24: Medication Safety and Drug Interactions
 *
 * Demonstrates:
 * - Drug-drug interaction detection
 * - Drug-disease contraindications
 * - Renal/hepatic dosing considerations
 * - Duplicate therapy detection
 * - High-risk medication monitoring
 */

library MedicationSafety version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "LOINC": 'http://loinc.org'

// Drug classes (RxNorm)
code "Warfarin": '11289' from "RxNorm"
code "Aspirin": '1191' from "RxNorm"
code "Metformin": '6809' from "RxNorm"
code "Lisinopril": '29046' from "RxNorm"
code "Potassium": '8591' from "RxNorm"
code "Digoxin": '3407' from "RxNorm"
code "Amiodarone": '703' from "RxNorm"
code "Simvastatin": '36567' from "RxNorm"

context Patient

// =====================================================
// Current Medications
// =====================================================

define ActiveMedications:
  [MedicationRequest] M
    where M.status = 'active'

define ActiveMedicationCodes:
  flatten (
    ActiveMedications M
      return all M.medication.coding.code
  )

define function IsOnMedication(rxnormCode String):
  exists (
    ActiveMedications M
      where M.medication.coding.code contains rxnormCode
  )

define function IsOnMedicationClass(classKeyword String):
  exists (
    ActiveMedications M
      where M.medication.coding.display contains classKeyword
  )

// =====================================================
// Drug-Drug Interaction Detection
// =====================================================

// Warfarin + Aspirin (increased bleeding risk)
define WarfarinAspirinInteraction:
  IsOnMedication('11289') and IsOnMedication('1191')

// Digoxin + Amiodarone (increased digoxin toxicity)
define DigoxinAmiodaroneInteraction:
  IsOnMedication('3407') and IsOnMedication('703')

// ACE inhibitor + Potassium (hyperkalemia risk)
define ACEPotassiumInteraction:
  IsOnMedicationClass('pril') and IsOnMedication('8591')

// Statin + Amiodarone (myopathy risk with simvastatin)
define StatinAmiodaroneInteraction:
  IsOnMedication('36567') and IsOnMedication('703')

// Multiple NSAIDs
define MultipleNSAIDs:
  Count(
    ActiveMedications M
      where M.medication.coding.display contains 'ibuprofen'
         or M.medication.coding.display contains 'naproxen'
         or M.medication.coding.display contains 'diclofenac'
         or M.medication.coding.display contains 'meloxicam'
  ) > 1

// Opioid + Benzodiazepine (respiratory depression)
define OpioidBenzoInteraction:
  IsOnMedicationClass('codone') and IsOnMedicationClass('azepam')

// All detected interactions
define DetectedDrugInteractions:
  List<String> {
    if WarfarinAspirinInteraction then 'Warfarin + Aspirin: Increased bleeding risk' else null,
    if DigoxinAmiodaroneInteraction then 'Digoxin + Amiodarone: Increased digoxin toxicity' else null,
    if ACEPotassiumInteraction then 'ACE inhibitor + Potassium: Hyperkalemia risk' else null,
    if StatinAmiodaroneInteraction then 'Simvastatin + Amiodarone: Myopathy risk' else null,
    if MultipleNSAIDs then 'Multiple NSAIDs: Increased GI/renal risk' else null,
    if OpioidBenzoInteraction then 'Opioid + Benzodiazepine: Respiratory depression risk' else null
  }

define ActiveDrugInteractions:
  DetectedDrugInteractions I where I is not null

define HasDrugInteractions:
  exists ActiveDrugInteractions

// =====================================================
// Drug-Disease Contraindications
// =====================================================

define ActiveConditions:
  [Condition] C
    where C.clinicalStatus.coding.code contains 'active'

define function HasCondition(snomedCode String):
  exists (
    ActiveConditions C
      where C.code.coding.code contains snomedCode
  )

// Metformin contraindicated in severe renal impairment
define MetforminRenalContraindication:
  IsOnMedication('6809') and HasCondition('236425005')  // CKD stage 4-5

// NSAIDs contraindicated in heart failure
define NSAIDHeartFailureContraindication:
  (IsOnMedicationClass('ibuprofen') or IsOnMedicationClass('naproxen'))
    and HasCondition('84114007')  // Heart failure

// Beta-blockers caution in asthma
define BetaBlockerAsthmaContraindication:
  IsOnMedicationClass('olol') and HasCondition('195967001')  // Asthma

// Antihistamines in glaucoma
define AntihistamineGlaucomaContraindication:
  IsOnMedicationClass('diphenhydramine') and HasCondition('23986001')  // Glaucoma

define DrugDiseaseContraindications:
  List<String> {
    if MetforminRenalContraindication then 'Metformin contraindicated: Severe renal impairment' else null,
    if NSAIDHeartFailureContraindication then 'NSAID contraindicated: Heart failure' else null,
    if BetaBlockerAsthmaContraindication then 'Beta-blocker caution: Asthma' else null,
    if AntihistamineGlaucomaContraindication then 'Antihistamine caution: Glaucoma' else null
  }

define ActiveContraindications:
  DrugDiseaseContraindications C where C is not null

// =====================================================
// Renal Dosing Considerations
// =====================================================

define MostRecentCreatinine:
  Last(
    [Observation] O
      where O.code.coding.code contains '2160-0'
        and O.status = 'final'
      sort by effective as dateTime
  ).value as Quantity

define MostRecentGFR:
  Last(
    [Observation] O
      where O.code.coding.code contains '33914-3'
        and O.status = 'final'
      sort by effective as dateTime
  ).value as Quantity

define RenalFunction:
  case
    when MostRecentGFR is null then 'Unknown'
    when MostRecentGFR.value >= 90 then 'Normal'
    when MostRecentGFR.value >= 60 then 'Mild impairment'
    when MostRecentGFR.value >= 30 then 'Moderate impairment'
    when MostRecentGFR.value >= 15 then 'Severe impairment'
    else 'End-stage renal disease'
  end

// Medications requiring renal adjustment
define MedicationsNeedingRenalAdjustment:
  ActiveMedications M
    where M.medication.coding.display contains 'metformin'
       or M.medication.coding.display contains 'gabapentin'
       or M.medication.coding.display contains 'enoxaparin'
       or M.medication.coding.display contains 'levofloxacin'
       or M.medication.coding.display contains 'digoxin'

define RenalDosingAlerts:
  if RenalFunction in {'Moderate impairment', 'Severe impairment', 'End-stage renal disease'}
    and exists MedicationsNeedingRenalAdjustment
  then 'Review dosing for renally-cleared medications'
  else null

// =====================================================
// Hepatic Dosing Considerations
// =====================================================

define MostRecentALT:
  Last(
    [Observation] O
      where O.code.coding.code contains '1742-6'
        and O.status = 'final'
      sort by effective as dateTime
  ).value as Quantity

define MostRecentAST:
  Last(
    [Observation] O
      where O.code.coding.code contains '1920-8'
        and O.status = 'final'
      sort by effective as dateTime
  ).value as Quantity

define ElevatedLiverEnzymes:
  (MostRecentALT.value > 40) or (MostRecentAST.value > 40)

define HepatotoxicMedications:
  ActiveMedications M
    where M.medication.coding.display contains 'acetaminophen'
       or M.medication.coding.display contains 'statin'
       or M.medication.coding.display contains 'methotrexate'
       or M.medication.coding.display contains 'valproate'

define HepaticMonitoringNeeded:
  ElevatedLiverEnzymes and exists HepatotoxicMedications

// =====================================================
// Duplicate Therapy Detection
// =====================================================

// Multiple ACE inhibitors or ARBs
define DuplicateRASBlockade:
  Count(
    ActiveMedications M
      where M.medication.coding.display contains 'pril'
         or M.medication.coding.display contains 'sartan'
  ) > 1

// Multiple statins
define DuplicateStatins:
  Count(
    ActiveMedications M
      where M.medication.coding.display contains 'statin'
  ) > 1

// Multiple PPIs
define DuplicatePPIs:
  Count(
    ActiveMedications M
      where M.medication.coding.display contains 'prazole'
  ) > 1

// Multiple antidepressants of same class
define DuplicateSSRIs:
  Count(
    ActiveMedications M
      where M.medication.coding.display contains 'sertraline'
         or M.medication.coding.display contains 'fluoxetine'
         or M.medication.coding.display contains 'paroxetine'
         or M.medication.coding.display contains 'citalopram'
         or M.medication.coding.display contains 'escitalopram'
  ) > 1

define DuplicateTherapyAlerts:
  List<String> {
    if DuplicateRASBlockade then 'Duplicate therapy: Multiple RAS blockers' else null,
    if DuplicateStatins then 'Duplicate therapy: Multiple statins' else null,
    if DuplicatePPIs then 'Duplicate therapy: Multiple PPIs' else null,
    if DuplicateSSRIs then 'Duplicate therapy: Multiple SSRIs' else null
  }

// =====================================================
// High-Risk Medications (ISMP List)
// =====================================================

define HighRiskMedications:
  ActiveMedications M
    where M.medication.coding.display contains 'insulin'
       or M.medication.coding.display contains 'warfarin'
       or M.medication.coding.display contains 'heparin'
       or M.medication.coding.display contains 'methotrexate'
       or M.medication.coding.display contains 'digoxin'
       or M.medication.coding.display contains 'opioid'
       or M.medication.coding.display contains 'chemotherapy'

define IsOnHighRiskMedication:
  exists HighRiskMedications

define HighRiskMedicationCount:
  Count(HighRiskMedications)

// =====================================================
// Anticholinergic Burden
// =====================================================

define AnticholinergicMedications:
  ActiveMedications M
    where M.medication.coding.display contains 'diphenhydramine'
       or M.medication.coding.display contains 'oxybutynin'
       or M.medication.coding.display contains 'amitriptyline'
       or M.medication.coding.display contains 'promethazine'
       or M.medication.coding.display contains 'hydroxyzine'

define AnticholinergicBurden:
  Count(AnticholinergicMedications)

define HighAnticholinergicBurden:
  AnticholinergicBurden >= 2

// =====================================================
// Elderly-Specific Safety (Beers Criteria concepts)
// =====================================================

define PatientAge:
  AgeInYears()

define IsElderly:
  PatientAge >= 65

// Potentially inappropriate medications in elderly
define BeersListMedications:
  ActiveMedications M
    where M.medication.coding.display contains 'benzodiazepine'
       or M.medication.coding.display contains 'diphenhydramine'
       or M.medication.coding.display contains 'muscle relaxant'

define BeersListAlert:
  if IsElderly and exists BeersListMedications
  then 'Review potentially inappropriate medications for elderly patient'
  else null

// =====================================================
// Medication Safety Summary
// =====================================================

define TotalMedicationCount:
  Count(ActiveMedications)

define Polypharmacy:
  TotalMedicationCount >= 5

define ExcessivePolypharmacy:
  TotalMedicationCount >= 10

define MedicationSafetySummary:
  Tuple {
    totalMedications: TotalMedicationCount,
    polypharmacy: Polypharmacy,
    excessivePolypharmacy: ExcessivePolypharmacy,
    hasDrugInteractions: HasDrugInteractions,
    interactionCount: Count(ActiveDrugInteractions),
    highRiskMedicationCount: HighRiskMedicationCount,
    anticholinergicBurden: AnticholinergicBurden,
    renalFunction: RenalFunction,
    hepaticMonitoringNeeded: HepaticMonitoringNeeded
  }

// =====================================================
// All Safety Alerts
// =====================================================

define AllSafetyAlerts:
  ActiveDrugInteractions
    union ActiveContraindications
    union (DuplicateTherapyAlerts T where T is not null)
    union {BeersListAlert}
    union {RenalDosingAlerts}

define SafetyAlertCount:
  Count(AllSafetyAlerts A where A is not null)

define HasSafetyAlerts:
  SafetyAlertCount > 0
