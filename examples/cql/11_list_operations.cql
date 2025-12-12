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
// List Query Operations
// =====================================================

define FilteredList:
    from n in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    where n mod 2 = 0
    return n

define TransformedList:
    from n in {1, 2, 3, 4, 5}
    return n * 2

define FilterAndTransform:
    from n in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    where n mod 2 = 0
    return n * n

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

// Find duplicates
define function FindDuplicates(items List<Integer>) returns List<Integer>:
    from item in items
    where Count(from i in items where i = item return i) > 1
    return all item

// Get unique values preserving order
define function UniqueOrdered(items List<Integer>) returns List<Integer>:
    Flatten(
        from i in IndexList(items)
        where i.index = IndexOf(items, i.value)
        return {i.value}
    )

// Helper to create index-value pairs
define function IndexList(items List<Integer>) returns List<Tuple{index Integer, value Integer}>:
    from idx in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    where idx < Count(items)
    return Tuple { index: idx, value: items[idx] }

// Chunk list into groups
define function ChunkList(items List<Integer>, size Integer) returns List<List<Integer>>:
    from i in {0, 1, 2, 3, 4}
    where i * size < Count(items)
    return Take(Skip(items, i * size), size)

// Test examples
define TestNumbers: {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5}
define TestDuplicates: FindDuplicates(TestNumbers)
