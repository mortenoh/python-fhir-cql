library StringExamples version '1.0.0'

/*
 * CQL String Operations
 * ---------------------
 * Strings in CQL use single quotes: 'Hello'
 * These functions are useful for searching patient names,
 * parsing codes, and formatting display text.
 */

// Creating and combining strings
define "Simple String": 'Hello, World!'
define "Concatenation": 'Hello' + ', ' + 'World!'

// Getting string information
define "Length": Length('Hello')                    // Result: 5
define "Position Of": PositionOf('World', 'Hello World')  // Result: 6

// Case conversion (useful for case-insensitive matching)
define "Upper Case": Upper('hello')                 // Result: 'HELLO'
define "Lower Case": Lower('HELLO')                 // Result: 'hello'

// Extracting parts of strings
define "Substring": Substring('Hello World', 0, 5) // Result: 'Hello'

// Checking string content
define "Starts With": StartsWith('Hello World', 'Hello')  // Result: true
define "Ends With": EndsWith('Hello World', 'World')      // Result: true
define "Contains": PositionOf('World', 'Hello World') >= 0

// Modifying strings
define "Replace": Replace('Hello World', 'World', 'CQL')

// Working with delimited data
define "Split": Split('a,b,c,d', ',')              // Result: ['a','b','c','d']
define "Combine": Combine({ 'a', 'b', 'c' }, '-')  // Result: 'a-b-c'

// Comparison (alphabetical ordering)
define "String Equality": 'abc' = 'abc'            // Result: true
define "String Compare": 'apple' < 'banana'        // Result: true
