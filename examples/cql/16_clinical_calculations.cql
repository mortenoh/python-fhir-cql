/*
 * Clinical Calculations - Common clinical formulas and calculations
 */
library ClinicalCalculations version '1.0.0'

using FHIR version '4.0.1'

codesystem "LOINC": 'http://loinc.org'

valueset "Body Weight": 'http://example.org/ValueSet/body-weight'
valueset "Body Height": 'http://example.org/ValueSet/body-height'
valueset "Serum Creatinine": 'http://example.org/ValueSet/serum-creatinine'
valueset "Total Cholesterol": 'http://example.org/ValueSet/total-cholesterol'
valueset "HDL Cholesterol": 'http://example.org/ValueSet/hdl-cholesterol'
valueset "Systolic Blood Pressure": 'http://example.org/ValueSet/systolic-bp'
valueset "Diastolic Blood Pressure": 'http://example.org/ValueSet/diastolic-bp'

context Patient

// =====================================================
// Body Mass Index (BMI)
// =====================================================

// BMI = weight(kg) / height(m)^2
define function CalculateBMI(weightKg Decimal, heightCm Decimal) returns Decimal:
    if weightKg is null or heightCm is null or heightCm = 0 then null
    else Round(weightKg / Power(heightCm / 100, 2), 1)

define function BMICategory(bmi Decimal) returns String:
    if bmi is null then null
    else if bmi < 18.5 then 'Underweight'
    else if bmi < 25.0 then 'Normal'
    else if bmi < 30.0 then 'Overweight'
    else if bmi < 35.0 then 'Obese Class I'
    else if bmi < 40.0 then 'Obese Class II'
    else 'Obese Class III'

// Get most recent weight and height
define MostRecentWeight:
    Last([Observation: "Body Weight"] W sort by effective)

define MostRecentHeight:
    Last([Observation: "Body Height"] H sort by effective)

define PatientBMI:
    CalculateBMI(MostRecentWeight.value.value, MostRecentHeight.value.value)

define PatientBMICategory:
    BMICategory(PatientBMI)

// =====================================================
// Body Surface Area (BSA)
// =====================================================

// Mosteller formula: BSA (m²) = sqrt((height(cm) × weight(kg)) / 3600)
define function CalculateBSA(weightKg Decimal, heightCm Decimal) returns Decimal:
    if weightKg is null or heightCm is null then null
    else Round(Sqrt((heightCm * weightKg) / 3600), 2)

// DuBois formula: BSA = 0.007184 × height^0.725 × weight^0.425
define function CalculateBSA_DuBois(weightKg Decimal, heightCm Decimal) returns Decimal:
    if weightKg is null or heightCm is null then null
    else Round(0.007184 * Power(heightCm, 0.725) * Power(weightKg, 0.425), 2)

// =====================================================
// Renal Function (eGFR)
// =====================================================

// CKD-EPI Creatinine Equation (simplified)
define function CalculateEGFR_CKDEPI(
    creatinine Decimal,
    age Integer,
    isFemale Boolean
) returns Integer:
    if creatinine is null or age is null then null
    else
        let kappa: if isFemale then 0.7 else 0.9,
            alpha: if isFemale then -0.329 else -0.411,
            crRatio: creatinine / kappa,
            minTerm: Power(Min(crRatio, 1.0), alpha),
            maxTerm: Power(Max(crRatio, 1.0), -1.209),
            ageTerm: Power(0.993, age),
            sexFactor: if isFemale then 1.018 else 1.0
        return Truncate(141 * minTerm * maxTerm * ageTerm * sexFactor)

// Cockcroft-Gault CrCl
define function CalculateCrCl(
    creatinine Decimal,
    weightKg Decimal,
    age Integer,
    isFemale Boolean
) returns Decimal:
    if creatinine is null or creatinine = 0 or weightKg is null or age is null then null
    else
        let baseCrCl: ((140 - age) * weightKg) / (72 * creatinine)
        return Round(baseCrCl * (if isFemale then 0.85 else 1.0), 1)

// CKD Stage based on eGFR
define function CKDStage(egfr Integer) returns String:
    if egfr is null then null
    else if egfr >= 90 then 'Stage 1'
    else if egfr >= 60 then 'Stage 2'
    else if egfr >= 45 then 'Stage 3a'
    else if egfr >= 30 then 'Stage 3b'
    else if egfr >= 15 then 'Stage 4'
    else 'Stage 5'

// =====================================================
// Cardiovascular Risk (Framingham)
// =====================================================

