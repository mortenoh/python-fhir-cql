"""SupplyRequest resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class SupplyRequestGenerator(FHIRResourceGenerator):
    """Generator for FHIR SupplyRequest resources."""

    # Supply item types (SNOMED CT)
    ITEM_TYPES = [
        {"code": "468063009", "display": "Surgical mask", "system": "http://snomed.info/sct"},
        {"code": "469008007", "display": "Examination gloves", "system": "http://snomed.info/sct"},
        {"code": "102303004", "display": "Intravenous catheter", "system": "http://snomed.info/sct"},
        {"code": "61968008", "display": "Syringe", "system": "http://snomed.info/sct"},
        {"code": "118456007", "display": "Wound dressing", "system": "http://snomed.info/sct"},
        {"code": "19923001", "display": "Surgical gown", "system": "http://snomed.info/sct"},
        {"code": "469252005", "display": "Sterilized gauze", "system": "http://snomed.info/sct"},
        {"code": "465839001", "display": "Bandage", "system": "http://snomed.info/sct"},
        {"code": "425620007", "display": "Antiseptic wipe", "system": "http://snomed.info/sct"},
        {"code": "37299003", "display": "Glucose test strip", "system": "http://snomed.info/sct"},
    ]

    # Supply categories
    CATEGORIES = [
        {"code": "central", "display": "Central Supply", "system": "http://terminology.hl7.org/CodeSystem/supply-kind"},
        {"code": "nonstock", "display": "Non-Stock", "system": "http://terminology.hl7.org/CodeSystem/supply-kind"},
    ]

    # Status codes
    STATUS_CODES = ["draft", "active", "suspended", "cancelled", "completed", "entered-in-error", "unknown"]

    # Priority codes
    PRIORITIES = ["routine", "urgent", "asap", "stat"]

    # Reason codes
    REASON_CODES = [
        {
            "code": "patient-care",
            "display": "Patient Care",
            "system": "http://terminology.hl7.org/CodeSystem/supplyrequest-reason",
        },
        {
            "code": "ward-stock",
            "display": "Ward Stock",
            "system": "http://terminology.hl7.org/CodeSystem/supplyrequest-reason",
        },
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        request_id: str | None = None,
        patient_ref: str | None = None,
        requester_ref: str | None = None,
        supplier_ref: str | None = None,
        deliver_to_ref: str | None = None,
        item_code: str | None = None,
        status: str = "active",
        priority: str = "routine",
        quantity: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a SupplyRequest resource.

        Args:
            request_id: Request ID (generates UUID if None)
            patient_ref: Reference to Patient (optional, for patient-specific supplies)
            requester_ref: Reference to Practitioner/Organization requester
            supplier_ref: Reference to Organization supplier
            deliver_to_ref: Reference to Location/Organization for delivery
            item_code: SNOMED CT item code (random if None)
            status: Request status
            priority: Request priority
            quantity: Quantity requested (random if None)

        Returns:
            SupplyRequest FHIR resource
        """
        if request_id is None:
            request_id = self._generate_id()

        # Select item type
        if item_code is None:
            item = self.faker.random_element(self.ITEM_TYPES)
        else:
            item = next(
                (i for i in self.ITEM_TYPES if i["code"] == item_code),
                self.ITEM_TYPES[0],
            )

        category = self.faker.random_element(self.CATEGORIES)
        reason = self.faker.random_element(self.REASON_CODES)

        # Generate quantity
        if quantity is None:
            quantity = self.faker.random_int(min=10, max=500)

        # Generate dates
        authored_on = self._generate_datetime()
        occurrence_date = self._generate_date(start_date=date.today(), end_date=date.today() + timedelta(days=7))

        request: dict[str, Any] = {
            "resourceType": "SupplyRequest",
            "id": request_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/supply-request-ids",
                    value=f"SR-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "priority": priority,
            "category": {
                "coding": [category],
                "text": category["display"],
            },
            "itemCodeableConcept": {
                "coding": [item],
                "text": item["display"],
            },
            "quantity": {
                "value": quantity,
                "unit": "units",
                "system": "http://unitsofmeasure.org",
                "code": "{unit}",
            },
            "occurrenceDateTime": occurrence_date,
            "authoredOn": authored_on,
            "reasonCode": [
                {
                    "coding": [reason],
                    "text": reason["display"],
                }
            ],
        }

        if patient_ref:
            # For patient-specific supplies
            request["deliverFrom"] = {"display": "Central Supply"}
            request["deliverTo"] = {"reference": patient_ref}
        elif deliver_to_ref:
            request["deliverTo"] = {"reference": deliver_to_ref}

        if requester_ref:
            request["requester"] = {"reference": requester_ref}

        if supplier_ref:
            request["supplier"] = [{"reference": supplier_ref}]

        return request
