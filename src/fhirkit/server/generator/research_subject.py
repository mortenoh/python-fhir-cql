"""ResearchSubject resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class ResearchSubjectGenerator(FHIRResourceGenerator):
    """Generator for FHIR ResearchSubject resources."""

    # Subject statuses
    STATUS_CODES = [
        "candidate",
        "eligible",
        "follow-up",
        "ineligible",
        "not-registered",
        "off-study",
        "on-study",
        "on-study-intervention",
        "on-study-observation",
        "pending-on-study",
        "potential-candidate",
        "screening",
        "withdrawn",
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        subject_id: str | None = None,
        patient_ref: str | None = None,
        study_ref: str | None = None,
        consent_ref: str | None = None,
        status: str = "on-study",
        assigned_arm: str | None = None,
        actual_arm: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a ResearchSubject resource.

        Args:
            subject_id: Subject ID (generates UUID if None)
            patient_ref: Reference to Patient (individual)
            study_ref: Reference to ResearchStudy
            consent_ref: Reference to Consent
            status: Subject status
            assigned_arm: Study arm assigned to subject
            actual_arm: Study arm subject is actually in

        Returns:
            ResearchSubject FHIR resource
        """
        if subject_id is None:
            subject_id = self._generate_id()

        # Generate study-specific identifier
        study_subject_id = f"SUBJ-{self.faker.numerify('####')}"

        # Generate dates
        period_start = self._generate_date(start_date=date.today() - timedelta(days=90))

        subject: dict[str, Any] = {
            "resourceType": "ResearchSubject",
            "id": subject_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/research-subject-ids",
                    value=study_subject_id,
                ),
            ],
            "status": status,
            "period": {
                "start": period_start,
            },
        }

        if patient_ref:
            subject["individual"] = {"reference": patient_ref}

        if study_ref:
            subject["study"] = {"reference": study_ref}

        if consent_ref:
            subject["consent"] = {"reference": consent_ref}

        # Assign study arm
        if assigned_arm is None:
            assigned_arm = self.faker.random_element(["Treatment Arm", "Control Arm", "Arm A", "Arm B"])

        subject["assignedArm"] = assigned_arm

        # Actual arm (may differ from assigned if subject crosses over)
        if actual_arm is None:
            # 90% chance actual arm matches assigned arm
            if self.faker.boolean(chance_of_getting_true=90):
                actual_arm = assigned_arm
            else:
                actual_arm = self.faker.random_element(["Treatment Arm", "Control Arm", "Arm A", "Arm B"])

        subject["actualArm"] = actual_arm

        # Add period end for completed/withdrawn subjects
        if status in ["off-study", "withdrawn", "follow-up"]:
            subject["period"]["end"] = self._generate_date(start_date=date.today() - timedelta(days=30))

        return subject
