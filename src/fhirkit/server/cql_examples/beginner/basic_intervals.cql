library IntervalExamples version '1.0.0'

/*
 * CQL Interval Operations
 * -----------------------
 * Intervals represent ranges - essential for clinical queries:
 * - Measurement periods: Interval[@2024-01-01, @2024-12-31]
 * - Value ranges: blood pressure 90-140 mmHg
 * - Time windows: "in the last 30 days"
 *
 * [ ] = inclusive (closed), ( ) = exclusive (open)
 */

// Creating intervals
define "Closed": Interval[1, 10]     // Includes 1 and 10
define "Open": Interval(1, 10)       // Excludes 1 and 10
define "Half Open": Interval[1, 10)  // Includes 1, excludes 10

// Date intervals (very common in clinical queries)
define "This Year": Interval[@2024-01-01, @2024-12-31]
define "Measurement Period": Interval[Today() - 1 year, Today()]

// Getting interval boundaries
define "Start": start of Interval[1, 10]    // Result: 1
define "End": end of Interval[1, 10]        // Result: 10

// Testing if value is in interval
define "5 In Range": 5 in Interval[1, 10]      // Result: true
define "15 In Range": 15 in Interval[1, 10]    // Result: false

// Comparing intervals
define "Overlaps": Interval[1, 5] overlaps Interval[4, 8]  // true
define "Before": Interval[1, 3] before Interval[5, 8]      // true
define "During": Interval[3, 7] during Interval[1, 10]     // true

// Combining intervals
define "Union": Interval[1, 5] union Interval[4, 10]       // [1,10]
define "Intersect": Interval[1, 8] intersect Interval[4, 12]  // [4,8]
