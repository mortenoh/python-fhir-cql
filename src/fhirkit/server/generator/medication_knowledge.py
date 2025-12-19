"""MedicationKnowledge resource generator."""

from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class MedicationKnowledgeGenerator(FHIRResourceGenerator):
    """Generator for FHIR MedicationKnowledge resources."""

    # Medication codes (RxNorm)
    MEDICATIONS = [
        {
            "code": "197361",
            "display": "Amlodipine 5 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "310965",
            "display": "Lisinopril 10 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "860975",
            "display": "Metformin 500 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "866924",
            "display": "Omeprazole 20 MG Oral Capsule",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "314076",
            "display": "Simvastatin 20 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "198211",
            "display": "Aspirin 81 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "197380",
            "display": "Atorvastatin 10 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "308136",
            "display": "Amoxicillin 500 MG Oral Capsule",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "311989",
            "display": "Ibuprofen 200 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
        {
            "code": "197591",
            "display": "Hydrochlorothiazide 25 MG Oral Tablet",
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        },
    ]

    # Drug form codes
    DOSE_FORMS = [
        {"code": "385055001", "display": "Tablet", "system": "http://snomed.info/sct"},
        {"code": "385049006", "display": "Capsule", "system": "http://snomed.info/sct"},
        {"code": "385023001", "display": "Oral Solution", "system": "http://snomed.info/sct"},
        {"code": "385219001", "display": "Injectable Solution", "system": "http://snomed.info/sct"},
        {"code": "385101003", "display": "Cream", "system": "http://snomed.info/sct"},
    ]

    # Administration routes
    ROUTES = [
        {"code": "26643006", "display": "Oral", "system": "http://snomed.info/sct"},
        {"code": "47625008", "display": "Intravenous", "system": "http://snomed.info/sct"},
        {"code": "78421000", "display": "Intramuscular", "system": "http://snomed.info/sct"},
        {"code": "34206005", "display": "Subcutaneous", "system": "http://snomed.info/sct"},
        {"code": "6064005", "display": "Topical", "system": "http://snomed.info/sct"},
    ]

    # Status codes
    STATUS_CODES = ["active", "inactive", "entered-in-error"]

    # Characteristic types
    CHARACTERISTIC_TYPES = [
        {"code": "scoring", "display": "Scoring"},
        {"code": "coating", "display": "Coating"},
        {"code": "color", "display": "Color"},
        {"code": "shape", "display": "Shape"},
        {"code": "size", "display": "Size"},
        {"code": "imprint", "display": "Imprint"},
    ]

    # Manufacturers
    MANUFACTURERS = [
        "Pfizer",
        "Merck",
        "Novartis",
        "AstraZeneca",
        "Johnson & Johnson",
        "Roche",
        "Sanofi",
        "GlaxoSmithKline",
        "AbbVie",
        "Bristol-Myers Squibb",
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        knowledge_id: str | None = None,
        medication_code: str | None = None,
        manufacturer_ref: str | None = None,
        status: str = "active",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a MedicationKnowledge resource.

        Args:
            knowledge_id: Knowledge ID (generates UUID if None)
            medication_code: RxNorm medication code (random if None)
            manufacturer_ref: Reference to Organization (manufacturer)
            status: Knowledge record status

        Returns:
            MedicationKnowledge FHIR resource
        """
        if knowledge_id is None:
            knowledge_id = self._generate_id()

        # Select medication
        if medication_code is None:
            med = self.faker.random_element(self.MEDICATIONS)
        else:
            med = next(
                (m for m in self.MEDICATIONS if m["code"] == medication_code),
                self.MEDICATIONS[0],
            )

        dose_form = self.faker.random_element(self.DOSE_FORMS)
        route = self.faker.random_element(self.ROUTES)
        manufacturer = self.faker.random_element(self.MANUFACTURERS)

        # Generate costs
        unit_cost = round(self.faker.random.uniform(0.10, 50.00), 2)

        knowledge: dict[str, Any] = {
            "resourceType": "MedicationKnowledge",
            "id": knowledge_id,
            "meta": self._generate_meta(),
            "code": {
                "coding": [med],
                "text": med["display"],
            },
            "status": status,
            "doseForm": {
                "coding": [dose_form],
                "text": dose_form["display"],
            },
            "amount": {
                "value": self.faker.random_int(min=10, max=100),
                "unit": "tablets",
                "system": "http://unitsofmeasure.org",
                "code": "{tablet}",
            },
            "synonym": [med["display"].split()[0]],
            "intendedRoute": [
                {
                    "coding": [route],
                    "text": route["display"],
                }
            ],
            "cost": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-cost-type",
                                "code": "wholeSale",
                                "display": "Wholesale",
                            }
                        ]
                    },
                    "source": manufacturer,
                    "cost": {
                        "value": unit_cost,
                        "currency": "USD",
                    },
                }
            ],
            "monitoringProgram": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-monitoring",
                                "code": "drug-to-drug",
                                "display": "Drug-Drug Interaction",
                            }
                        ]
                    },
                    "name": "Drug Interaction Monitoring",
                }
            ],
            "administrationGuidelines": [
                {
                    "dosage": [
                        {
                            "type": {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-dosage",
                                        "code": "ordered",
                                        "display": "Ordered",
                                    }
                                ]
                            },
                            "dosage": [
                                {
                                    "text": (
                                        f"Take {self.faker.random_element(['1', '1-2', '2'])} tablet(s) "
                                        f"{self.faker.random_element(['once', 'twice', 'three times'])} daily"
                                    ),
                                }
                            ],
                        }
                    ],
                }
            ],
            "packaging": {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-package-type",
                            "code": "bot",
                            "display": "Bottle",
                        }
                    ]
                },
                "quantity": {
                    "value": self.faker.random_element([30, 60, 90, 100]),
                    "unit": "tablets",
                },
            },
            "drugCharacteristic": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-characteristic",
                                "code": "color",
                                "display": "Color",
                            }
                        ]
                    },
                    "valueString": self.faker.random_element(["white", "yellow", "pink", "blue", "orange"]),
                },
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/medicationknowledge-characteristic",
                                "code": "shape",
                                "display": "Shape",
                            }
                        ]
                    },
                    "valueString": self.faker.random_element(["round", "oval", "oblong", "capsule-shaped"]),
                },
            ],
        }

        if manufacturer_ref:
            knowledge["manufacturer"] = {"reference": manufacturer_ref}
        else:
            knowledge["manufacturer"] = {"display": manufacturer}

        return knowledge