// Simplified Framingham Risk Score (10-year CVD risk)
define function FraminghamRiskScore(
    age Integer,
    totalCholesterol Decimal,
    hdlCholesterol Decimal,
    systolicBP Decimal,
    isTreatedBP Boolean,
    isSmoker Boolean,
    isDiabetic Boolean,
    isMale Boolean
) returns Decimal:
    // Simplified implementation - actual scoring uses lookup tables
    let agePoints: if isMale then
                       if age < 35 then 0
                       else if age < 45 then 6
                       else if age < 55 then 11
                       else if age < 65 then 15
                       else 18
                   else
                       if age < 35 then 0
                       else if age < 45 then 3
                       else if age < 55 then 6
                       else if age < 65 then 9
                       else 12,
        cholPoints: if totalCholesterol < 160 then 0
                    else if totalCholesterol < 200 then 1
                    else if totalCholesterol < 240 then 2
                    else 3,
        hdlPoints: if hdlCholesterol >= 60 then -1
                   else if hdlCholesterol >= 50 then 0
                   else if hdlCholesterol >= 40 then 1
                   else 2,
        bpPoints: if systolicBP < 120 then 0
                  else if systolicBP < 140 then (if isTreatedBP then 2 else 1)
                  else if systolicBP < 160 then (if isTreatedBP then 3 else 2)
                  else (if isTreatedBP then 4 else 3),
        smokePoints: if isSmoker then 2 else 0,
        diabetesPoints: if isDiabetic then 3 else 0,
        totalPoints: agePoints + cholPoints + hdlPoints + bpPoints + smokePoints + diabetesPoints
    // Convert points to approximate risk percentage
    return if totalPoints < 5 then 1.0
           else if totalPoints < 10 then 5.0
           else if totalPoints < 15 then 10.0
           else if totalPoints < 20 then 20.0
           else 30.0

// =====================================================
// Ideal Body Weight
// =====================================================

// Devine formula
define function IdealBodyWeight(heightCm Decimal, isFemale Boolean) returns Decimal:
    if heightCm is null then null
    else
        let heightInches: heightCm / 2.54,
            inchesOver5Feet: heightInches - 60
        return if isFemale then
                   45.5 + (2.3 * inchesOver5Feet)
               else
                   50.0 + (2.3 * inchesOver5Feet)

// Adjusted Body Weight (for obesity)
define function AdjustedBodyWeight(actualKg Decimal, idealKg Decimal) returns Decimal:
    if actualKg is null or idealKg is null then null
    else idealKg + (0.4 * (actualKg - idealKg))

// =====================================================
// Pediatric Calculations
// =====================================================

// Age in months
define PatientAgeInMonths:
    months between Patient.birthDate and Today()

// Age in days
define PatientAgeInDays:
    days between Patient.birthDate and Today()

// Check if pediatric (under 18)
define IsPediatric:
    years between Patient.birthDate and Today() < 18

// Check if neonate (under 28 days)
define IsNeonate:
    days between Patient.birthDate and Today() < 28

// Check if infant (under 1 year)
define IsInfant:
    years between Patient.birthDate and Today() < 1

// =====================================================
// Drug Dosing
// =====================================================

// Weight-based dosing
define function WeightBasedDose(dosePerKg Decimal, weightKg Decimal) returns Decimal:
    if dosePerKg is null or weightKg is null then null
    else Round(dosePerKg * weightKg, 2)

// BSA-based dosing (chemotherapy)
define function BSABasedDose(dosePerM2 Decimal, bsa Decimal) returns Decimal:
    if dosePerM2 is null or bsa is null then null
    else Round(dosePerM2 * bsa, 2)

// Renal dose adjustment
define function RenalDoseAdjustment(standardDose Decimal, egfr Integer) returns Decimal:
    if standardDose is null or egfr is null then null
    else if egfr >= 60 then standardDose
    else if egfr >= 30 then standardDose * 0.75
    else if egfr >= 15 then standardDose * 0.5
    else standardDose * 0.25

// =====================================================
// Unit Conversions
// =====================================================

// Temperature
define function CelsiusToFahrenheit(c Decimal) returns Decimal:
    Round(c * 9.0 / 5.0 + 32, 1)

define function FahrenheitToCelsius(f Decimal) returns Decimal:
    Round((f - 32) * 5.0 / 9.0, 1)

// Weight
define function PoundsToKg(lbs Decimal) returns Decimal:
    Round(lbs / 2.205, 2)

define function KgToPounds(kg Decimal) returns Decimal:
    Round(kg * 2.205, 2)

// Height
define function InchesToCm(inches Decimal) returns Decimal:
    Round(inches * 2.54, 1)

define function CmToInches(cm Decimal) returns Decimal:
    Round(cm / 2.54, 1)

// Glucose
define function MgDlToMmolL(mgdl Decimal) returns Decimal:
    Round(mgdl / 18.0, 2)

define function MmolLToMgDl(mmol Decimal) returns Decimal:
    Round(mmol * 18.0, 1)

// =====================================================
// Patient Demographics
// =====================================================

define PatientAge:
    years between Patient.birthDate and Today()

define PatientIsFemale:
    Patient.gender = 'female'

define PatientMostRecentCreatinine:
    Last([Observation: "Serum Creatinine"] sort by effective)

define PatientEGFR:
    CalculateEGFR_CKDEPI(
        PatientMostRecentCreatinine.value.value,
        PatientAge,
        PatientIsFemale
    )

define PatientCKDStage:
    CKDStage(PatientEGFR)
