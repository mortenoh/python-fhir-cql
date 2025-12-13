"""Clinical code templates for synthetic data generation.

Contains SNOMED CT, LOINC, RxNorm, and other standard code sets
commonly used in clinical scenarios.
"""

from typing import TypedDict


class CodingTemplate(TypedDict, total=False):
    """Template for a FHIR Coding element."""

    system: str
    code: str
    display: str


class VitalSignTemplate(TypedDict):
    """Template for vital sign observations."""

    code: str
    display: str
    unit: str
    normal_low: float
    normal_high: float
    abnormal_low: float | None
    abnormal_high: float | None


class LabTemplate(TypedDict):
    """Template for lab observations."""

    code: str
    display: str
    unit: str
    normal_low: float
    normal_high: float
    category: str


# =============================================================================
# SNOMED CT Conditions (Common diagnoses)
# =============================================================================

SNOMED_SYSTEM = "http://snomed.info/sct"

CONDITIONS_SNOMED: list[CodingTemplate] = [
    # Cardiovascular
    {"system": SNOMED_SYSTEM, "code": "38341003", "display": "Hypertensive disorder"},
    {"system": SNOMED_SYSTEM, "code": "49436004", "display": "Atrial fibrillation"},
    {"system": SNOMED_SYSTEM, "code": "53741008", "display": "Coronary arteriosclerosis"},
    {"system": SNOMED_SYSTEM, "code": "84114007", "display": "Heart failure"},
    {"system": SNOMED_SYSTEM, "code": "22298006", "display": "Myocardial infarction"},
    # Metabolic/Endocrine
    {"system": SNOMED_SYSTEM, "code": "44054006", "display": "Type 2 diabetes mellitus"},
    {"system": SNOMED_SYSTEM, "code": "46635009", "display": "Type 1 diabetes mellitus"},
    {"system": SNOMED_SYSTEM, "code": "55822004", "display": "Hyperlipidemia"},
    {"system": SNOMED_SYSTEM, "code": "40930008", "display": "Hypothyroidism"},
    {"system": SNOMED_SYSTEM, "code": "414916001", "display": "Obesity"},
    # Respiratory
    {"system": SNOMED_SYSTEM, "code": "195967001", "display": "Asthma"},
    {"system": SNOMED_SYSTEM, "code": "13645005", "display": "Chronic obstructive pulmonary disease"},
    {"system": SNOMED_SYSTEM, "code": "233604007", "display": "Pneumonia"},
    {"system": SNOMED_SYSTEM, "code": "36971009", "display": "Sinusitis"},
    {"system": SNOMED_SYSTEM, "code": "82423001", "display": "Chronic bronchitis"},
    # Gastrointestinal
    {"system": SNOMED_SYSTEM, "code": "235595009", "display": "Gastroesophageal reflux disease"},
    {"system": SNOMED_SYSTEM, "code": "40845000", "display": "Gastric ulcer"},
    {"system": SNOMED_SYSTEM, "code": "64766004", "display": "Ulcerative colitis"},
    {"system": SNOMED_SYSTEM, "code": "34000006", "display": "Crohn's disease"},
    {"system": SNOMED_SYSTEM, "code": "197480006", "display": "Anxiety disorder"},
    # Musculoskeletal
    {"system": SNOMED_SYSTEM, "code": "396275006", "display": "Osteoarthritis"},
    {"system": SNOMED_SYSTEM, "code": "64859006", "display": "Osteoporosis"},
    {"system": SNOMED_SYSTEM, "code": "203082005", "display": "Fibromyalgia"},
    {"system": SNOMED_SYSTEM, "code": "279039007", "display": "Low back pain"},
    {"system": SNOMED_SYSTEM, "code": "57676002", "display": "Rheumatoid arthritis"},
    # Mental Health
    {"system": SNOMED_SYSTEM, "code": "35489007", "display": "Depressive disorder"},
    {"system": SNOMED_SYSTEM, "code": "191736004", "display": "Bipolar disorder"},
    {"system": SNOMED_SYSTEM, "code": "58214004", "display": "Schizophrenia"},
    {"system": SNOMED_SYSTEM, "code": "386806002", "display": "Impaired cognition"},
    {"system": SNOMED_SYSTEM, "code": "26929004", "display": "Alzheimer's disease"},
    # Neurological
    {"system": SNOMED_SYSTEM, "code": "37796009", "display": "Migraine"},
    {"system": SNOMED_SYSTEM, "code": "84757009", "display": "Epilepsy"},
    {"system": SNOMED_SYSTEM, "code": "49049000", "display": "Parkinson's disease"},
    {"system": SNOMED_SYSTEM, "code": "230690007", "display": "Cerebrovascular accident"},
    # Renal
    {"system": SNOMED_SYSTEM, "code": "709044004", "display": "Chronic kidney disease"},
    {"system": SNOMED_SYSTEM, "code": "431855005", "display": "Chronic kidney disease stage 3"},
    {"system": SNOMED_SYSTEM, "code": "90688005", "display": "Chronic renal failure"},
    # Cancer
    {"system": SNOMED_SYSTEM, "code": "254837009", "display": "Malignant neoplasm of breast"},
    {"system": SNOMED_SYSTEM, "code": "363406005", "display": "Malignant neoplasm of colon"},
    {"system": SNOMED_SYSTEM, "code": "254632001", "display": "Malignant neoplasm of prostate"},
    {"system": SNOMED_SYSTEM, "code": "254637007", "display": "Malignant neoplasm of lung"},
    # Infectious
    {"system": SNOMED_SYSTEM, "code": "186747009", "display": "Coronavirus infection"},
    {"system": SNOMED_SYSTEM, "code": "840539006", "display": "COVID-19"},
    {"system": SNOMED_SYSTEM, "code": "6142004", "display": "Influenza"},
    {"system": SNOMED_SYSTEM, "code": "186431008", "display": "Urinary tract infection"},
    # Allergies/Immune
    {"system": SNOMED_SYSTEM, "code": "61582004", "display": "Allergic rhinitis"},
    {"system": SNOMED_SYSTEM, "code": "24079001", "display": "Atopic dermatitis"},
    {"system": SNOMED_SYSTEM, "code": "402387002", "display": "Psoriasis"},
    # Other common
    {"system": SNOMED_SYSTEM, "code": "267432004", "display": "Insomnia"},
    {"system": SNOMED_SYSTEM, "code": "73211009", "display": "Diabetes mellitus"},
    {"system": SNOMED_SYSTEM, "code": "59621000", "display": "Essential hypertension"},
]


