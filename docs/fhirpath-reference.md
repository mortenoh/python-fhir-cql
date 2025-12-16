# FHIRPath Reference

Complete reference for all FHIRPath functions and operators supported in FHIRKit.

---

## Quick Reference

| Category | Functions |
|----------|-----------|
| [Existence](#existence-functions) | exists, empty, count, all, allTrue, anyTrue, allFalse, anyFalse, hasValue |
| [Subsetting](#subsetting-functions) | first, last, tail, take, skip, single |
| [Filtering](#filtering-functions) | where, select, repeat, ofType |
| [Navigation](#navigation-functions) | children, descendants |
| [String](#string-functions) | startsWith, endsWith, contains, matches, replace, replaceMatches, length, substring, upper, lower, trim, split, join, indexOf, toChars, encode, decode |
| [Math](#math-functions) | abs, ceiling, floor, round, truncate, sqrt, ln, log, power, exp |
| [Date/Time](#datetime-functions) | today, now, timeOfDay |
| [Type Conversion](#type-conversion-functions) | toBoolean, toInteger, toDecimal, toString, toDate, toDateTime, toTime, toQuantity |
| [Type Testing](#type-testing-functions) | convertsToBoolean, convertsToInteger, convertsToDecimal, convertsToString, convertsToDate, convertsToDateTime, convertsToTime, convertsToQuantity |
| [Boolean Logic](#boolean-logic-functions) | not, iif, trace |
| [Comparison](#comparison-operators) | =, !=, ~, !~, <, >, <=, >= |
| [Collections](#collection-functions) | distinct, isDistinct, union, intersect, exclude, combine, flatten, subsetOf, supersetOf |
| [FHIR-Specific](#fhir-specific-functions) | resolve, extension, conformsTo, memberOf, subsumes, subsumedBy |

---

## Existence Functions

Functions for testing the existence and state of collections.

### exists()

Returns `true` if the collection has any elements.

```
collection.exists() : Boolean
collection.exists(criteria) : Boolean
```

**Examples:**
```fhirpath
Patient.name.exists()                    // true if patient has any names
Patient.name.where(use = 'official').exists()  // true if has official name
Patient.telecom.exists(system = 'phone')  // true if has phone contact
```

### empty()

Returns `true` if the collection is empty.

```
collection.empty() : Boolean
```

**Examples:**
```fhirpath
Patient.deceased.empty()     // true if deceased element not present
{}.empty()                   // true
{1, 2, 3}.empty()           // false
```

### count()

Returns the number of elements in the collection.

```
collection.count() : Integer
```

**Examples:**
```fhirpath
Patient.name.count()         // number of names
Patient.telecom.count()      // number of contact points
{1, 2, 3}.count()           // 3
{}.count()                  // 0
```

### all()

Returns `true` if all elements in the collection satisfy the criteria.

```
collection.all(criteria) : Boolean
```

**Examples:**
```fhirpath
Patient.telecom.all(system.exists())  // true if all contacts have system
{1, 2, 3}.all($this > 0)              // true (all positive)
{1, -1, 2}.all($this > 0)             // false
```

### allTrue()

Returns `true` if all items in the collection are `true`.

```
collection.allTrue() : Boolean
```

**Examples:**
```fhirpath
{true, true, true}.allTrue()    // true
{true, false, true}.allTrue()   // false
{}.allTrue()                    // true (vacuously true)
```

### anyTrue()

Returns `true` if any item in the collection is `true`.

```
collection.anyTrue() : Boolean
```

**Examples:**
```fhirpath
{false, true, false}.anyTrue()   // true
{false, false, false}.anyTrue()  // false
{}.anyTrue()                     // false
```

### allFalse()

Returns `true` if all items in the collection are `false`.

```
collection.allFalse() : Boolean
```

**Examples:**
```fhirpath
{false, false, false}.allFalse()  // true
{false, true, false}.allFalse()   // false
{}.allFalse()                     // true (vacuously true)
```

### anyFalse()

Returns `true` if any item in the collection is `false`.

```
collection.anyFalse() : Boolean
```

**Examples:**
```fhirpath
{true, false, true}.anyFalse()   // true
{true, true, true}.anyFalse()    // false
{}.anyFalse()                    // false
```

### hasValue()

Returns `true` if the input collection has a single value that is not null.

```
singleton.hasValue() : Boolean
```

**Examples:**
```fhirpath
Patient.birthDate.hasValue()     // true if birthDate exists and has value
(5).hasValue()                   // true
{}.hasValue()                    // false
```

---

## Subsetting Functions

Functions for extracting subsets of collections.

### first()

Returns the first element of the collection.

```
collection.first() : Element
```

**Examples:**
```fhirpath
Patient.name.first()              // first name
{1, 2, 3}.first()                // 1
{}.first()                       // {} (empty)
```

### last()

Returns the last element of the collection.

```
collection.last() : Element
```

**Examples:**
```fhirpath
Patient.name.last()               // last name
{1, 2, 3}.last()                 // 3
{}.last()                        // {} (empty)
```

### tail()

Returns all but the first element of the collection.

```
collection.tail() : Collection
```

**Examples:**
```fhirpath
{1, 2, 3, 4}.tail()              // {2, 3, 4}
{1}.tail()                       // {}
{}.tail()                        // {}
```

### take(num)

Returns the first `num` elements of the collection.

```
collection.take(num : Integer) : Collection
```

**Examples:**
```fhirpath
{1, 2, 3, 4, 5}.take(3)          // {1, 2, 3}
{1, 2}.take(5)                   // {1, 2}
{}.take(3)                       // {}
```

### skip(num)

Returns all elements except the first `num`.

```
collection.skip(num : Integer) : Collection
```

**Examples:**
```fhirpath
{1, 2, 3, 4, 5}.skip(2)          // {3, 4, 5}
{1, 2}.skip(5)                   // {}
{}.skip(3)                       // {}
```

### single()

Returns the single element if collection has exactly one, otherwise empty.

```
collection.single() : Element
```

**Examples:**
```fhirpath
{5}.single()                     // 5
{1, 2}.single()                  // {} (error/empty - not single)
{}.single()                      // {} (empty)
Patient.birthDate.single()       // the birthDate if present
```

---

## Filtering Functions

Functions for filtering and transforming collections.

### where(criteria)

Filters collection to elements matching the criteria.

```
collection.where(criteria) : Collection
```

**Examples:**
```fhirpath
Patient.name.where(use = 'official')
Patient.telecom.where(system = 'phone')
{1, 2, 3, 4, 5}.where($this > 3)      // {4, 5}
Observation.component.where(code.coding.code = '8480-6')
```

### select(projection)

Projects each element through an expression, flattening the result.

```
collection.select(projection) : Collection
```

**Examples:**
```fhirpath
Patient.name.select(given)                    // all given names flattened
Patient.telecom.select(value)                 // all contact values
{1, 2, 3}.select($this * 2)                  // {2, 4, 6}
```

### repeat(expression)

Repeatedly evaluates expression on each item until no new items are produced.

```
collection.repeat(expression) : Collection
```

**Examples:**
```fhirpath
// Navigate through all extensions recursively
Patient.repeat(extension)

// Get all descendants (alternative to descendants())
resource.repeat(children())
```

### ofType(type)

Filters to elements of the specified type.

```
collection.ofType(type) : Collection
```

**Examples:**
```fhirpath
Bundle.entry.resource.ofType(Patient)         // all Patient resources
Bundle.entry.resource.ofType(Observation)     // all Observations
Observation.value.ofType(Quantity)            // value if it's a Quantity
```

---

## Navigation Functions

Functions for navigating resource structure.

### children()

Returns all immediate child nodes.

```
collection.children() : Collection
```

**Examples:**
```fhirpath
Patient.children()              // all immediate children of Patient
Patient.name.children()         // all parts of all names
```

### descendants()

Returns all descendant nodes recursively.

```
collection.descendants() : Collection
```

**Examples:**
```fhirpath
Patient.descendants()           // all nested elements
Bundle.descendants().ofType(Observation)  // all Observations anywhere
```

---

## String Functions

Functions for string manipulation.

### startsWith(prefix)

Returns `true` if string starts with prefix.

```
string.startsWith(prefix : String) : Boolean
```

**Examples:**
```fhirpath
'Hello World'.startsWith('Hello')     // true
'Hello World'.startsWith('World')     // false
Patient.name.family.startsWith('Sm')  // true for 'Smith'
```

### endsWith(suffix)

Returns `true` if string ends with suffix.

```
string.endsWith(suffix : String) : Boolean
```

**Examples:**
```fhirpath
'Hello World'.endsWith('World')       // true
'test.json'.endsWith('.json')         // true
```

### contains(substring)

Returns `true` if string contains the substring.

```
string.contains(substring : String) : Boolean
```

**Examples:**
```fhirpath
'Hello World'.contains('lo Wo')       // true
Patient.name.text.contains('John')    // true if name contains 'John'
```

### matches(regex)

Returns `true` if string matches the regular expression.

```
string.matches(regex : String) : Boolean
```

**Examples:**
```fhirpath
'test@email.com'.matches('.*@.*\\.com')  // true
'12345'.matches('^\\d+$')                 // true (all digits)
Patient.telecom.value.matches('^\\+?\\d{10,}$')  // phone pattern
```

### replace(pattern, replacement)

Replaces first occurrence of pattern with replacement.

```
string.replace(pattern : String, replacement : String) : String
```

**Examples:**
```fhirpath
'Hello World'.replace('World', 'FHIRPath')  // 'Hello FHIRPath'
'foo-bar-baz'.replace('-', '_')              // 'foo_bar-baz'
```

### replaceMatches(regex, replacement)

Replaces all regex matches with replacement.

```
string.replaceMatches(regex : String, replacement : String) : String
```

**Examples:**
```fhirpath
'Hello123World456'.replaceMatches('\\d+', 'X')  // 'HelloXWorldX'
'a-b-c'.replaceMatches('-', '_')                 // 'a_b_c'
```

### length()

Returns the length of the string.

```
string.length() : Integer
```

**Examples:**
```fhirpath
'Hello'.length()              // 5
''.length()                   // 0
Patient.name.family.length()  // length of family name
```

### substring(start, length?)

Returns substring starting at index with optional length.

```
string.substring(start : Integer, length? : Integer) : String
```

**Examples:**
```fhirpath
'Hello World'.substring(0, 5)     // 'Hello'
'Hello World'.substring(6)        // 'World'
'Hello'.substring(1, 3)           // 'ell'
```

### upper()

Converts string to uppercase.

```
string.upper() : String
```

**Examples:**
```fhirpath
'Hello World'.upper()             // 'HELLO WORLD'
```

### lower()

Converts string to lowercase.

```
string.lower() : String
```

**Examples:**
```fhirpath
'Hello World'.lower()             // 'hello world'
```

### trim()

Removes leading and trailing whitespace.

```
string.trim() : String
```

**Examples:**
```fhirpath
'  Hello  '.trim()                // 'Hello'
```

### split(separator)

Splits string into a collection.

```
string.split(separator : String) : Collection
```

**Examples:**
```fhirpath
'a,b,c'.split(',')                // {'a', 'b', 'c'}
'Hello World'.split(' ')          // {'Hello', 'World'}
```

### join(separator?)

Joins collection of strings with separator.

```
collection.join(separator? : String) : String
```

**Examples:**
```fhirpath
{'a', 'b', 'c'}.join(',')         // 'a,b,c'
{'a', 'b', 'c'}.join()            // 'abc'
Patient.name.given.join(' ')      // 'John Michael'
```

### indexOf(substring)

Returns index of first occurrence of substring (-1 if not found).

```
string.indexOf(substring : String) : Integer
```

**Examples:**
```fhirpath
'Hello World'.indexOf('World')    // 6
'Hello World'.indexOf('xyz')      // -1
```

### toChars()

Converts string to collection of characters.

```
string.toChars() : Collection
```

**Examples:**
```fhirpath
'abc'.toChars()                   // {'a', 'b', 'c'}
```

### encode(encoding) / decode(encoding)

Encodes/decodes string using specified encoding (base64, urlbase64, hex).

```
string.encode(encoding : String) : String
string.decode(encoding : String) : String
```

**Examples:**
```fhirpath
'Hello'.encode('base64')          // 'SGVsbG8='
'SGVsbG8='.decode('base64')       // 'Hello'
```

---

## Math Functions

Mathematical functions.

### abs()

Returns absolute value.

```
number.abs() : Number
```

**Examples:**
```fhirpath
(-5).abs()                        // 5
(5).abs()                         // 5
```

### ceiling()

Returns smallest integer >= value.

```
number.ceiling() : Integer
```

**Examples:**
```fhirpath
(4.2).ceiling()                   // 5
(4.8).ceiling()                   // 5
(-4.2).ceiling()                  // -4
```

### floor()

Returns largest integer <= value.

```
number.floor() : Integer
```

**Examples:**
```fhirpath
(4.2).floor()                     // 4
(4.8).floor()                     // 4
(-4.2).floor()                    // -5
```

### round(precision?)

Rounds to specified precision (default 0).

```
number.round(precision? : Integer) : Number
```

**Examples:**
```fhirpath
(3.14159).round()                 // 3
(3.14159).round(2)                // 3.14
(3.145).round(2)                  // 3.15
```

### truncate()

Truncates decimal portion.

```
number.truncate() : Integer
```

**Examples:**
```fhirpath
(4.8).truncate()                  // 4
(-4.8).truncate()                 // -4
```

### sqrt()

Returns square root.

```
number.sqrt() : Decimal
```

**Examples:**
```fhirpath
(16).sqrt()                       // 4.0
(2).sqrt()                        // 1.414...
```

### ln()

Returns natural logarithm.

```
number.ln() : Decimal
```

**Examples:**
```fhirpath
(2.71828).ln()                    // ~1.0
(10).ln()                         // ~2.302
```

### log(base)

Returns logarithm to specified base.

```
number.log(base : Number) : Decimal
```

**Examples:**
```fhirpath
(100).log(10)                     // 2.0
(8).log(2)                        // 3.0
```

### power(exponent)

Returns number raised to exponent.

```
number.power(exponent : Number) : Number
```

**Examples:**
```fhirpath
(2).power(8)                      // 256
(3).power(2)                      // 9
```

### exp()

Returns e raised to the power of the number.

```
number.exp() : Decimal
```

**Examples:**
```fhirpath
(1).exp()                         // ~2.718
(0).exp()                         // 1.0
```

---

## Date/Time Functions

Functions for date and time operations.

### today()

Returns the current date.

```
today() : Date
```

**Examples:**
```fhirpath
today()                           // @2024-12-16
Patient.birthDate < today()       // true if born before today
```

### now()

Returns the current date and time with timezone.

```
now() : DateTime
```

**Examples:**
```fhirpath
now()                             // @2024-12-16T10:30:00Z
Observation.effectiveDateTime < now()
```

### timeOfDay()

Returns the current time.

```
timeOfDay() : Time
```

**Examples:**
```fhirpath
timeOfDay()                       // @T10:30:00
```

---

## Type Conversion Functions

Functions for converting between types.

### toBoolean()

Converts to boolean.

```
value.toBoolean() : Boolean
```

**Conversion rules:**
- `true`, `'true'`, `'t'`, `'yes'`, `'y'`, `'1'`, `1`, `1.0` -> `true`
- `false`, `'false'`, `'f'`, `'no'`, `'n'`, `'0'`, `0`, `0.0` -> `false`

**Examples:**
```fhirpath
'true'.toBoolean()                // true
(1).toBoolean()                   // true
'yes'.toBoolean()                 // true
```

### toInteger()

Converts to integer.

```
value.toInteger() : Integer
```

**Examples:**
```fhirpath
'42'.toInteger()                  // 42
(3.0).toInteger()                 // 3
true.toInteger()                  // 1
```

### toDecimal()

Converts to decimal.

```
value.toDecimal() : Decimal
```

**Examples:**
```fhirpath
'3.14'.toDecimal()                // 3.14
(42).toDecimal()                  // 42.0
```

### toString()

Converts to string.

```
value.toString() : String
```

**Examples:**
```fhirpath
(42).toString()                   // '42'
true.toString()                   // 'true'
```

### toDate()

Converts to date.

```
value.toDate() : Date
```

**Examples:**
```fhirpath
'2024-12-16'.toDate()             // @2024-12-16
'2024-12-16T10:30:00Z'.toDate()   // @2024-12-16
```

### toDateTime()

Converts to datetime.

```
value.toDateTime() : DateTime
```

**Examples:**
```fhirpath
'2024-12-16'.toDateTime()         // @2024-12-16
'2024-12-16T10:30:00Z'.toDateTime()  // @2024-12-16T10:30:00Z
```

### toTime()

Converts to time.

```
value.toTime() : Time
```

**Examples:**
```fhirpath
'10:30:00'.toTime()               // @T10:30:00
```

### toQuantity(unit?)

Converts to quantity.

```
value.toQuantity(unit? : String) : Quantity
```

**Examples:**
```fhirpath
'5 kg'.toQuantity()               // 5 'kg'
(70).toQuantity('kg')             // 70 'kg'
```

---

## Type Testing Functions

Functions for testing if conversion is possible.

### convertsToBoolean()

Returns `true` if value can be converted to boolean.

```
value.convertsToBoolean() : Boolean
```

### convertsToInteger()

Returns `true` if value can be converted to integer.

```
value.convertsToInteger() : Boolean
```

### convertsToDecimal()

Returns `true` if value can be converted to decimal.

```
value.convertsToDecimal() : Boolean
```

### convertsToString()

Returns `true` if value can be converted to string.

```
value.convertsToString() : Boolean
```

### convertsToDate()

Returns `true` if value can be converted to date.

```
value.convertsToDate() : Boolean
```

### convertsToDateTime()

Returns `true` if value can be converted to datetime.

```
value.convertsToDateTime() : Boolean
```

### convertsToTime()

Returns `true` if value can be converted to time.

```
value.convertsToTime() : Boolean
```

### convertsToQuantity()

Returns `true` if value can be converted to quantity.

```
value.convertsToQuantity() : Boolean
```

---

## Boolean Logic Functions

### not()

Returns boolean negation.

```
boolean.not() : Boolean
```

**Examples:**
```fhirpath
true.not()                        // false
false.not()                       // true
Patient.active.not()              // negation of active status
```

### iif(true-result, otherwise-result?)

If-then-else conditional.

```
condition.iif(true-result, otherwise-result?) : Any
```

**Examples:**
```fhirpath
(5 > 3).iif('yes', 'no')          // 'yes'
Patient.active.iif('Active', 'Inactive')
Patient.deceased.exists().iif('Deceased', 'Alive')
```

### trace(name, projection?)

Logs collection for debugging, returns unchanged.

```
collection.trace(name : String, projection?) : Collection
```

**Examples:**
```fhirpath
Patient.name.trace('names')       // logs and returns names
```

---

## Comparison Operators

### Equality (=, !=)

Test equality/inequality.

```
left = right : Boolean
left != right : Boolean
```

**Examples:**
```fhirpath
5 = 5                             // true
'hello' = 'hello'                 // true
5 != 3                            // true
Patient.gender = 'male'           // true if male
```

### Equivalence (~, !~)

Test equivalence (case-insensitive for strings, empty = empty).

```
left ~ right : Boolean
left !~ right : Boolean
```

**Examples:**
```fhirpath
'Hello' ~ 'HELLO'                 // true (case-insensitive)
{} ~ {}                           // true (both empty)
5 ~ 5.0                           // true
```

### Comparison (<, >, <=, >=)

Compare ordered values.

```
left < right : Boolean
left > right : Boolean
left <= right : Boolean
left >= right : Boolean
```

**Examples:**
```fhirpath
5 < 10                            // true
'apple' < 'banana'                // true (lexicographic)
@2024-01-01 < @2024-12-31         // true
Patient.birthDate < @1990-01-01   // born before 1990
```

---

## Collection Functions

Functions for set operations on collections.

### distinct()

Returns collection with duplicates removed.

```
collection.distinct() : Collection
```

**Examples:**
```fhirpath
{1, 2, 2, 3, 3, 3}.distinct()     // {1, 2, 3}
Patient.name.given.distinct()     // unique given names
```

### isDistinct()

Returns `true` if all elements are unique.

```
collection.isDistinct() : Boolean
```

**Examples:**
```fhirpath
{1, 2, 3}.isDistinct()            // true
{1, 2, 2}.isDistinct()            // false
```

### union(other)

Returns union of two collections (with duplicates removed).

```
collection.union(other : Collection) : Collection
```

**Examples:**
```fhirpath
{1, 2, 3}.union({2, 3, 4})        // {1, 2, 3, 4}
```

### intersect(other)

Returns intersection of two collections.

```
collection.intersect(other : Collection) : Collection
```

**Examples:**
```fhirpath
{1, 2, 3}.intersect({2, 3, 4})    // {2, 3}
```

### exclude(other)

Returns elements not in other collection.

```
collection.exclude(other : Collection) : Collection
```

**Examples:**
```fhirpath
{1, 2, 3, 4}.exclude({2, 4})      // {1, 3}
```

### combine(other)

Combines collections (preserves duplicates).

```
collection.combine(other : Collection) : Collection
```

**Examples:**
```fhirpath
{1, 2}.combine({2, 3})            // {1, 2, 2, 3}
```

### flatten()

Flattens nested collections.

```
collection.flatten() : Collection
```

**Examples:**
```fhirpath
{{1, 2}, {3, 4}}.flatten()        // {1, 2, 3, 4}
Bundle.entry.resource.flatten()
```

### subsetOf(other)

Returns `true` if all elements are in other collection.

```
collection.subsetOf(other : Collection) : Boolean
```

**Examples:**
```fhirpath
{1, 2}.subsetOf({1, 2, 3, 4})     // true
{1, 5}.subsetOf({1, 2, 3, 4})     // false
```

### supersetOf(other)

Returns `true` if collection contains all elements of other.

```
collection.supersetOf(other : Collection) : Boolean
```

**Examples:**
```fhirpath
{1, 2, 3, 4}.supersetOf({1, 2})   // true
{1, 2, 3, 4}.supersetOf({1, 5})   // false
```

---

## FHIR-Specific Functions

Functions specific to FHIR resources.

### resolve()

Resolves FHIR References to their target resources.

```
reference.resolve() : Resource
```

**Examples:**
```fhirpath
Observation.subject.resolve()     // resolves to Patient resource
MedicationRequest.medication.resolve()  // resolves to Medication
```

### extension(url)

Returns extensions with the specified URL.

```
element.extension(url : String) : Collection
```

**Examples:**
```fhirpath
Patient.extension('http://hl7.org/fhir/StructureDefinition/patient-birthPlace')
Observation.extension('http://example.org/ext/certainty')
```

### conformsTo(profile)

Returns `true` if resource conforms to the specified profile.

```
resource.conformsTo(profile : String) : Boolean
```

**Examples:**
```fhirpath
Patient.conformsTo('http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient')
Observation.conformsTo('http://hl7.org/fhir/StructureDefinition/vitalsigns')
```

### memberOf(valueset)

Returns `true` if code is in the specified ValueSet.

```
code.memberOf(valueset : String) : Boolean
```

**Examples:**
```fhirpath
Observation.code.memberOf('http://hl7.org/fhir/ValueSet/observation-vitalsignresult')
Condition.code.memberOf('http://example.org/ValueSet/diabetes-codes')
```

### subsumes(code) / subsumedBy(code)

Tests subsumption relationships between codes.

```
code.subsumes(other) : Boolean
code.subsumedBy(other) : Boolean
```

**Examples:**
```fhirpath
// Check if condition code is a subtype of diabetes
Condition.code.subsumedBy(%diabetes)
```

### htmlChecks()

Validates HTML content in Narrative.

```
narrative.htmlChecks() : Boolean
```

**Examples:**
```fhirpath
Patient.text.htmlChecks()         // validates narrative HTML
```

---

## Operators

### Arithmetic Operators

```
+    Addition / string concatenation
-    Subtraction
*    Multiplication
/    Division
mod  Modulo (remainder)
div  Integer division
```

**Examples:**
```fhirpath
5 + 3               // 8
'Hello' + ' World'  // 'Hello World'
10 - 3              // 7
4 * 5               // 20
10 / 3              // 3.333...
10 mod 3            // 1
10 div 3            // 3
```

### Boolean Operators

```
and    Logical AND
or     Logical OR
xor    Logical XOR
implies  Logical implication
```

**Examples:**
```fhirpath
true and false      // false
true or false       // true
true xor false      // true
true implies false  // false
```

### Membership Operators

```
in       Element in collection
contains Collection contains element
```

**Examples:**
```fhirpath
5 in {1, 2, 3, 4, 5}           // true
{1, 2, 3} contains 2           // true
Patient.gender in {'male', 'female'}  // true
```

### Type Operators

```
is     Type test
as     Type cast
```

**Examples:**
```fhirpath
Observation.value is Quantity   // true if valueQuantity
Observation.value as Quantity   // casts to Quantity or empty
```

---

## Special Variables

### $this

Refers to current item in iteration.

```fhirpath
Patient.name.where($this.use = 'official')
{1, 2, 3}.where($this > 1)
```

### $index

Index of current item (0-based).

```fhirpath
Patient.name.where($index = 0)    // first name
{a, b, c}.select($this + $index.toString())
```

### $total

Running total in aggregate operations.

```fhirpath
{1, 2, 3}.aggregate($total + $this, 0)  // 6
```

### %resource

Root resource being evaluated.

```fhirpath
%resource.id                      // resource ID
%resource.resourceType            // 'Patient', 'Observation', etc.
```

### %context

Evaluation context (same as %resource for simple evaluations).

```fhirpath
%context.meta.lastUpdated
```

---

## Next Steps

- [FHIRPath Tutorial](fhirpath-tutorial.md) - Step-by-step learning
- [FHIRPath Guide](fhirpath-guide.md) - Conceptual overview
- [FHIRPath API](fhirpath-api.md) - Python API reference
