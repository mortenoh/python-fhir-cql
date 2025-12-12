/*
 * Type Conversions - Converting between CQL types
 */
library TypeConversions version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// String Conversions
// =====================================================

// ToString - convert various types to string
define IntegerToString: ToString(42)
define DecimalToString: ToString(3.14159)
define BooleanToStringTrue: ToString(true)
define BooleanToStringFalse: ToString(false)
define DateToString: ToString(@2024-06-15)
define DateTimeToString: ToString(@2024-06-15T10:30:00)
define TimeToString: ToString(@T14:30:00)
define QuantityToString: ToString(100 'mg')
define NullToString: ToString(null)

// =====================================================
// Numeric Conversions
// =====================================================

// ToInteger - convert to integer
define StringToInteger: ToInteger('42')
define DecimalToInteger: ToInteger(3.9)
define IntegerToInteger: ToInteger(42)
define InvalidStringToInteger: ToInteger('not a number')

// ToDecimal - convert to decimal
define StringToDecimal: ToDecimal('3.14159')
define IntegerToDecimal: ToDecimal(42)
define DecimalToDecimal: ToDecimal(3.14)
define InvalidStringToDecimal: ToDecimal('invalid')

// ToLong - convert to long integer
define StringToLong: ToLong('9999999999')
define IntegerToLong: ToLong(42)

// =====================================================
// Boolean Conversions
// =====================================================

// ToBoolean - convert to boolean
define StringTrueToBoolean: ToBoolean('true')
define StringFalseToBoolean: ToBoolean('false')
define StringYToBoolean: ToBoolean('y')
define StringNToBoolean: ToBoolean('n')
define StringYesBoolean: ToBoolean('yes')
define StringNoBoolean: ToBoolean('no')
define String1ToBoolean: ToBoolean('1')
define String0ToBoolean: ToBoolean('0')
define IntegerOneToBoolean: ToBoolean(1)
define IntegerZeroToBoolean: ToBoolean(0)
define InvalidToBoolean: ToBoolean('maybe')

// =====================================================
// Date/Time Conversions
// =====================================================

// ToDate - convert to Date
define StringToDate: ToDate('2024-06-15')
define DateTimeToDate: ToDate(@2024-06-15T10:30:00)
define PartialDateToDate: ToDate('2024-06')
define InvalidStringToDate: ToDate('not a date')

// ToDateTime - convert to DateTime
define StringToDateTime: ToDateTime('2024-06-15T10:30:00')
define DateToDateTime: ToDateTime(@2024-06-15)
define PartialToDateTime: ToDateTime('2024-06-15T10:30')

// ToTime - convert to Time
define StringToTime: ToTime('14:30:00')
define TimeToTime: ToTime(@T14:30:00)

// =====================================================
// Quantity Conversions
// =====================================================

// ToQuantity - convert to Quantity
define IntegerToQuantity: ToQuantity(100)
define DecimalToQuantity: ToQuantity(3.14)
define StringToQuantity: ToQuantity('100 mg')

// =====================================================
// Type Checking
// =====================================================

// Check value types
define IsIntegerTrue: 42 is Integer
define IsIntegerFalse: 3.14 is Integer
define IsDecimalTrue: 3.14 is Decimal
define IsStringTrue: 'hello' is String
define IsBooleanTrue: true is Boolean
define IsDateTrue: @2024-06-15 is Date
define IsListTrue: {1, 2, 3} is List<Integer>

// =====================================================
// Type Casting
// =====================================================

// Cast expressions
define CastToInteger: 3.9 as Integer
define CastToDecimal: 42 as Decimal
define CastToString: 123 as String

// Safe casting with null on failure
define SafeCastValid: 'hello' as String
define SafeCastInvalid: 'hello' as Integer

// =====================================================
// Implicit Conversions
// =====================================================

// Integer to Decimal (implicit in arithmetic)
define ImplicitIntToDecimal: 5 + 3.14

// String concatenation
define ImplicitStringConcat: 'Value: ' + ToString(42)

// =====================================================
// Null Handling in Conversions
// =====================================================

define NullConversion: ToInteger(null)
define NullCheck: if null is null then 'null' else 'not null'
define CoalesceConversion: Coalesce(ToInteger(null), ToInteger('invalid'), 0)

// =====================================================
// Collection Type Conversions
// =====================================================

// Convert single value to list
define SingleToList: {42}
define SingletonFrom: singleton from {42}

// Flatten nested lists
define FlattenLists: Flatten({{1, 2}, {3, 4}})

// =====================================================
// FHIR Type Conversions
// =====================================================

context Patient

// Convert FHIR string to CQL string
define PatientGender: Patient.gender as String

// Convert FHIR date to CQL date
define PatientBirthDate: Patient.birthDate as Date

// Extract value from Quantity
define function GetQuantityValue(q FHIR.Quantity) returns Decimal:
    q.value

define function GetQuantityUnit(q FHIR.Quantity) returns String:
    q.unit

// =====================================================
// Practical Conversion Functions
// =====================================================

// Safe integer parsing with default
define function SafeParseInt(s String, defaultVal Integer) returns Integer:
    Coalesce(ToInteger(s), defaultVal)

// Safe decimal parsing with default
define function SafeParseDecimal(s String, defaultVal Decimal) returns Decimal:
    Coalesce(ToDecimal(s), defaultVal)

// Safe boolean parsing
define function SafeParseBool(s String, defaultVal Boolean) returns Boolean:
    Coalesce(ToBoolean(Lower(Trim(s))), defaultVal)

// Parse date with fallback to current date
define function SafeParseDate(s String) returns Date:
    Coalesce(ToDate(s), Today())

// Format number with precision
define function FormatNumber(value Decimal, precision Integer) returns String:
    ToString(Round(value, precision))

// Format as percentage
define function FormatPercentage(value Decimal) returns String:
    ToString(Round(value * 100, 1)) + '%'

// Parse quantity from string (value unit)
define function ParseQuantity(s String) returns System.Quantity:
    ToQuantity(s)

// =====================================================
// Test Examples
// =====================================================

define TestSafeParseInt: SafeParseInt('42', 0)
define TestSafeParseIntInvalid: SafeParseInt('invalid', -1)
define TestFormatNumber: FormatNumber(3.14159, 2)
define TestFormatPercentage: FormatPercentage(0.756)
