library LatestObservations version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Observations":
  [Observation]

define "Observation Count":
  Count([Observation])

define "Latest Observation":
  Last([Observation] O sort by effective)

define "Latest Observation Date":
  ("Latest Observation").effective

define "Latest Observation Code":
  ("Latest Observation").code.coding.first().display

define "Latest Observation Value":
  ("Latest Observation").value

define "Observations Last 30 Days":
  [Observation] O
    where O.effective in Interval[Today() - 30 days, Today()]

define "Observations Last Year":
  [Observation] O
    where O.effective in Interval[Today() - 1 year, Today()]

define "Most Recent By Category":
  from [Observation] O
    let category: O.category.coding.first().code
    where O.effective = Max([Observation] O2
      where O2.category.coding.first().code = category
      return O2.effective)
    return {
      category: category,
      code: O.code.coding.first().display,
      value: O.value,
      date: O.effective
    }
