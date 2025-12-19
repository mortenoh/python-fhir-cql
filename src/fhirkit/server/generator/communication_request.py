"""CommunicationRequest resource generator."""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class CommunicationRequestGenerator(FHIRResourceGenerator):
    """Generator for FHIR CommunicationRequest resources."""

    # Communication categories
    CATEGORIES = [
        {"code": "alert", "display": "Alert", "system": "http://terminology.hl7.org/CodeSystem/communication-category"},
        {
            "code": "notification",
            "display": "Notification",
            "system": "http://terminology.hl7.org/CodeSystem/communication-category",
        },
        {
            "code": "reminder",
            "display": "Reminder",
            "system": "http://terminology.hl7.org/CodeSystem/communication-category",
        },
        {
            "code": "instruction",
            "display": "Instruction",
            "system": "http://terminology.hl7.org/CodeSystem/communication-category",
        },
    ]

    # Medium codes
    MEDIUMS = [
        {
            "code": "WRITTEN",
            "display": "Written",
            "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode",
        },
        {"code": "VERBAL", "display": "Verbal", "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode"},
        {
            "code": "PHONE",
            "display": "Telephone",
            "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode",
        },
        {
            "code": "EMAILWRIT",
            "display": "Email",
            "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode",
        },
        {"code": "FAXWRIT", "display": "Fax", "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationMode"},
    ]

    # Priority codes
    PRIORITIES = ["routine", "urgent", "asap", "stat"]

    # Status codes
    STATUS_CODES = ["draft", "active", "on-hold", "revoked", "completed", "entered-in-error", "unknown"]

    # Reason codes (SNOMED CT)
    REASON_CODES = [
        {"code": "310385006", "display": "Appointment reminder", "system": "http://snomed.info/sct"},
        {"code": "308540004", "display": "Laboratory results", "system": "http://snomed.info/sct"},
        {"code": "183685000", "display": "Medication reminder", "system": "http://snomed.info/sct"},
        {"code": "305896008", "display": "Patient education", "system": "http://snomed.info/sct"},
        {"code": "385763009", "display": "Referral request", "system": "http://snomed.info/sct"},
        {"code": "225358003", "display": "Care coordination", "system": "http://snomed.info/sct"},
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        request_id: str | None = None,
        patient_ref: str | None = None,
        encounter_ref: str | None = None,
        requester_ref: str | None = None,
        recipient_refs: list[str] | None = None,
        sender_ref: str | None = None,
        about_refs: list[str] | None = None,
        category: str | None = None,
        priority: str = "routine",
        status: str = "active",
        message: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a CommunicationRequest resource.

        Args:
            request_id: Request ID (generates UUID if None)
            patient_ref: Reference to Patient (subject)
            encounter_ref: Reference to Encounter
            requester_ref: Reference to requester (Practitioner/Organization)
            recipient_refs: List of references to recipients
            sender_ref: Reference to intended sender
            about_refs: List of references this is about
            category: Communication category code (random if None)
            priority: Request priority
            status: Request status
            message: Message content (auto-generated if None)

        Returns:
            CommunicationRequest FHIR resource
        """
        if request_id is None:
            request_id = self._generate_id()

        # Select category
        if category is None:
            category_coding = self.faker.random_element(self.CATEGORIES)
        else:
            category_coding = next(
                (c for c in self.CATEGORIES if c["code"] == category),
                self.CATEGORIES[0],
            )

        medium = self.faker.random_element(self.MEDIUMS)
        reason = self.faker.random_element(self.REASON_CODES)

        # Generate dates
        authored_on = self._generate_datetime()

        # Generate message
        if message is None:
            message_templates = [
                f"Please contact the patient regarding {reason['display'].lower()}.",
                f"Reminder: {reason['display']} - follow-up required.",
                f"Notification regarding {reason['display']}.",
                f"Action required: {reason['display']}.",
            ]
            message = self.faker.random_element(message_templates)

        request: dict[str, Any] = {
            "resourceType": "CommunicationRequest",
            "id": request_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/communication-request-ids",
                    value=f"CR-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "priority": priority,
            "category": [
                {
                    "coding": [category_coding],
                    "text": category_coding["display"],
                }
            ],
            "medium": [
                {
                    "coding": [medium],
                    "text": medium["display"],
                }
            ],
            "authoredOn": authored_on,
            "reasonCode": [
                {
                    "coding": [reason],
                    "text": reason["display"],
                }
            ],
            "payload": [
                {
                    "contentString": message,
                }
            ],
        }

        if patient_ref:
            request["subject"] = {"reference": patient_ref}

        if encounter_ref:
            request["encounter"] = {"reference": encounter_ref}

        if requester_ref:
            request["requester"] = {"reference": requester_ref}

        if recipient_refs:
            request["recipient"] = [{"reference": ref} for ref in recipient_refs]

        if sender_ref:
            request["sender"] = {"reference": sender_ref}

        if about_refs:
            request["about"] = [{"reference": ref} for ref in about_refs]

        # Add occurrence if scheduled for future
        if status in ["active", "draft"]:
            now = datetime.now(timezone.utc)
            request["occurrenceDateTime"] = self._generate_datetime(start_date=now, end_date=now + timedelta(days=7))

        return request
