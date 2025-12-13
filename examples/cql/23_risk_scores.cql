/*
 * CQL Example 23: Clinical Risk Scoring Algorithms
 *
 * Demonstrates:
 * - CHA2DS2-VASc score (stroke risk in AFib)
 * - HAS-BLED score (bleeding risk)
 * - Framingham Risk Score (cardiovascular)
 * - MELD score (liver disease severity)
 * - Wells criteria (DVT probability)
 */

library RiskScores version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "ICD10": 'http://hl7.org/fhir/sid/icd-10-cm'
codesystem "LOINC": 'http://loinc.org'

// Condition codes
code "Atrial Fibrillation": '49436004' from "SNOMED"
code "Heart Failure": '84114007' from "SNOMED"
code "Hypertension": '38341003' from "SNOMED"
code "Diabetes": '73211009' from "SNOMED"
code "Stroke": '230690007' from "SNOMED"
code "TIA": '266257000' from "SNOMED"
code "Vascular Disease": '27550009' from "SNOMED"

context Patient

// =====================================================
// Helper Definitions
// =====================================================

// Patient age in years
define PatientAge:
  AgeInYears()

// Patient gender
define PatientGender:
  Patient.gender

// Active conditions
define ActiveConditions:
  [Condition] C
    where C.clinicalStatus.coding.code contains 'active'

// Check for specific condition
define function HasCondition(snomedCode String):
  exists (
    ActiveConditions C
      where C.code.coding.code contains snomedCode
  )

// Get most recent lab value
define function MostRecentLabValue(loincCode String):
  Last(
    [Observation] O
      where O.code.coding.code contains loincCode
        and O.status = 'final'
      sort by effective as dateTime
  ).value as Quantity

// =====================================================
// CHA2DS2-VASc Score (Stroke Risk in AFib)
// =====================================================
// C - Congestive heart failure: 1 point
// H - Hypertension: 1 point
// A2 - Age >= 75: 2 points
// D - Diabetes: 1 point
// S2 - Stroke/TIA/thromboembolism: 2 points
// V - Vascular disease: 1 point
// A - Age 65-74: 1 point
// Sc - Sex category (female): 1 point

define HasAtrialFibrillation:
  HasCondition('49436004')

define HasCongestiveHeartFailure:
  HasCondition('84114007')

define HasHypertension:
  HasCondition('38341003')

define HasDiabetes:
  HasCondition('73211009')

define HasPriorStrokeOrTIA:
  HasCondition('230690007') or HasCondition('266257000')

define HasVascularDisease:
  HasCondition('27550009')

define CHADS2VASc_C:
  if HasCongestiveHeartFailure then 1 else 0

define CHADS2VASc_H:
  if HasHypertension then 1 else 0

define CHADS2VASc_A2:
  if PatientAge >= 75 then 2 else 0

define CHADS2VASc_D:
  if HasDiabetes then 1 else 0

define CHADS2VASc_S2:
  if HasPriorStrokeOrTIA then 2 else 0

define CHADS2VASc_V:
  if HasVascularDisease then 1 else 0

define CHADS2VASc_A:
  if PatientAge >= 65 and PatientAge < 75 then 1 else 0

define CHADS2VASc_Sc:
  if PatientGender = 'female' then 1 else 0

define CHA2DS2VAScScore:
  CHADS2VASc_C + CHADS2VASc_H + CHADS2VASc_A2 + CHADS2VASc_D
  + CHADS2VASc_S2 + CHADS2VASc_V + CHADS2VASc_A + CHADS2VASc_Sc

define CHA2DS2VAScRiskCategory:
  case
    when CHA2DS2VAScScore = 0 then 'Low'
    when CHA2DS2VAScScore = 1 then 'Low-Moderate'
    when CHA2DS2VAScScore = 2 then 'Moderate'
    else 'High'
  end

define AnticoagulationRecommended:
  HasAtrialFibrillation and CHA2DS2VAScScore >= 2

// =====================================================
// HAS-BLED Score (Bleeding Risk)
// =====================================================
// H - Hypertension (uncontrolled, >160 mmHg): 1 point
// A - Abnormal renal/liver function: 1-2 points
// S - Stroke history: 1 point
// B - Bleeding history/predisposition: 1 point
// L - Labile INR: 1 point
// E - Elderly (>65): 1 point
// D - Drugs/alcohol: 1-2 points

define HAS_BLED_H:
  if HasHypertension then 1 else 0

define HAS_BLED_A:
  0  // Would need liver/kidney function assessment

define HAS_BLED_S:
  if HasPriorStrokeOrTIA then 1 else 0

define HAS_BLED_B:
  0  // Would need bleeding history assessment

define HAS_BLED_L:
  0  // Would need INR variability assessment

define HAS_BLED_E:
  if PatientAge > 65 then 1 else 0

define HAS_BLED_D:
  0  // Would need medication/alcohol assessment

define HASBLEDScore:
  HAS_BLED_H + HAS_BLED_A + HAS_BLED_S + HAS_BLED_B
  + HAS_BLED_L + HAS_BLED_E + HAS_BLED_D

define HASBLEDRiskCategory:
  case
    when HASBLEDScore <= 2 then 'Low'
    when HASBLEDScore = 3 then 'Moderate'
    else 'High'
  end

define HighBleedingRisk:
  HASBLEDScore >= 3

// =====================================================
// Simplified Framingham Risk Score (10-year CVD)
// =====================================================

define IsSmoker:
  exists (
    [Observation] O
      where O.code.coding.code contains '72166-2'  // Smoking status
        and O.value.coding.code contains '449868002'  // Current smoker
  )

define TotalCholesterol:
  MostRecentLabValue('2093-3')

