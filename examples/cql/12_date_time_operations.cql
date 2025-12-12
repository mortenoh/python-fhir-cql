/*
 * Date and Time Operations - Working with dates and times in CQL
 */
library DateTimeOperations version '1.0.0'

using FHIR version '4.0.1'

// =====================================================
// Date/Time Literals
// =====================================================

define DateLiteral: @2024-06-15
define DateTimeLiteral: @2024-06-15T10:30:00
define DateTimeWithTimezone: @2024-06-15T10:30:00-05:00
define TimeLiteral: @T14:30:00
define PartialDate: @2024-06
define YearOnly: @2024

// =====================================================
// Current Date/Time
// =====================================================

define CurrentDate: Today()
define CurrentDateTime: Now()
define CurrentTime: TimeOfDay()

// =====================================================
// Component Extraction
// =====================================================

define TestDate: @2024-06-15T10:30:45

define ExtractYear: year from TestDate
define ExtractMonth: month from TestDate
define ExtractDay: day from TestDate
define ExtractHour: hour from TestDate
define ExtractMinute: minute from TestDate
define ExtractSecond: second from TestDate

// Date of a datetime
define DateFromDateTime: date from @2024-06-15T10:30:00
define TimeFromDateTime: time from @2024-06-15T10:30:00

// =====================================================
// Date Arithmetic
// =====================================================

define AddYears: @2024-01-15 + 2 years
define AddMonths: @2024-01-15 + 3 months
define AddWeeks: @2024-01-15 + 2 weeks
define AddDays: @2024-01-15 + 30 days

define SubtractYears: @2024-01-15 - 1 year
define SubtractMonths: @2024-06-15 - 6 months
define SubtractDays: @2024-01-15 - 10 days

// DateTime arithmetic
define AddHours: @2024-01-15T10:00:00 + 5 hours
define AddMinutes: @2024-01-15T10:00:00 + 45 minutes
define AddSeconds: @2024-01-15T10:00:00 + 30 seconds

// =====================================================
// Duration Calculations
// =====================================================

define BirthDate: @1990-03-15
define ReferenceDate: @2024-06-15

define YearsBetween: years between BirthDate and ReferenceDate
define MonthsBetween: months between BirthDate and ReferenceDate
define WeeksBetween: weeks between BirthDate and ReferenceDate
define DaysBetween: days between BirthDate and ReferenceDate

// Time durations
define StartTime: @T09:00:00
define EndTime: @T17:30:00

define HoursBetween: hours between StartTime and EndTime
define MinutesBetween: minutes between StartTime and EndTime

// =====================================================
// Date Comparisons
// =====================================================

define Date1: @2024-01-15
define Date2: @2024-06-15

define IsBefore: Date1 before Date2
define IsAfter: Date2 after Date1
define IsSameOrBefore: Date1 same or before Date2
define IsSameOrAfter: Date2 same or after Date1

// Precision comparisons
define SameDay: @2024-06-15T10:00:00 same day as @2024-06-15T22:00:00
define SameMonth: @2024-06-01 same month as @2024-06-30
define SameYear: @2024-01-01 same year as @2024-12-31

// =====================================================
// Edge Cases
// =====================================================

// Leap year handling
define LeapYearDate: @2024-02-29
define LeapYearPlusYear: @2024-02-29 + 1 year

// Month-end handling
define MonthEnd: @2024-01-31
define MonthEndPlusMonth: @2024-01-31 + 1 month

// Year boundary
define NewYearsEve: @2024-12-31
define CrossYear: @2024-12-31 + 1 day

// Midnight boundary
define BeforeMidnight: @2024-06-15T23:59:59
define AfterMidnight: @2024-06-15T23:59:59 + 1 minute

// =====================================================
// Practical Clinical Examples
// =====================================================

// Calculate age
define function CalculateAge(birthDate Date) returns Integer:
    years between birthDate and Today()

// Calculate age at specific date
define function AgeAt(birthDate Date, asOf Date) returns Integer:
    years between birthDate and asOf

// Check if date is within last N days
define function WithinLastDays(testDate Date, days Integer) returns Boolean:
    testDate >= Today() - days day and testDate <= Today()

// Check if within measurement period
define function DuringMeasurementPeriod(eventDate Date, periodStart Date, periodEnd Date) returns Boolean:
    eventDate >= periodStart and eventDate <= periodEnd

// Calculate days since event
define function DaysSince(eventDate Date) returns Integer:
    days between eventDate and Today()

// Get start of year
define function StartOfYear(d Date) returns Date:
    @(year from d)-01-01

// Get end of year
define function EndOfYear(d Date) returns Date:
    @(year from d)-12-31

// Check if pediatric patient (under 18)
define function IsPediatric(birthDate Date) returns Boolean:
    CalculateAge(birthDate) < 18

// Check if geriatric patient (65+)
define function IsGeriatric(birthDate Date) returns Boolean:
    CalculateAge(birthDate) >= 65

// =====================================================
// Test Examples
// =====================================================

define TestBirthDate: @1985-07-20
define TestAge: CalculateAge(TestBirthDate)
define TestAgeAt2020: AgeAt(TestBirthDate, @2020-07-20)
define TestWithinLast30Days: WithinLastDays(@2024-06-01, 30)
define TestDaysSince: DaysSince(@2024-01-01)