# =============================================================================
# LOINC Vital Signs
# =============================================================================

LOINC_SYSTEM = "http://loinc.org"

VITAL_SIGNS: list[VitalSignTemplate] = [
    {
        "code": "8310-5",
        "display": "Body temperature",
        "unit": "Cel",
        "normal_low": 36.1,
        "normal_high": 37.2,
        "abnormal_low": 35.0,
        "abnormal_high": 39.5,
    },
    {
        "code": "8867-4",
        "display": "Heart rate",
        "unit": "/min",
        "normal_low": 60,
        "normal_high": 100,
        "abnormal_low": 40,
        "abnormal_high": 150,
    },
    {
        "code": "9279-1",
        "display": "Respiratory rate",
        "unit": "/min",
        "normal_low": 12,
        "normal_high": 20,
        "abnormal_low": 8,
        "abnormal_high": 30,
    },
    {
        "code": "8480-6",
        "display": "Systolic blood pressure",
        "unit": "mm[Hg]",
        "normal_low": 90,
        "normal_high": 120,
        "abnormal_low": 70,
        "abnormal_high": 180,
    },
    {
        "code": "8462-4",
        "display": "Diastolic blood pressure",
        "unit": "mm[Hg]",
        "normal_low": 60,
        "normal_high": 80,
        "abnormal_low": 40,
        "abnormal_high": 110,
    },
    {
        "code": "2708-6",
        "display": "Oxygen saturation in Arterial blood",
        "unit": "%",
        "normal_low": 95,
        "normal_high": 100,
        "abnormal_low": 85,
        "abnormal_high": None,
    },
    {
        "code": "39156-5",
        "display": "Body mass index",
        "unit": "kg/m2",
        "normal_low": 18.5,
        "normal_high": 24.9,
        "abnormal_low": 15.0,
        "abnormal_high": 45.0,
    },
    {
        "code": "29463-7",
        "display": "Body weight",
        "unit": "kg",
        "normal_low": 50,
        "normal_high": 90,
        "abnormal_low": 30,
        "abnormal_high": 200,
    },
    {
        "code": "8302-2",
        "display": "Body height",
        "unit": "cm",
        "normal_low": 150,
        "normal_high": 190,
        "abnormal_low": 120,
        "abnormal_high": 220,
    },
]


