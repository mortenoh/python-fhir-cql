"""EpisodeOfCare resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class EpisodeOfCareGenerator(FHIRResourceGenerator):
    """Generator for FHIR EpisodeOfCare resources."""

    # Episode types
    TYPES = [
        {
            "code": "hacc",
            "display": "Home and Community Care",
            "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        },
        {
            "code": "pac",
            "display": "Post Acute Care",
            "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        },
        {
            "code": "diab",
            "display": "Post Coordinated Diabetes Program",
            "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        },
        {
            "code": "da",
            "display": "Drug and Alcohol Program",
            "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        },
        {
            "code": "cacp",
            "display": "Community-based Aged Care Package",
            "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
        },
    ]

    # Diagnosis roles
    DIAGNOSIS_ROLES = [
        {"code": "CC", "display": "Chief complaint", "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role"},
        {
            "code": "AD",
            "display": "Admission diagnosis",
            "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role",
        },
        {
            "code": "DD",
            "display": "Discharge diagnosis",
            "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role",
        },
    ]

    # Status codes
    STATUS_CODES = ["planned", "waitlist", "active", "onhold", "finished", "cancelled", "entered-in-error"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        episode_id: str | None = None,
        patient_ref: str | None = None,
        managing_org_ref: str | None = None,
        care_manager_ref: str | None = None,
        condition_ref: str | None = None,
        care_team_ref: str | None = None,
        episode_type: str | None = None,
        status: str = "active",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate an EpisodeOfCare resource.

        Args:
            episode_id: Episode ID (generates UUID if None)
            patient_ref: Reference to Patient
            managing_org_ref: Reference to managing Organization
            care_manager_ref: Reference to Practitioner care manager
            condition_ref: Reference to Condition for diagnosis
            care_team_ref: Reference to CareTeam
            episode_type: Episode type code (random if None)
            status: Episode status

        Returns:
            EpisodeOfCare FHIR resource
        """
        if episode_id is None:
            episode_id = self._generate_id()

        # Select type
        if episode_type is None:
            type_coding = self.faker.random_element(self.TYPES)
        else:
            type_coding = next(
                (t for t in self.TYPES if t["code"] == episode_type),
                self.TYPES[0],
            )

        # Generate period
        start_date = self._generate_date(start_date=date.today() - timedelta(days=180))
        period: dict[str, str] = {"start": start_date}
        if status in ["finished", "cancelled"]:
            period["end"] = self._generate_date(start_date=date.today() - timedelta(days=30))

        episode: dict[str, Any] = {
            "resourceType": "EpisodeOfCare",
            "id": episode_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/episode-ids",
                    value=f"EP-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "statusHistory": [
                {
                    "status": "planned",
                    "period": {"start": start_date},
                }
            ],
            "type": [
                {
                    "coding": [type_coding],
                    "text": type_coding["display"],
                }
            ],
            "period": period,
        }

        if patient_ref:
            episode["patient"] = {"reference": patient_ref}

        if managing_org_ref:
            episode["managingOrganization"] = {"reference": managing_org_ref}

        if care_manager_ref:
            episode["careManager"] = {"reference": care_manager_ref}

        if condition_ref:
            diagnosis_role = self.faker.random_element(self.DIAGNOSIS_ROLES)
            episode["diagnosis"] = [
                {
                    "condition": {"reference": condition_ref},
                    "role": {
                        "coding": [diagnosis_role],
                        "text": diagnosis_role["display"],
                    },
                    "rank": 1,
                }
            ]

        if care_team_ref:
            episode["team"] = [{"reference": care_team_ref}]

        return episode
