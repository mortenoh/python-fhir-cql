/*
 * List Operations - Working with lists in CQL
 */
library ListOperations version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// List Creation
// =====================================================

define EmptyList: {}
define IntegerList: {1, 2, 3, 4, 5}
define StringList: {'apple', 'banana', 'cherry'}
define MixedList: {1, 'two', true, null}
define NestedList: {{1, 2}, {3, 4}, {5, 6}}

// =====================================================
// List Access
// =====================================================

define FirstElement: First({1, 2, 3, 4, 5})
define LastElement: Last({1, 2, 3, 4, 5})
define IndexedAccess: ({1, 2, 3, 4, 5})[2]
define SingletonFrom: singleton from {42}

// =====================================================
// List Slicing
// =====================================================

define TakeThree: Take({1, 2, 3, 4, 5}, 3)
define SkipTwo: Skip({1, 2, 3, 4, 5}, 2)
define TailOfList: Tail({1, 2, 3, 4, 5})

// =====================================================
// List Membership
// =====================================================

define ContainsTrue: {1, 2, 3} contains 2
define ContainsFalse: {1, 2, 3} contains 5
define InTrue: 2 in {1, 2, 3}
define InFalse: 5 in {1, 2, 3}

// =====================================================
// List Comparison
// =====================================================

define ListEquality: {1, 2, 3} = {1, 2, 3}
define ListInequality: {1, 2, 3} = {3, 2, 1}
define IncludesTrue: {1, 2, 3, 4, 5} includes {2, 3, 4}
define IncludedInTrue: {2, 3} included in {1, 2, 3, 4, 5}

// =====================================================
// List Combination
// =====================================================

define UnionLists: {1, 2, 3} union {3, 4, 5}
define IntersectLists: {1, 2, 3, 4} intersect {2, 3, 4, 5}
define ExceptLists: {1, 2, 3, 4, 5} except {2, 4}
define CombineLists: Combine({1, 2}, {3, 4})

// =====================================================
// List Transformation
// =====================================================

define DistinctList: distinct {1, 2, 2, 3, 3, 3}
define FlattenNested: Flatten({{1, 2}, {3, 4}, {5}})
define SortAscending: Sort({5, 2, 8, 1, 9})

// =====================================================
// Existence and Counting
// =====================================================

define ExistsTrue: exists({1, 2, 3})
define ExistsFalse: exists({})
define CountElements: Count({1, 2, 3, 4, 5})
define CountEmpty: Count({})

// =====================================================
// Aggregate Functions
// =====================================================

define SumNumbers: Sum({1, 2, 3, 4, 5})
define AvgNumbers: Avg({1, 2, 3, 4, 5})
define MinNumber: Min({5, 2, 8, 1, 9})
define MaxNumber: Max({5, 2, 8, 1, 9})

// =====================================================
// Boolean Aggregates
// =====================================================

define AllTrueTest: AllTrue({true, true, true})
define AllTrueWithFalse: AllTrue({true, false, true})
define AnyTrueTest: AnyTrue({false, true, false})
define AnyTrueAllFalse: AnyTrue({false, false, false})

// =====================================================
// Null Handling in Lists
// =====================================================

define ListWithNulls: {1, null, 2, null, 3}
define CountWithNulls: Count({1, null, 2, null, 3})
define SumWithNulls: Sum({1, null, 2, null, 3})
define CoalesceFromList: Coalesce({null, null, 'found', 'also'})

// =====================================================
// Practical Examples
// =====================================================

// Check if list has duplicates
define TestNumbers: {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5}
define HasDuplicates: Count(TestNumbers) != Count(distinct TestNumbers)

// Filter using where clause
define EvenNumbers: ({2, 4, 6, 8, 10} except {})

// Range operations
define RangeSum: Sum({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
define RangeCount: Count({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
