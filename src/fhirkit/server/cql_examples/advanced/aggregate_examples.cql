library AggregateExamples version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "Observations":
  [Observation] O where O.status = 'final'

define "Observation Count":
  Count("Observations")

define "Numeric Values":
  "Observations" O
    where O.value is Quantity
    return (O.value as Quantity).value

define "Sum of Values":
  Sum("Numeric Values")

define "Average Value":
  Avg("Numeric Values")

define "Minimum Value":
  Min("Numeric Values")

define "Maximum Value":
  Max("Numeric Values")

define "Standard Deviation":
  StdDev("Numeric Values")

define "Variance":
  Variance("Numeric Values")

define "Median":
  Median("Numeric Values")

define "Population Standard Deviation":
  PopulationStdDev("Numeric Values")

// Aggregate with Filter
define "Recent Observations":
  "Observations" O
    where O.effective after Today() - 30 days

define "Recent Count":
  Count("Recent Observations")

// Custom Aggregation
define "Value Distribution":
  from "Observations" O
    let val: (O.value as Quantity).value
    return {
      code: O.code.coding.first().display,
      value: val,
      aboveAvg: val > Avg("Numeric Values")
    }
