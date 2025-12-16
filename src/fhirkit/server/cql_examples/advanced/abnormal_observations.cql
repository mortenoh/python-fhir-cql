library AbnormalObservations version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "All Observations":
  [Observation]

define "Observations With Interpretation":
  [Observation] O where O.interpretation is not null

define "Abnormal Observations":
  [Observation] O
    where O.interpretation.coding.code contains 'A'
      or O.interpretation.coding.code contains 'AA'
      or O.interpretation.coding.code contains 'H'
      or O.interpretation.coding.code contains 'HH'
      or O.interpretation.coding.code contains 'L'
      or O.interpretation.coding.code contains 'LL'

define "High Values":
  [Observation] O
    where O.interpretation.coding.code contains 'H'
      or O.interpretation.coding.code contains 'HH'

define "Low Values":
  [Observation] O
    where O.interpretation.coding.code contains 'L'
      or O.interpretation.coding.code contains 'LL'

define "Critical Values":
  [Observation] O
    where O.interpretation.coding.code contains 'HH'
      or O.interpretation.coding.code contains 'LL'
      or O.interpretation.coding.code contains 'AA'

define "Out Of Range":
  [Observation] O
    where (O.value as Quantity).value > O.referenceRange.first().high.value
      or (O.value as Quantity).value < O.referenceRange.first().low.value

define "Recent Abnormal":
  "Abnormal Observations" O
    where O.effective in Interval[Today() - 30 days, Today()]