# =============================================================================
# LOINC Laboratory Tests
# =============================================================================

LAB_TESTS: list[LabTemplate] = [
    # Chemistry Panel
    {
        "code": "2345-7",
        "display": "Glucose [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 70,
        "normal_high": 100,
        "category": "chemistry",
    },
    {
        "code": "4548-4",
        "display": "Hemoglobin A1c/Hemoglobin.total in Blood",
        "unit": "%",
        "normal_low": 4.0,
        "normal_high": 5.6,
        "category": "chemistry",
    },
    {
        "code": "2160-0",
        "display": "Creatinine [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 0.7,
        "normal_high": 1.3,
        "category": "chemistry",
    },
    {
        "code": "3094-0",
        "display": "Urea nitrogen [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 7,
        "normal_high": 20,
        "category": "chemistry",
    },
    {
        "code": "33914-3",
        "display": "Glomerular filtration rate/1.73 sq M.predicted",
        "unit": "mL/min/{1.73_m2}",
        "normal_low": 90,
        "normal_high": 120,
        "category": "chemistry",
    },
    # Lipid Panel
    {
        "code": "2093-3",
        "display": "Cholesterol [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 100,
        "normal_high": 200,
        "category": "lipid",
    },
    {
        "code": "2571-8",
        "display": "Triglyceride [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 50,
        "normal_high": 150,
        "category": "lipid",
    },
    {
        "code": "2085-9",
        "display": "HDL Cholesterol [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 40,
        "normal_high": 60,
        "category": "lipid",
    },
    {
        "code": "13457-7",
        "display": "LDL Cholesterol [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 50,
        "normal_high": 100,
        "category": "lipid",
    },
    # CBC
    {
        "code": "6690-2",
        "display": "Leukocytes [#/volume] in Blood",
        "unit": "10*3/uL",
        "normal_low": 4.5,
        "normal_high": 11.0,
        "category": "hematology",
    },
    {
        "code": "789-8",
        "display": "Erythrocytes [#/volume] in Blood",
        "unit": "10*6/uL",
        "normal_low": 4.5,
        "normal_high": 5.5,
        "category": "hematology",
    },
    {
        "code": "718-7",
        "display": "Hemoglobin [Mass/volume] in Blood",
        "unit": "g/dL",
        "normal_low": 12.0,
        "normal_high": 17.5,
        "category": "hematology",
    },
    {
        "code": "4544-3",
        "display": "Hematocrit [Volume Fraction] of Blood",
        "unit": "%",
        "normal_low": 36,
        "normal_high": 50,
        "category": "hematology",
    },
    {
        "code": "777-3",
        "display": "Platelets [#/volume] in Blood",
        "unit": "10*3/uL",
        "normal_low": 150,
        "normal_high": 400,
        "category": "hematology",
    },
    # Electrolytes
    {
        "code": "2951-2",
        "display": "Sodium [Moles/volume] in Serum or Plasma",
        "unit": "mmol/L",
        "normal_low": 136,
        "normal_high": 145,
        "category": "electrolytes",
    },
    {
        "code": "2823-3",
        "display": "Potassium [Moles/volume] in Serum or Plasma",
        "unit": "mmol/L",
        "normal_low": 3.5,
        "normal_high": 5.0,
        "category": "electrolytes",
    },
    {
        "code": "2075-0",
        "display": "Chloride [Moles/volume] in Serum or Plasma",
        "unit": "mmol/L",
        "normal_low": 98,
        "normal_high": 106,
        "category": "electrolytes",
    },
    {
        "code": "2028-9",
        "display": "Carbon dioxide, total [Moles/volume] in Serum or Plasma",
        "unit": "mmol/L",
        "normal_low": 23,
        "normal_high": 29,
        "category": "electrolytes",
    },
    # Liver Function
    {
        "code": "1742-6",
        "display": "Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma",
        "unit": "U/L",
        "normal_low": 7,
        "normal_high": 56,
        "category": "liver",
    },
    {
        "code": "1920-8",
        "display": "Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma",
        "unit": "U/L",
        "normal_low": 10,
        "normal_high": 40,
        "category": "liver",
    },
    {
        "code": "1975-2",
        "display": "Bilirubin.total [Mass/volume] in Serum or Plasma",
        "unit": "mg/dL",
        "normal_low": 0.1,
        "normal_high": 1.2,
        "category": "liver",
    },
    {
        "code": "6768-6",
        "display": "Alkaline phosphatase [Enzymatic activity/volume] in Serum or Plasma",
        "unit": "U/L",
        "normal_low": 44,
        "normal_high": 147,
        "category": "liver",
    },
    # Thyroid
    {
        "code": "3016-3",
        "display": "Thyrotropin [Units/volume] in Serum or Plasma",
        "unit": "mIU/L",
        "normal_low": 0.4,
        "normal_high": 4.0,
        "category": "thyroid",
    },
    {
        "code": "3051-0",
        "display": "T4 Free [Mass/volume] in Serum or Plasma",
        "unit": "ng/dL",
        "normal_low": 0.8,
        "normal_high": 1.8,
        "category": "thyroid",
    },
]


