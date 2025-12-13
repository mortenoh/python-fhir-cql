/*
 * CQL Example 21: Immunization Status and Recommendations
 *
 * Demonstrates:
 * - Querying Immunization resources
 * - Vaccination status checks
 * - Immunization series tracking
 * - Age-based recommendations
 */

library ImmunizationQueries version '1.0.0'

using FHIR version '4.0.1'

// Code Systems
codesystem "CVX": 'http://hl7.org/fhir/sid/cvx'
codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "ImmunizationStatus": 'http://hl7.org/fhir/event-status'

// Common vaccine codes (CVX)
code "Flu Vaccine": '141' from "CVX"
code "COVID-19 Pfizer": '208' from "CVX"
code "COVID-19 Moderna": '207' from "CVX"
code "Tdap": '115' from "CVX"
code "Pneumococcal PCV13": '133' from "CVX"
code "Pneumococcal PPSV23": '33' from "CVX"
code "Shingrix": '187' from "CVX"
code "Hepatitis B": '08' from "CVX"
code "MMR": '03' from "CVX"

context Patient

// =====================================================
// Basic Immunization Queries
// =====================================================

// All immunizations
define AllImmunizations:
  [Immunization]

// Completed immunizations
define CompletedImmunizations:
  [Immunization] I
    where I.status = 'completed'

// Not given (refused, contraindicated, etc.)
define DeclinedImmunizations:
  [Immunization] I
    where I.status = 'not-done'

// =====================================================
// COVID-19 Vaccination Status
// =====================================================

// All COVID-19 vaccinations
define COVID19Vaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '207'  // Moderna
       or I.vaccineCode.coding.code contains '208'  // Pfizer
       or I.vaccineCode.coding.code contains '212'  // J&J
       or I.vaccineCode.coding.code contains '218'  // Pfizer Bivalent
       or I.vaccineCode.coding.code contains '219'  // Moderna Bivalent

// COVID-19 vaccination count
define COVID19VaccinationCount:
  Count(COVID19Vaccinations)

// Has completed primary COVID series (2+ doses for mRNA)
define HasCompletedCOVIDPrimarySeries:
  COVID19VaccinationCount >= 2

// Has recent COVID booster (within last year)
define HasRecentCOVIDBooster:
  exists (
    COVID19Vaccinations I
      where I.occurrence as dateTime >= Today() - 1 year
  )

// COVID-19 booster recommended (if last dose > 1 year ago)
define COVIDBoosterRecommended:
  HasCompletedCOVIDPrimarySeries
    and not HasRecentCOVIDBooster

// Most recent COVID vaccine date
define MostRecentCOVIDVaccineDate:
  Max(COVID19Vaccinations I return I.occurrence as dateTime)

// =====================================================
// Influenza Vaccination
// =====================================================

// All flu vaccinations
define FluVaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '141'  // Flu
       or I.vaccineCode.coding.code contains '140'  // Flu intradermal
       or I.vaccineCode.coding.code contains '153'  // Flu high dose
       or I.vaccineCode.coding.code contains '158'  // Flu recombinant

// Current flu season vaccination
define HasCurrentFluVaccine:
  exists (
    FluVaccinations I
      where I.occurrence as dateTime >= @2024-08-01  // Current flu season start
  )

// Flu vaccine recommended (if not given this season)
define FluVaccineRecommended:
  not HasCurrentFluVaccine

// =====================================================
// Pneumococcal Vaccination
// =====================================================

// PCV13 (Prevnar)
define PCV13Vaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '133'

// PPSV23 (Pneumovax)
define PPSV23Vaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '33'

// Has received pneumococcal vaccine
define HasPneumococcalVaccination:
  exists PCV13Vaccinations or exists PPSV23Vaccinations

// Pneumococcal vaccine recommended (age 65+, none documented)
define PneumococcalVaccineRecommended:
  not HasPneumococcalVaccination  // Would check age in real implementation

// =====================================================
// Shingles (Herpes Zoster) Vaccination
// =====================================================

