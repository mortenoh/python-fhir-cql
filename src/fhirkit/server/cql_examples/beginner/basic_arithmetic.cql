library ArithmeticExamples version '1.0.0'

/*
 * CQL Arithmetic Operations
 * -------------------------
 * CQL supports standard math operations plus useful
 * functions for clinical calculations like BMI, eGFR, etc.
 *
 * Try modifying values to see how results change!
 */

// Basic operators: +, -, *, /
define "Addition": 5 + 3           // Result: 8
define "Subtraction": 10 - 4       // Result: 6
define "Multiplication": 6 * 7     // Result: 42
define "Division": 20 / 4          // Result: 5.0 (decimal)

// Integer operations
define "Integer Division": 20 div 3  // Result: 6 (whole number only)
define "Modulo": 17 mod 5            // Result: 2 (remainder)
define "Power": 2 ^ 10               // Result: 1024

// Useful math functions
define "Absolute Value": Abs(-15)    // Result: 15
define "Ceiling": Ceiling(4.2)       // Result: 5 (round up)
define "Floor": Floor(4.8)           // Result: 4 (round down)
define "Round": Round(3.567, 2)      // Result: 3.57 (2 decimals)

// Aggregate functions (work on lists)
define "Minimum": Min({ 3, 1, 4, 1, 5 })   // Result: 1
define "Maximum": Max({ 3, 1, 4, 1, 5 })   // Result: 5
define "Sum": Sum({ 1, 2, 3, 4, 5 })       // Result: 15
define "Average": Avg({ 1, 2, 3, 4, 5 })   // Result: 3.0
