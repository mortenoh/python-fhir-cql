library DateExamples version '1.0.0'

/*
 * CQL Date & Time Operations
 * --------------------------
 * Dates are CRITICAL in clinical CQL for:
 * - Calculating patient age
 * - Finding observations in time ranges
 * - Checking medication durations
 *
 * Date literals start with @: @2024-01-15
 */

// Current date/time
define "Today": Today()       // Current date (no time)
define "Now": Now()           // Current date AND time

// Date literals (start with @)
define "Date Literal": @2024-01-15
define "DateTime Literal": @2024-01-15T10:30:00
define "Time Literal": @T14:30:00

// Extracting parts of dates
define "Year": year from @2024-06-15      // Result: 2024
define "Month": month from @2024-06-15    // Result: 6
define "Day": day from @2024-06-15        // Result: 15

// Date arithmetic (essential for clinical queries!)
define "Add Days": @2024-01-01 + 30 days
define "Add Months": @2024-01-01 + 3 months
define "Subtract": @2024-12-31 - 1 month

// Duration calculations
define "Days Between": days between @2024-01-01 and @2024-12-31    // Result: 365
define "Months Between": months between @2024-01-01 and @2024-12-31
define "Years Between": years between @2000-01-01 and @2024-01-01  // Result: 24

// Comparisons (for filtering by date)
define "Date Comparison": @2024-01-01 < @2024-12-31   // Result: true
define "Is Past": Today() > @2020-01-01               // Result: true
define "Is Future": @2030-01-01 > Today()             // Result: true