// Shingrix vaccinations
define ShinglesVaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '187'

// Shingrix requires 2 doses
define ShinglesSeriesComplete:
  Count(ShinglesVaccinations) >= 2

// Shingles vaccine recommended (age 50+, series incomplete)
define ShinglesVaccineRecommended:
  not ShinglesSeriesComplete

// =====================================================
// Tdap Vaccination
// =====================================================

// Tdap vaccinations
define TdapVaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '115'

// Most recent Tdap
define MostRecentTdap:
  Max(TdapVaccinations I return I.occurrence as dateTime)

// Tdap due (every 10 years)
define TdapDue:
  MostRecentTdap is null
    or MostRecentTdap < Today() - 10 years

// =====================================================
// Hepatitis B Vaccination
// =====================================================

// Hepatitis B vaccinations
define HepBVaccinations:
  CompletedImmunizations I
    where I.vaccineCode.coding.code contains '08'
       or I.vaccineCode.coding.code contains '43'
       or I.vaccineCode.coding.code contains '44'

// Hepatitis B series complete (3 doses for adults)
define HepBSeriesComplete:
  Count(HepBVaccinations) >= 3

// =====================================================
// Immunization Series Tracking
// =====================================================

// Get dose number for a vaccination
define function GetDoseNumber(I Immunization):
  if I.protocolApplied is not null then
    First(I.protocolApplied).doseNumber as integer
  else
    null

// COVID series doses
define COVIDSeriesDoses:
  COVID19Vaccinations I
    return Tuple {
      date: I.occurrence as dateTime,
      doseNumber: GetDoseNumber(I),
      manufacturer: I.manufacturer.display
    }

// =====================================================
// Adverse Reactions
// =====================================================

// Immunizations with recorded reactions
define ImmunizationsWithReactions:
  CompletedImmunizations I
    where exists I.reaction

// Get all recorded reactions
define AllVaccineReactions:
  flatten (
    ImmunizationsWithReactions I
      return all I.reaction
  )

// Has had severe vaccine reaction
define HasHadSevereVaccineReaction:
  exists (
    AllVaccineReactions R
      where R.detail.display contains 'severe'
         or R.detail.display contains 'anaphyla'
  )

// =====================================================
// Vaccine Administration Details
// =====================================================

// Vaccines given at specific site
define VaccinesGivenInLeftArm:
  CompletedImmunizations I
    where I.site.coding.code contains 'LA'

// =====================================================
// Immunization Calendar/Schedule
// =====================================================

// All vaccines due
define VaccinesDue:
  Tuple {
    flu: FluVaccineRecommended,
    covid: COVIDBoosterRecommended,
    tdap: TdapDue,
    pneumococcal: PneumococcalVaccineRecommended,
    shingles: ShinglesVaccineRecommended
  }

// Count of vaccines due
define NumberOfVaccinesDue:
  (if FluVaccineRecommended then 1 else 0)
  + (if COVIDBoosterRecommended then 1 else 0)
  + (if TdapDue then 1 else 0)
  + (if PneumococcalVaccineRecommended then 1 else 0)
  + (if ShinglesVaccineRecommended then 1 else 0)

// =====================================================
// Immunization Summary
// =====================================================

define ImmunizationSummary:
  Tuple {
    totalImmunizations: Count(CompletedImmunizations),
    covidDoses: COVID19VaccinationCount,
    covidLastDate: MostRecentCOVIDVaccineDate,
    fluCurrentSeason: HasCurrentFluVaccine,
    tdapLastDate: MostRecentTdap,
    tdapDue: TdapDue,
    vaccinationsDue: NumberOfVaccinesDue
  }

// =====================================================
// Immunization Status Message
// =====================================================

define ImmunizationStatusMessage:
  if NumberOfVaccinesDue = 0 then
    'All immunizations are up to date.'
  else if NumberOfVaccinesDue = 1 then
    '1 vaccination is due.'
  else
    ToString(NumberOfVaccinesDue) + ' vaccinations are due.'
