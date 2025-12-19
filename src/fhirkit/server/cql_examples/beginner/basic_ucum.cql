library UCUMConversions version '1.0.0'

// UCUM (Unified Code for Units of Measure) Unit Conversions
// These examples demonstrate unit conversions for clinical calculations

// ========================================
// Mass Conversions
// ========================================

define "GramsToMilligrams": ConvertQuantity(1 'g', 'mg')
// Result: 1000 'mg'

define "KilogramsToGrams": ConvertQuantity(1 'kg', 'g')
// Result: 1000 'g'

define "PoundsToKilograms": ConvertQuantity(150 '[lb_av]', 'kg')
// Result: 68.04 'kg'

define "OuncesToGrams": ConvertQuantity(1 '[oz_av]', 'g')
// Result: 28.35 'g'

define "MedicationDose": ConvertQuantity(500 'mg', 'g')
// Result: 0.5 'g'

// ========================================
// Volume Conversions
// ========================================

define "LitersToMilliliters": ConvertQuantity(1 'L', 'mL')
// Result: 1000 'mL'

define "MillilitersToLiters": ConvertQuantity(500 'mL', 'L')
// Result: 0.5 'L'

define "GallonsToLiters": ConvertQuantity(1 '[gal_us]', 'L')
// Result: 3.785 'L'

define "IVFluidRate": ConvertQuantity(125 'mL', 'L')
// Result: 0.125 'L'

// ========================================
// Temperature Conversions
// ========================================

define "BodyTempFahrenheitToCelsius": ConvertQuantity(98.6 '[degF]', 'Cel')
// Result: 37.0 'Cel'

define "BodyTempCelsiusToFahrenheit": ConvertQuantity(37 'Cel', '[degF]')
// Result: 98.6 '[degF]'

define "BoilingPointCelsiusToFahrenheit": ConvertQuantity(100 'Cel', '[degF]')
// Result: 212 '[degF]'

define "FreezingPointToKelvin": ConvertQuantity(0 'Cel', 'K')
// Result: 273.15 'K'

// ========================================
// Length Conversions (Patient Height)
// ========================================

define "InchesToCentimeters": ConvertQuantity(70 '[in_i]', 'cm')
// Result: 177.8 'cm' (5'10")

define "FeetToMeters": ConvertQuantity(6 '[ft_i]', 'm')
// Result: 1.83 'm'

define "CentimetersToInches": ConvertQuantity(175 'cm', '[in_i]')
// Result: 68.9 '[in_i]'

// ========================================
// Time Conversions
// ========================================

define "MinutesToSeconds": ConvertQuantity(5 'min', 's')
// Result: 300 's'

define "HoursToMinutes": ConvertQuantity(2 'h', 'min')
// Result: 120 'min'

define "DaysToHours": ConvertQuantity(1 'd', 'h')
// Result: 24 'h'

define "WeeksToDays": ConvertQuantity(2 'wk', 'd')
// Result: 14 'd'

// ========================================
// Concentration Conversions
// ========================================

define "GlucoseMgDLToMgL": ConvertQuantity(180 'mg/dL', 'mg/L')
// Result: 1800 'mg/L'

define "GramPerLiterToMgDL": ConvertQuantity(1 'g/L', 'mg/dL')
// Result: 100 'mg/dL'

// ========================================
// Clinical Calculations Example
// ========================================

// Patient weight in different units
define "PatientWeightLbs": 165 '[lb_av]'
define "PatientWeightKg": ConvertQuantity(PatientWeightLbs, 'kg')

// Patient height in different units
define "PatientHeightInches": 68 '[in_i]'
define "PatientHeightCm": ConvertQuantity(PatientHeightInches, 'cm')
define "PatientHeightMeters": ConvertQuantity(PatientHeightInches, 'm')

// Temperature check
define "FeverThresholdF": 100.4 '[degF]'
define "FeverThresholdC": ConvertQuantity(FeverThresholdF, 'Cel')
