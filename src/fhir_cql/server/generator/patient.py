"""Patient resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class PatientGenerator(FHIRResourceGenerator):
    """Generator for FHIR Patient resources."""

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        patient_id: str | None = None,
        gender: str | None = None,
        birth_date: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a Patient resource.

        Args:
            patient_id: Patient ID (generates UUID if None)
            gender: Patient gender (random if None)
            birth_date: Birth date (random if None)

        Returns:
            Patient FHIR resource
        """
        if patient_id is None:
            patient_id = self._generate_id()

        if gender is None:
            gender = self.faker.random_element(["male", "female"])

        # Generate appropriate name based on gender
        if gender == "male":
            first_name = self.faker.first_name_male()
        else:
            first_name = self.faker.first_name_female()

        last_name = self.faker.last_name()

        # Generate birth date with realistic age distribution
        if birth_date is None:
            # Age distribution: more adults, fewer children and elderly
            age_weights = [
                (0, 18, 0.15),  # Children: 15%
                (18, 40, 0.25),  # Young adults: 25%
                (40, 65, 0.35),  # Middle aged: 35%
                (65, 90, 0.25),  # Elderly: 25%
            ]

            roll = self.faker.random.random()
            cumulative = 0.0
            min_age, max_age = 18, 65

            for age_min, age_max, weight in age_weights:
                cumulative += weight
                if roll < cumulative:
                    min_age, max_age = age_min, age_max
                    break

            today = date.today()
            start_date = today - timedelta(days=max_age * 365)
            end_date = today - timedelta(days=min_age * 365)
            birth_date = self._generate_date(start_date, end_date)

        # Generate MRN
        mrn = self.faker.numerify("MRN########")

        patient: dict[str, Any] = {
            "resourceType": "Patient",
            "id": patient_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://hospital.example.org/mrn",
                    value=mrn,
                    type_code="MR",
                    type_display="Medical Record Number",
                ),
                self._generate_identifier(
                    system="http://hl7.org/fhir/sid/us-ssn",
                    value=self.faker.ssn(),
                    type_code="SS",
                    type_display="Social Security Number",
                ),
            ],
            "active": True,
            "name": [
                self._generate_human_name(
                    family=last_name,
                    given=[first_name, self.faker.first_name()[0] + "."],
                )
            ],
            "telecom": [
                self._generate_contact_point("phone", use="home"),
                self._generate_contact_point("phone", use="mobile"),
                self._generate_contact_point("email"),
            ],
            "gender": gender,
            "birthDate": birth_date,
            "address": [self._generate_address()],
            "maritalStatus": self._generate_marital_status(),
            "communication": [
                {
                    "language": {
                        "coding": [
                            {
                                "system": "urn:ietf:bcp:47",
                                "code": "en-US",
                                "display": "English (United States)",
                            }
                        ],
                        "text": "English",
                    },
                    "preferred": True,
                }
            ],
        }

        # Add extensions for US Core
        patient["extension"] = self._generate_us_core_extensions()

        return patient

    def _generate_marital_status(self) -> dict[str, Any]:
        """Generate marital status."""
        statuses = [
            ("S", "Never Married", 0.3),
            ("M", "Married", 0.5),
            ("D", "Divorced", 0.1),
            ("W", "Widowed", 0.1),
        ]

        roll = self.faker.random.random()
        cumulative = 0.0
        code, display = "S", "Never Married"

        for c, d, weight in statuses:
            cumulative += weight
            if roll < cumulative:
                code, display = c, d
                break

        return {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                    "code": code,
                    "display": display,
                }
            ],
            "text": display,
        }

    def _generate_us_core_extensions(self) -> list[dict[str, Any]]:
        """Generate US Core race and ethnicity extensions."""
        extensions = []

        # Race extension
        races = [
            ("2106-3", "White", 0.6),
            ("2054-5", "Black or African American", 0.13),
            ("2028-9", "Asian", 0.06),
            ("1002-5", "American Indian or Alaska Native", 0.01),
            ("2076-8", "Native Hawaiian or Other Pacific Islander", 0.002),
            ("2131-1", "Other Race", 0.19),
        ]

        roll = self.faker.random.random()
        cumulative = 0.0
        race_code, race_display = "2106-3", "White"

        for code, display, weight in races:
            cumulative += weight
            if roll < cumulative:
                race_code, race_display = code, display
                break

        extensions.append(
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                "extension": [
                    {
                        "url": "ombCategory",
                        "valueCoding": {
                            "system": "urn:oid:2.16.840.1.113883.6.238",
                            "code": race_code,
                            "display": race_display,
                        },
                    },
                    {"url": "text", "valueString": race_display},
                ],
            }
        )

        # Ethnicity extension
        is_hispanic = self.faker.random.random() < 0.18  # ~18% Hispanic

        if is_hispanic:
            eth_code, eth_display = "2135-2", "Hispanic or Latino"
        else:
            eth_code, eth_display = "2186-5", "Not Hispanic or Latino"

        extensions.append(
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                "extension": [
                    {
                        "url": "ombCategory",
                        "valueCoding": {
                            "system": "urn:oid:2.16.840.1.113883.6.238",
                            "code": eth_code,
                            "display": eth_display,
                        },
                    },
                    {"url": "text", "valueString": eth_display},
                ],
            }
        )

        return extensions
