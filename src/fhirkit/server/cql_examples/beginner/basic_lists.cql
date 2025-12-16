library ListExamples version '1.0.0'

/*
 * CQL List Operations
 * -------------------
 * Lists are fundamental in CQL because FHIR data is list-based:
 * - [Condition] returns a LIST of conditions
 * - Patient.name is a LIST of names
 *
 * Lists use curly braces: { 1, 2, 3 }
 */

// Creating lists
define "Number List": { 1, 2, 3, 4, 5 }
define "String List": { 'apple', 'banana', 'cherry' }
define "Empty List": { }

// List information
define "Count": Count({ 1, 2, 3, 4, 5 })   // Result: 5
define "Is Empty": IsEmpty({ })             // Result: true
define "Exists": exists { 1, 2, 3 }         // Result: true

// Accessing elements
define "First": First({ 1, 2, 3, 4, 5 })   // Result: 1
define "Last": Last({ 1, 2, 3, 4, 5 })     // Result: 5
define "By Index": ({ 1, 2, 3, 4, 5 })[2]  // Result: 3 (0-indexed)
define "Take First 3": Take({ 1, 2, 3, 4, 5 }, 3)  // Result: {1,2,3}
define "Skip First 2": Skip({ 1, 2, 3, 4, 5 }, 2)  // Result: {3,4,5}

// Membership testing
define "Contains": 3 in { 1, 2, 3, 4, 5 }           // Result: true
define "Includes All": { 1, 2, 3, 4, 5 } includes { 2, 3 }

// Set operations (removing duplicates)
define "Union": { 1, 2, 3 } union { 3, 4, 5 }       // Result: {1,2,3,4,5}
define "Intersect": { 1, 2, 3, 4 } intersect { 3, 4, 5, 6 }  // Result: {3,4}
define "Except": { 1, 2, 3, 4 } except { 3, 4 }     // Result: {1,2}

// Transforming lists
define "Distinct": distinct { 1, 1, 2, 2, 3, 3 }   // Result: {1,2,3}
define "Flatten": flatten { { 1, 2 }, { 3, 4 } }   // Result: {1,2,3,4}
