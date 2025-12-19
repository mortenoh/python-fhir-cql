"""BodyStructure resource generator."""

from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class BodyStructureGenerator(FHIRResourceGenerator):
    """Generator for FHIR BodyStructure resources."""

    # Body locations (SNOMED CT)
    LOCATIONS = [
        {"code": "39937001", "display": "Skin", "system": "http://snomed.info/sct"},
        {"code": "71341001", "display": "Bone", "system": "http://snomed.info/sct"},
        {"code": "181268008", "display": "Lung", "system": "http://snomed.info/sct"},
        {"code": "10200004", "display": "Liver", "system": "http://snomed.info/sct"},
        {"code": "64033007", "display": "Kidney", "system": "http://snomed.info/sct"},
        {"code": "80891009", "display": "Heart", "system": "http://snomed.info/sct"},
        {"code": "15497006", "display": "Ovary", "system": "http://snomed.info/sct"},
        {"code": "13648007", "display": "Prostate", "system": "http://snomed.info/sct"},
        {"code": "76752008", "display": "Breast", "system": "http://snomed.info/sct"},
        {"code": "69536005", "display": "Head", "system": "http://snomed.info/sct"},
    ]

    # Morphology types (SNOMED CT)
    MORPHOLOGIES = [
        {"code": "4147007", "display": "Mass", "system": "http://snomed.info/sct"},
        {"code": "339008", "display": "Blister", "system": "http://snomed.info/sct"},
        {"code": "56208002", "display": "Ulcer", "system": "http://snomed.info/sct"},
        {"code": "125568002", "display": "Cyst", "system": "http://snomed.info/sct"},
        {"code": "86273004", "display": "Lesion", "system": "http://snomed.info/sct"},
        {"code": "414722000", "display": "Nodule", "system": "http://snomed.info/sct"},
        {"code": "73573004", "display": "Polyp", "system": "http://snomed.info/sct"},
        {"code": "21239007", "display": "Implant", "system": "http://snomed.info/sct"},
        {"code": "18659000", "display": "Grafted tissue", "system": "http://snomed.info/sct"},
        {"code": "108369006", "display": "Tumor", "system": "http://snomed.info/sct"},
    ]

    # Laterality
    LATERALITY = [
        {"code": "419161000", "display": "Unilateral left", "system": "http://snomed.info/sct"},
        {"code": "419465000", "display": "Unilateral right", "system": "http://snomed.info/sct"},
        {"code": "51440002", "display": "Bilateral", "system": "http://snomed.info/sct"},
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        structure_id: str | None = None,
        patient_ref: str | None = None,
        location_code: str | None = None,
        morphology_code: str | None = None,
        active: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a BodyStructure resource.

        Args:
            structure_id: Structure ID (generates UUID if None)
            patient_ref: Reference to Patient
            location_code: SNOMED CT location code (random if None)
            morphology_code: SNOMED CT morphology code (random if None)
            active: Whether the structure record is active

        Returns:
            BodyStructure FHIR resource
        """
        if structure_id is None:
            structure_id = self._generate_id()

        # Select location
        if location_code is None:
            location = self.faker.random_element(self.LOCATIONS)
        else:
            location = next(
                (loc for loc in self.LOCATIONS if loc["code"] == location_code),
                self.LOCATIONS[0],
            )

        # Select morphology
        if morphology_code is None:
            morphology = self.faker.random_element(self.MORPHOLOGIES)
        else:
            morphology = next(
                (m for m in self.MORPHOLOGIES if m["code"] == morphology_code),
                self.MORPHOLOGIES[0],
            )

        laterality = self.faker.random_element(self.LATERALITY)

        structure: dict[str, Any] = {
            "resourceType": "BodyStructure",
            "id": structure_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/body-structure-ids",
                    value=f"BS-{self.faker.numerify('########')}",
                ),
            ],
            "active": active,
            "morphology": {
                "coding": [morphology],
                "text": morphology["display"],
            },
            "location": {
                "coding": [location],
                "text": location["display"],
            },
            "locationQualifier": [
                {
                    "coding": [laterality],
                    "text": laterality["display"],
                }
            ],
            "description": f"{morphology['display']} located in {location['display']} ({laterality['display']})",
        }

        if patient_ref:
            structure["patient"] = {"reference": patient_ref}

        # Add image if morphology is visible
        if morphology["code"] in ["4147007", "56208002", "86273004", "414722000"]:
            structure["image"] = [
                {
                    "contentType": "image/jpeg",
                    "title": f"Image of {morphology['display']}",
                }
            ]

        return structure
