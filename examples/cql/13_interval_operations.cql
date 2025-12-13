/*
 * Interval Operations - Working with intervals in CQL
 */
library IntervalOperations version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// Interval Creation
// =====================================================

// Closed intervals (include endpoints)
define ClosedInterval: Interval[1, 10]
define DateClosedInterval: Interval[@2024-01-01, @2024-12-31]

// Open intervals (exclude endpoints)
define OpenInterval: Interval(1, 10)

// Half-open intervals
define LeftOpenInterval: Interval(1, 10]
define RightOpenInterval: Interval[1, 10)

// Point intervals (single value)
define PointInterval: Interval[5, 5]

// =====================================================
// Interval Boundaries
// =====================================================

define TestInterval: Interval[1, 10]

define StartOfInterval: start of TestInterval
define EndOfInterval: end of TestInterval
define WidthOfInterval: width of TestInterval

define LowOfInterval: low TestInterval
define HighOfInterval: high TestInterval

// Point from single-value interval
define PointFromInterval: point from Interval[5, 5]

// =====================================================
// Interval Membership
// =====================================================

// Contains (interval contains point)
define ContainsPoint: Interval[1, 10] contains 5
define NotContainsPoint: Interval[1, 10] contains 15

// In (point in interval)
define PointInInterval: 5 in Interval[1, 10]
define PointNotInInterval: 15 in Interval[1, 10]

// Boundary cases
define AtLowBound: 1 in Interval[1, 10]
define AtHighBound: 10 in Interval[1, 10]
define BelowOpenLow: 1 in Interval(1, 10)
define AboveOpenHigh: 10 in Interval[1, 10)

// =====================================================
// Interval Relationships
// =====================================================

define IntervalA: Interval[1, 5]
define IntervalB: Interval[3, 8]
define IntervalC: Interval[6, 10]
define IntervalD: Interval[2, 4]

// Overlaps
define OverlapsTrue: IntervalA overlaps IntervalB
define OverlapsFalse: IntervalA overlaps IntervalC

// Includes (one interval contains another)
define IncludesTrue: Interval[1, 10] includes Interval[3, 7]
define IncludesFalse: IntervalA includes IntervalB

// Included in (one interval is within another)
define IncludedInTrue: Interval[3, 7] included in Interval[1, 10]

// Properly includes/included in (strictly contains)
define ProperlyIncludes: Interval[1, 10] properly includes Interval[3, 7]

// =====================================================
// Interval Comparison
// =====================================================

// Before/After
define IntervalBefore: Interval[1, 3] before Interval[5, 10]
define IntervalAfter: Interval[5, 10] after Interval[1, 3]

// Meets (adjacent intervals)
define MeetsTrue: Interval[1, 5] meets Interval[6, 10]
define MeetsBefore: Interval[1, 5] meets before Interval[6, 10]
define MeetsAfter: Interval[6, 10] meets after Interval[1, 5]

// Starts/Ends
define StartsTrue: Interval[1, 5] starts Interval[1, 10]
define EndsTrue: Interval[5, 10] ends Interval[1, 10]

// =====================================================
// Interval Operations
// =====================================================

// Union (combine intervals)
define UnionOverlapping: Interval[1, 5] union Interval[3, 8]
define UnionDisjoint: Interval[1, 3] union Interval[5, 8]

// Intersect (common part)
define IntersectOverlapping: Interval[1, 5] intersect Interval[3, 8]
define IntersectNoOverlap: Interval[1, 3] intersect Interval[5, 8]

// Except (difference)
define ExceptInterval: Interval[1, 10] except Interval[4, 6]

// =====================================================
// Collapse and Expand
// =====================================================

// Collapse adjacent/overlapping intervals
define IntervalsToCollapse: {
    Interval[1, 3],
    Interval[2, 5],
    Interval[7, 9],
    Interval[8, 10]
}
define CollapsedIntervals: collapse IntervalsToCollapse

// Expand interval to discrete points
define ExpandByDay: expand Interval[@2024-01-01, @2024-01-05] per day
define ExpandByMonth: expand Interval[@2024-01, @2024-06] per month
define ExpandByYear: expand Interval[@2020, @2024] per year

// =====================================================
// Date/Time Intervals
// =====================================================

define MeasurementPeriod: Interval[@2024-01-01T00:00:00, @2024-12-31T23:59:59]

// Check if date during interval
define DateDuring: @2024-06-15 during MeasurementPeriod
define DateNotDuring: @2023-06-15 during MeasurementPeriod

// Create interval from dates
define Q1_2024: Interval[@2024-01-01, @2024-03-31]
define Q2_2024: Interval[@2024-04-01, @2024-06-30]
define Q3_2024: Interval[@2024-07-01, @2024-09-30]
define Q4_2024: Interval[@2024-10-01, @2024-12-31]

// =====================================================
// Practical Clinical Examples
// =====================================================

// Check if encounter is within measurement period
define function EncounterInPeriod(encounterStart Date, encounterEnd Date, periodStart Date, periodEnd Date) returns Boolean:
    Interval[encounterStart, encounterEnd] overlaps Interval[periodStart, periodEnd]

// Get overlapping portion of two intervals
define function GetOverlap(interval1 Interval<Date>, interval2 Interval<Date>) returns Interval<Date>:
    interval1 intersect interval2

// Calculate gap between intervals
define function GapBetween(interval1 Interval<Integer>, interval2 Interval<Integer>) returns Integer:
    if interval1 before interval2 then
        (start of interval2) - (end of interval1) - 1
    else if interval2 before interval1 then
        (start of interval1) - (end of interval2) - 1
    else
        0

// Check if interval list covers a period (after collapsing)
define function CoversAfterCollapse(coverageIntervals List<Interval<Date>>, period Interval<Date>) returns Boolean:
    exists(collapse coverageIntervals C where C includes period)

// Create age range interval
define function AgeRange(minAge Integer, maxAge Integer) returns Interval<Integer>:
    Interval[minAge, maxAge]

// =====================================================
// Test Examples
// =====================================================

define TestEncounterPeriod: Interval[@2024-03-01, @2024-03-15]
define TestMeasurementPeriod: Interval[@2024-01-01, @2024-12-31]
define TestEncounterInPeriod: TestEncounterPeriod overlaps TestMeasurementPeriod

define AdultAgeRange: AgeRange(18, 64)
define GeriatricAgeRange: AgeRange(65, 120)
define Age45InAdult: 45 in AdultAgeRange
define Age70InGeriatric: 70 in GeriatricAgeRange
