/*
 * String Functions - Comprehensive string manipulation in CQL
 */
library StringFunctions version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// Basic String Operations
// =====================================================

// Concatenation
define ConcatExample: 'Hello' + ' ' + 'World'
define ConcatWithConcat: Concat('Hello', ', ', 'World', '!')

// Combine (join list of strings with separator)
define Words: {'apple', 'banana', 'cherry'}
define CombineWithComma: Combine(Words, ', ')
define CombineNoSeparator: Combine({'x', 'y', 'z'})

// Split
define SplitByComma: Split('a,b,c,d', ',')
define SplitBySpace: Split('Hello World CQL', ' ')

// =====================================================
// Case Conversion
// =====================================================

define UpperCase: Upper('hello world')
define LowerCase: Lower('HELLO WORLD')
define MixedCase: Upper('Hello') + ' ' + Lower('WORLD')

// =====================================================
// Substring Operations
// =====================================================

define SubstringFromStart: Substring('Hello World', 0, 5)
define SubstringFromMiddle: Substring('Hello World', 6, 5)
define SubstringToEnd: Substring('Hello World', 6)

// =====================================================
// Search and Position
// =====================================================

define IndexOfFound: IndexOf('Hello World', 'World')
define IndexOfNotFound: IndexOf('Hello World', 'xyz')
define PositionOfFound: PositionOf('l', 'Hello')

// =====================================================
// Prefix and Suffix
// =====================================================

define StartsWithTrue: StartsWith('Hello World', 'Hello')
define StartsWithFalse: StartsWith('Hello World', 'World')
define EndsWithTrue: EndsWith('Hello World', 'World')
define EndsWithFalse: EndsWith('Hello World', 'Hello')

// =====================================================
// Pattern Matching
// =====================================================

define MatchesDigits: Matches('12345', '\\d+')
define MatchesEmail: Matches('user@example.com', '.*@.*\\..*')
define MatchesFails: Matches('hello', '\\d+')

// =====================================================
// Replace Operations
// =====================================================

define ReplaceSimple: Replace('Hello World', 'World', 'CQL')
define ReplaceMultiple: Replace('banana', 'a', 'o')
define ReplaceMatchesRegex: ReplaceMatches('abc123def456', '\\d+', 'X')

// =====================================================
// Trim and Length
// =====================================================

define TrimSpaces: Trim('  Hello World  ')
define TrimAlreadyClean: Trim('Hello')
define StringLength: Length('Hello World')
define EmptyLength: Length('')

// =====================================================
// Null Handling
// =====================================================

define NullConcat: 'Hello' + null
define CoalesceStrings: Coalesce(null, null, 'Default')
define NullLength: Length(null)

// =====================================================
// Practical Examples
// =====================================================

// Format a patient name
define function FormatPatientName(given String, family String, suffix String) returns String:
    Coalesce(given, '') + ' ' + Coalesce(family, '') +
    (if suffix is not null then ', ' + suffix else '')

// Parse a code from display text (extract code in parentheses)
define function ExtractCodeFromDisplay(display String) returns String:
    if display is null then null
    else Substring(display, IndexOf(display, '(') + 1,
                   IndexOf(display, ')') - IndexOf(display, '(') - 1)

// Sanitize string for search
define function SanitizeForSearch(input String) returns String:
    Lower(Trim(ReplaceMatches(input, '[^a-zA-Z0-9 ]', '')))
