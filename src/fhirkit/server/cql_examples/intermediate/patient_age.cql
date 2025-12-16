library PatientAge version '1.0.0'

using FHIR version '4.0.1'
include FHIRHelpers version '4.0.1'

context Patient

define "Birth Date": Patient.birthDate

define "Age In Years": AgeInYears()
define "Age In Months": AgeInMonths()
define "Age In Days": AgeInDays()

define "Age At Date": AgeInYearsAt(@2024-01-01)

define "Is Infant": AgeInYears() < 1
define "Is Toddler": AgeInYears() in Interval[1, 3)
define "Is Child": AgeInYears() in Interval[3, 12)
define "Is Adolescent": AgeInYears() in Interval[12, 18)
define "Is Adult": AgeInYears() >= 18
define "Is Senior": AgeInYears() >= 65

define "Age Group":
  case
    when AgeInYears() < 1 then 'Infant'
    when AgeInYears() < 3 then 'Toddler'
    when AgeInYears() < 12 then 'Child'
    when AgeInYears() < 18 then 'Adolescent'
    when AgeInYears() < 65 then 'Adult'
    else 'Senior'
  end

define "Is Working Age": AgeInYears() in Interval[18, 65)
define "Is Pediatric": AgeInYears() < 18
define "Is Geriatric": AgeInYears() >= 65