define HDLCholesterol:
  MostRecentLabValue('2085-9')

define SystolicBP:
  MostRecentLabValue('8480-6')

// Simplified point calculation (demonstration only)
define FraminghamAgePoints:
  case
    when PatientAge < 35 then 0
    when PatientAge >= 35 and PatientAge < 40 then 2
    when PatientAge >= 40 and PatientAge < 45 then 5
    when PatientAge >= 45 and PatientAge < 50 then 6
    when PatientAge >= 50 and PatientAge < 55 then 8
    when PatientAge >= 55 and PatientAge < 60 then 10
    when PatientAge >= 60 and PatientAge < 65 then 11
    when PatientAge >= 65 and PatientAge < 70 then 12
    when PatientAge >= 70 and PatientAge < 75 then 14
    else 15
  end

define FraminghamSmokingPoints:
  if IsSmoker then 4 else 0

define FraminghamDiabetesPoints:
  if HasDiabetes then 3 else 0

// Simplified total (full calculation requires cholesterol/BP values)
define FraminghamPoints:
  FraminghamAgePoints + FraminghamSmokingPoints + FraminghamDiabetesPoints

define FraminghamRiskCategory:
  case
    when FraminghamPoints < 10 then 'Low (<10%)'
    when FraminghamPoints >= 10 and FraminghamPoints < 15 then 'Intermediate (10-20%)'
    else 'High (>20%)'
  end

// =====================================================
// Wells Score for DVT
// =====================================================
// Active cancer: 1 point
// Paralysis/immobilization: 1 point
// Bedridden > 3 days or surgery in past 12 weeks: 1 point
// Tenderness along deep venous system: 1 point
// Entire leg swollen: 1 point
// Calf swelling > 3 cm: 1 point
// Pitting edema: 1 point
// Collateral superficial veins: 1 point
// Previously documented DVT: 1 point
// Alternative diagnosis as likely as DVT: -2 points

define HasActiveCancer:
  exists (
    ActiveConditions C
      where C.code.coding.display contains 'cancer'
         or C.code.coding.display contains 'malignant'
  )

define HasPriorDVT:
  exists (
    [Condition] C
      where C.code.coding.code contains '128053003'  // DVT
  )

define WellsScoreForDVT:
  (if HasActiveCancer then 1 else 0)
  + (if HasPriorDVT then 1 else 0)
  // Other criteria would require clinical assessment

define WellsDVTCategory:
  case
    when WellsScoreForDVT < 2 then 'Low probability'
    when WellsScoreForDVT = 2 then 'Moderate probability'
    else 'High probability'
  end

// =====================================================
// MELD Score (Model for End-Stage Liver Disease)
// =====================================================
// MELD = 3.78 x ln(bilirubin) + 11.2 x ln(INR) + 9.57 x ln(creatinine) + 6.43

define Bilirubin:
  MostRecentLabValue('1975-2')  // Total bilirubin

define INR:
  MostRecentLabValue('34714-6')  // INR

define Creatinine:
  MostRecentLabValue('2160-0')  // Creatinine

// Note: MELD requires natural log calculations
// This is a simplified presence check
define HasLiverDiseaseMarkers:
  Bilirubin is not null or INR is not null

// =====================================================
// BMI Calculation
// =====================================================

define Weight:
  MostRecentLabValue('29463-7')  // Body weight

define Height:
  MostRecentLabValue('8302-2')  // Body height

define BMI:
  if Weight is not null and Height is not null then
    (Weight.value / (Height.value / 100) / (Height.value / 100))
  else
    null

define BMICategory:
  case
    when BMI is null then 'Unknown'
    when BMI < 18.5 then 'Underweight'
    when BMI >= 18.5 and BMI < 25 then 'Normal'
    when BMI >= 25 and BMI < 30 then 'Overweight'
    when BMI >= 30 and BMI < 35 then 'Obese Class I'
    when BMI >= 35 and BMI < 40 then 'Obese Class II'
    else 'Obese Class III'
  end

// =====================================================
// Falls Risk Assessment (Simplified)
// =====================================================

define FallsRiskFactors:
  (if PatientAge >= 65 then 1 else 0)
  + (if HasCondition('84757009') then 1 else 0)  // Epilepsy
  + (if HasCondition('386661006') then 1 else 0)  // Fever
  + (if HasCondition('422587007') then 1 else 0)  // Nausea

define IsHighFallsRisk:
  FallsRiskFactors >= 2

// =====================================================
// Risk Summary Report
// =====================================================

define RiskSummary:
  Tuple {
    patientAge: PatientAge,
    gender: PatientGender,
    hasAFib: HasAtrialFibrillation,
    cha2ds2vasc: CHA2DS2VAScScore,
    strokeRisk: CHA2DS2VAScRiskCategory,
    anticoagulationRecommended: AnticoagulationRecommended,
    hasbled: HASBLEDScore,
    bleedingRisk: HASBLEDRiskCategory,
    framinghamRisk: FraminghamRiskCategory,
    bmiCategory: BMICategory
  }

// =====================================================
// Risk Alert Messages
// =====================================================

define RiskAlerts:
  List<String> {
    if AnticoagulationRecommended then 'Consider anticoagulation therapy (CHA2DS2-VASc >= 2)' else null,
    if HighBleedingRisk then 'High bleeding risk - monitor closely if anticoagulating' else null,
    if FraminghamPoints >= 15 then 'High cardiovascular risk - consider statin therapy' else null,
    if BMI >= 30 then 'Obesity - recommend weight management counseling' else null,
    if IsHighFallsRisk then 'High falls risk - implement fall prevention measures' else null
  }

// Active alerts only (non-null)
define ActiveRiskAlerts:
  RiskAlerts R where R is not null
