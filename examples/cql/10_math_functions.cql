/*
 * Math Functions - Mathematical operations in CQL
 */
library MathFunctions version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// Basic Arithmetic
// =====================================================

define Addition: 10 + 5
define Subtraction: 10 - 5
define Multiplication: 10 * 5
define Division: 10.0 / 3.0
define IntegerDivision: 10 div 3
define Modulo: 10 mod 3

// =====================================================
// Sign and Absolute Value
// =====================================================

define AbsPositive: Abs(42)
define AbsNegative: Abs(-42)
define AbsDecimal: Abs(-3.14)

// =====================================================
// Rounding Functions
// =====================================================

define CeilingExample: Ceiling(3.2)
define CeilingNegative: Ceiling(-3.2)
define FloorExample: Floor(3.8)
define FloorNegative: Floor(-3.2)
define TruncatePositive: Truncate(3.9)
define TruncateNegative: Truncate(-3.9)

// Round with precision
define RoundDefault: Round(3.5)
define RoundToOne: Round(3.456, 1)
define RoundToTwo: Round(3.456, 2)
define RoundBankersEven: Round(2.5)

// =====================================================
// Power and Roots
// =====================================================

define SquareRoot: Sqrt(16)
define SquareRootDecimal: Sqrt(2.0)
define PowerSquare: Power(2, 3)
define PowerFraction: Power(4, 0.5)

// =====================================================
// Logarithms and Exponentials
// =====================================================

define NaturalLog: Ln(2.71828)
define LogE: Exp(1)
define LogBase10: Log(100, 10)

// =====================================================
// Min/Max
// =====================================================

define MinOfTwo: Min(5, 3)
define MaxOfTwo: Max(5, 3)
define MinList: Min({3, 1, 4, 1, 5, 9})
define MaxList: Max({3, 1, 4, 1, 5, 9})

// =====================================================
// Predecessor and Successor
// =====================================================

define PredecessorInt: predecessor of 5
define SuccessorInt: successor of 5
define PredecessorDecimal: predecessor of 5.0
define SuccessorDecimal: successor of 5.0

// =====================================================
// Practical Examples
// =====================================================

// Calculate BMI
define function CalculateBMI(weightKg Decimal, heightM Decimal) returns Decimal:
    if heightM is null or heightM = 0 or weightKg is null then null
    else Round(weightKg / Power(heightM, 2), 1)

// Temperature conversion
define function CelsiusToFahrenheit(celsius Decimal) returns Decimal:
    Round(celsius * 9.0 / 5.0 + 32, 1)

define function FahrenheitToCelsius(fahrenheit Decimal) returns Decimal:
    Round((fahrenheit - 32) * 5.0 / 9.0, 1)

// eGFR calculation (simplified CKD-EPI)
define function CalculateEGFR(creatinine Decimal, age Integer, isFemale Boolean) returns Integer:
    Truncate(
        141 * Power(Min(creatinine / (if isFemale then 0.7 else 0.9), 1.0),
                    if isFemale then -0.329 else -0.411)
            * Power(Max(creatinine / (if isFemale then 0.7 else 0.9), 1.0), -1.209)
            * Power(0.993, age)
            * (if isFemale then 1.018 else 1.0)
    )

// Percentage calculation
define function CalculatePercentage(part Decimal, whole Decimal) returns Decimal:
    if whole is null or whole = 0 then null
    else Round(part / whole * 100, 2)

// Helper for variance calculation
define function SquaredDifference(value Decimal, mean Decimal) returns Decimal:
    Power(value - mean, 2)

// Statistical examples
define SampleData: {1.0, 2.0, 3.0, 4.0, 5.0}
define SampleMean: Avg(SampleData)
define SampleSum: Sum(SampleData)
define SampleMin: Min(SampleData)
define SampleMax: Max(SampleData)

// Test calculations
define TestBMI: CalculateBMI(70.0, 1.75)
define TestCelsiusToF: CelsiusToFahrenheit(37.0)
define TestFahrenheitToC: FahrenheitToCelsius(98.6)
define TestPercentage: CalculatePercentage(75.0, 100.0)
