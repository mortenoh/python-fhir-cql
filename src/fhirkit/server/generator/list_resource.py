"""List resource generator."""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class ListGenerator(FHIRResourceGenerator):
    """Generator for FHIR List resources."""

    # List purpose codes
    PURPOSE_CODES = [
        {
            "code": "alerts",
            "display": "Alerts",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "adverserxns",
            "display": "Adverse Reactions",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "allergies",
            "display": "Allergies",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "medications",
            "display": "Medication List",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "problems",
            "display": "Problem List",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "worklist",
            "display": "Worklist",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "waiting",
            "display": "Waiting List",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "protocols",
            "display": "Protocols",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
        {
            "code": "plans",
            "display": "Care Plans",
            "system": "http://terminology.hl7.org/CodeSystem/list-example-use-codes",
        },
    ]

    # List modes
    MODES = ["working", "snapshot", "changes"]

    # Status codes
    STATUS_CODES = ["current", "retired", "entered-in-error"]

    # Empty reason codes
    EMPTY_REASONS = [
        {
            "code": "nilknown",
            "display": "Nil Known",
            "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason",
        },
        {
            "code": "notasked",
            "display": "Not Asked",
            "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason",
        },
        {
            "code": "withheld",
            "display": "Information Withheld",
            "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason",
        },
        {
            "code": "unavailable",
            "display": "Unavailable",
            "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason",
        },
        {
            "code": "notstarted",
            "display": "Not Started",
            "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason",
        },
        {"code": "closed", "display": "Closed", "system": "http://terminology.hl7.org/CodeSystem/list-empty-reason"},
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        list_id: str | None = None,
        patient_ref: str | None = None,
        encounter_ref: str | None = None,
        source_ref: str | None = None,
        entry_refs: list[str] | None = None,
        purpose: str | None = None,
        mode: str = "working",
        status: str = "current",
        title: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a List resource.

        Args:
            list_id: List ID (generates UUID if None)
            patient_ref: Reference to Patient (subject)
            encounter_ref: Reference to Encounter
            source_ref: Reference to creator (Practitioner/Patient/Device)
            entry_refs: List of references to include in the list
            purpose: List purpose code (random if None)
            mode: List mode (working, snapshot, changes)
            status: List status
            title: List title (auto-generated if None)

        Returns:
            List FHIR resource
        """
        if list_id is None:
            list_id = self._generate_id()

        # Select purpose
        if purpose is None:
            purpose_coding = self.faker.random_element(self.PURPOSE_CODES)
        else:
            purpose_coding = next(
                (p for p in self.PURPOSE_CODES if p["code"] == purpose),
                self.PURPOSE_CODES[0],
            )

        # Generate title
        if title is None:
            title = f"Patient {purpose_coding['display']}"

        # Generate date
        date = self._generate_datetime()

        list_resource: dict[str, Any] = {
            "resourceType": "List",
            "id": list_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/list-ids",
                    value=f"LIST-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "mode": mode,
            "title": title,
            "code": {
                "coding": [purpose_coding],
                "text": purpose_coding["display"],
            },
            "date": date,
            "orderedBy": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/list-order",
                        "code": "entry-date",
                        "display": "Sorted by Item Date",
                    }
                ]
            },
        }

        if patient_ref:
            list_resource["subject"] = {"reference": patient_ref}

        if encounter_ref:
            list_resource["encounter"] = {"reference": encounter_ref}

        if source_ref:
            list_resource["source"] = {"reference": source_ref}

        # Add entries
        if entry_refs and len(entry_refs) > 0:
            list_resource["entry"] = []
            for i, ref in enumerate(entry_refs):
                entry: dict[str, Any] = {
                    "item": {"reference": ref},
                }
                # Add optional date for some entries
                if self.faker.boolean(chance_of_getting_true=60):
                    entry["date"] = self._generate_datetime(start_date=datetime.now(timezone.utc) - timedelta(days=30))
                list_resource["entry"].append(entry)
        else:
            # Empty list - add reason
            empty_reason = self.faker.random_element(self.EMPTY_REASONS)
            list_resource["emptyReason"] = {
                "coding": [empty_reason],
                "text": empty_reason["display"],
            }

        return list_resource