# =============================================================================
# RxNorm Medications
# =============================================================================

RXNORM_SYSTEM = "http://www.nlm.nih.gov/research/umls/rxnorm"

MEDICATIONS_RXNORM: list[CodingTemplate] = [
    # Cardiovascular
    {"system": RXNORM_SYSTEM, "code": "197361", "display": "Lisinopril 10 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197884", "display": "Amlodipine 5 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "866924", "display": "Metoprolol Succinate 25 MG Extended Release Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "859749", "display": "Atorvastatin 20 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "310798", "display": "Hydrochlorothiazide 25 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "998689", "display": "Losartan 50 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197318", "display": "Carvedilol 12.5 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197380", "display": "Furosemide 40 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "313585", "display": "Warfarin Sodium 5 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "855812", "display": "Apixaban 5 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "1361226", "display": "Rivaroxaban 20 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "318272", "display": "Clopidogrel 75 MG Oral Tablet"},
    # Diabetes
    {"system": RXNORM_SYSTEM, "code": "860975", "display": "Metformin hydrochloride 500 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197737", "display": "Glipizide 5 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "1368001", "display": "Empagliflozin 10 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "1545653", "display": "Semaglutide 0.5 MG/0.5ML Prefilled Syringe"},
    {"system": RXNORM_SYSTEM, "code": "311036", "display": "Insulin glargine 100 UNT/ML Injectable Solution"},
    {"system": RXNORM_SYSTEM, "code": "847230", "display": "Insulin lispro 100 UNT/ML Injectable Solution"},
    # GI/Acid Reflux
    {"system": RXNORM_SYSTEM, "code": "198108", "display": "Omeprazole 20 MG Delayed Release Oral Capsule"},
    {"system": RXNORM_SYSTEM, "code": "310274", "display": "Pantoprazole 40 MG Delayed Release Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "261237", "display": "Famotidine 20 MG Oral Tablet"},
    # Thyroid
    {"system": RXNORM_SYSTEM, "code": "966247", "display": "Levothyroxine Sodium 50 MCG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "966191", "display": "Levothyroxine Sodium 100 MCG Oral Tablet"},
    # Pain/Anti-inflammatory
    {"system": RXNORM_SYSTEM, "code": "198440", "display": "Acetaminophen 500 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197805", "display": "Ibuprofen 400 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "198405", "display": "Naproxen 500 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197591", "display": "Meloxicam 15 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "247521", "display": "Aspirin 81 MG Delayed Release Oral Tablet"},
    # Respiratory
    {"system": RXNORM_SYSTEM, "code": "745679", "display": "Albuterol 0.083 MG/ACTUAT Inhalation Solution"},
    {"system": RXNORM_SYSTEM, "code": "896188", "display": "Fluticasone Propionate 0.05 MG/ACTUAT Nasal Spray"},
    {"system": RXNORM_SYSTEM, "code": "1649562", "display": "Tiotropium 0.0025 MG/ACTUAT Inhalation Spray"},
    {"system": RXNORM_SYSTEM, "code": "310132", "display": "Montelukast 10 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "905233", "display": "Prednisone 10 MG Oral Tablet"},
    # Mental Health
    {"system": RXNORM_SYSTEM, "code": "312938", "display": "Sertraline 50 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "310384", "display": "Fluoxetine 20 MG Oral Capsule"},
    {"system": RXNORM_SYSTEM, "code": "283406", "display": "Escitalopram 10 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "1190220", "display": "Duloxetine 30 MG Delayed Release Oral Capsule"},
    {
        "system": RXNORM_SYSTEM,
        "code": "1098670",
        "display": "Bupropion hydrochloride 150 MG Extended Release Oral Tablet",
    },
    {"system": RXNORM_SYSTEM, "code": "197591", "display": "Trazodone 50 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "310385", "display": "Lorazepam 1 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "308049", "display": "Alprazolam 0.5 MG Oral Tablet"},
    # Antibiotics
    {"system": RXNORM_SYSTEM, "code": "308182", "display": "Amoxicillin 500 MG Oral Capsule"},
    {"system": RXNORM_SYSTEM, "code": "197516", "display": "Azithromycin 250 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "197511", "display": "Ciprofloxacin 500 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "562518", "display": "Amoxicillin 875 MG / Clavulanate 125 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "351156", "display": "Sulfamethoxazole 800 MG / Trimethoprim 160 MG Oral Tablet"},
    # Sleep/Insomnia
    {"system": RXNORM_SYSTEM, "code": "828692", "display": "Zolpidem 10 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "108460", "display": "Melatonin 3 MG Oral Tablet"},
    # Osteoporosis
    {"system": RXNORM_SYSTEM, "code": "904420", "display": "Alendronate 70 MG Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "1151131", "display": "Vitamin D3 1000 UNT Oral Tablet"},
    {"system": RXNORM_SYSTEM, "code": "318076", "display": "Calcium Carbonate 500 MG Oral Tablet"},
    # Misc
    {"system": RXNORM_SYSTEM, "code": "197318", "display": "Gabapentin 300 MG Oral Capsule"},
    {"system": RXNORM_SYSTEM, "code": "1049640", "display": "Pregabalin 75 MG Oral Capsule"},
    {"system": RXNORM_SYSTEM, "code": "197732", "display": "Tramadol 50 MG Oral Tablet"},
]


# =============================================================================
# Procedure Codes (SNOMED CT)
# =============================================================================

PROCEDURES_SNOMED: list[CodingTemplate] = [
    {"system": SNOMED_SYSTEM, "code": "428191000124101", "display": "Documentation of current medications"},
    {"system": SNOMED_SYSTEM, "code": "171207006", "display": "Screening for depression"},
    {"system": SNOMED_SYSTEM, "code": "271442007", "display": "Electrocardiogram"},
    {"system": SNOMED_SYSTEM, "code": "77477000", "display": "Computed tomography"},
    {"system": SNOMED_SYSTEM, "code": "113091000", "display": "Magnetic resonance imaging"},
    {"system": SNOMED_SYSTEM, "code": "241615005", "display": "Dual-energy X-ray absorptiometry"},
    {"system": SNOMED_SYSTEM, "code": "73761001", "display": "Colonoscopy"},
    {"system": SNOMED_SYSTEM, "code": "241541005", "display": "Mammography"},
    {"system": SNOMED_SYSTEM, "code": "385763009", "display": "Wound care"},
    {"system": SNOMED_SYSTEM, "code": "33195004", "display": "Blood pressure taking"},
    {"system": SNOMED_SYSTEM, "code": "268400002", "display": "Eye examination"},
    {"system": SNOMED_SYSTEM, "code": "46973005", "display": "Blood pressure measurement"},
    {"system": SNOMED_SYSTEM, "code": "71651007", "display": "Mammography"},
    {"system": SNOMED_SYSTEM, "code": "24623002", "display": "Flu vaccination"},
    {"system": SNOMED_SYSTEM, "code": "252465000", "display": "Pulse oximetry"},
]


# =============================================================================
# Encounter Types
# =============================================================================

ENCOUNTER_CLASSES: list[CodingTemplate] = [
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB", "display": "ambulatory"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "EMER", "display": "emergency"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "ACUTE", "display": "inpatient acute"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "SS", "display": "short stay"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "HH", "display": "home health"},
    {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "VR", "display": "virtual"},
]


ENCOUNTER_TYPES: list[CodingTemplate] = [
    {"system": SNOMED_SYSTEM, "code": "185349003", "display": "Encounter for check up"},
    {"system": SNOMED_SYSTEM, "code": "390906007", "display": "Follow-up encounter"},
    {"system": SNOMED_SYSTEM, "code": "439740005", "display": "Postoperative follow-up visit"},
    {"system": SNOMED_SYSTEM, "code": "185345009", "display": "Encounter for symptom"},
    {"system": SNOMED_SYSTEM, "code": "308335008", "display": "Patient encounter procedure"},
    {"system": SNOMED_SYSTEM, "code": "702927004", "display": "Urgent care visit"},
    {"system": SNOMED_SYSTEM, "code": "50849002", "display": "Emergency room admission"},
]


# =============================================================================
# Observation Categories
# =============================================================================

OBSERVATION_CATEGORIES: list[CodingTemplate] = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
        "code": "vital-signs",
        "display": "Vital Signs",
    },
    {
        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
        "code": "laboratory",
        "display": "Laboratory",
    },
    {
        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
        "code": "social-history",
        "display": "Social History",
    },
    {"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "survey", "display": "Survey"},
    {"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "exam", "display": "Exam"},
]


# =============================================================================
# Clinical Status Codes
# =============================================================================

CONDITION_CLINICAL_STATUS: list[CodingTemplate] = [
    {"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active", "display": "Active"},
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "recurrence",
        "display": "Recurrence",
    },
    {"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "relapse", "display": "Relapse"},
    {"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "inactive", "display": "Inactive"},
    {"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "remission", "display": "Remission"},
    {"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "resolved", "display": "Resolved"},
]

CONDITION_VERIFICATION_STATUS: list[CodingTemplate] = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "unconfirmed",
        "display": "Unconfirmed",
    },
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "provisional",
        "display": "Provisional",
    },
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "differential",
        "display": "Differential",
    },
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "confirmed",
        "display": "Confirmed",
    },
]


# =============================================================================
# Practitioner Specialties
# =============================================================================

PRACTITIONER_SPECIALTIES: list[CodingTemplate] = [
    {"system": SNOMED_SYSTEM, "code": "419772000", "display": "Family medicine"},
    {"system": SNOMED_SYSTEM, "code": "394802001", "display": "General medicine"},
    {"system": SNOMED_SYSTEM, "code": "394579002", "display": "Cardiology"},
    {"system": SNOMED_SYSTEM, "code": "394583002", "display": "Endocrinology"},
    {"system": SNOMED_SYSTEM, "code": "394584008", "display": "Gastroenterology"},
    {"system": SNOMED_SYSTEM, "code": "394591006", "display": "Neurology"},
    {"system": SNOMED_SYSTEM, "code": "394592004", "display": "Oncology"},
    {"system": SNOMED_SYSTEM, "code": "394600006", "display": "Pulmonology"},
    {"system": SNOMED_SYSTEM, "code": "394587001", "display": "Psychiatry"},
    {"system": SNOMED_SYSTEM, "code": "394586005", "display": "Gynecology"},
    {"system": SNOMED_SYSTEM, "code": "394609007", "display": "General surgery"},
    {"system": SNOMED_SYSTEM, "code": "394610002", "display": "Orthopedic surgery"},
    {"system": SNOMED_SYSTEM, "code": "418112009", "display": "Nurse practitioner"},
    {"system": SNOMED_SYSTEM, "code": "224535009", "display": "Physician assistant"},
]


# =============================================================================
# Helper Functions
# =============================================================================


def make_codeable_concept(coding: CodingTemplate | dict[str, str], text: str | None = None) -> dict:
    """Create a FHIR CodeableConcept from a coding template."""
    result: dict = {"coding": [dict(coding)]}
    if text:
        result["text"] = text
    elif "display" in coding:
        result["text"] = coding["display"]
    return result


def make_coding(template: CodingTemplate | dict[str, str]) -> dict:
    """Create a FHIR Coding from a template."""
    return dict(template)
