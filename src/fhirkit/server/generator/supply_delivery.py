"""SupplyDelivery resource generator."""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class SupplyDeliveryGenerator(FHIRResourceGenerator):
    """Generator for FHIR SupplyDelivery resources."""

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

    # Supply types
    SUPPLY_TYPES = [
        {
            "code": "medication",
            "display": "Medication",
            "system": "http://terminology.hl7.org/CodeSystem/supply-item-type",
        },
        {"code": "device", "display": "Device", "system": "http://terminology.hl7.org/CodeSystem/supply-item-type"},
    ]

    # Status codes
    STATUS_CODES = ["in-progress", "completed", "abandoned", "entered-in-error"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        delivery_id: str | None = None,
        patient_ref: str | None = None,
        supplier_ref: str | None = None,
        destination_ref: str | None = None,
        receiver_ref: str | None = None,
        based_on_ref: str | None = None,
        item_code: str | None = None,
        status: str = "completed",
        quantity: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a SupplyDelivery resource.

        Args:
            delivery_id: Delivery ID (generates UUID if None)
            patient_ref: Reference to Patient
            supplier_ref: Reference to Organization/Practitioner supplier
            destination_ref: Reference to Location destination
            receiver_ref: Reference to Practitioner receiver
            based_on_ref: Reference to SupplyRequest
            item_code: SNOMED CT item code (random if None)
            status: Delivery status
            quantity: Quantity delivered (random if None)

        Returns:
            SupplyDelivery FHIR resource
        """
        if delivery_id is None:
            delivery_id = self._generate_id()

        # Select item type
        if item_code is None:
            item = self.faker.random_element(self.ITEM_TYPES)
        else:
            item = next(
                (i for i in self.ITEM_TYPES if i["code"] == item_code),
                self.ITEM_TYPES[0],
            )

        supply_type = self.faker.random_element(self.SUPPLY_TYPES)

        # Generate quantity
        if quantity is None:
            quantity = self.faker.random_int(min=10, max=500)

        # Generate delivery datetime
        occurrence_datetime = self._generate_datetime(start_date=datetime.now(timezone.utc) - timedelta(days=7))

        delivery: dict[str, Any] = {
            "resourceType": "SupplyDelivery",
            "id": delivery_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/supply-delivery-ids",
                    value=f"SD-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "type": {
                "coding": [supply_type],
                "text": supply_type["display"],
            },
            "suppliedItem": {
                "quantity": {
                    "value": quantity,
                    "unit": "units",
                    "system": "http://unitsofmeasure.org",
                    "code": "{unit}",
                },
                "itemCodeableConcept": {
                    "coding": [item],
                    "text": item["display"],
                },
            },
            "occurrenceDateTime": occurrence_datetime,
        }

        if patient_ref:
            delivery["patient"] = {"reference": patient_ref}

        if supplier_ref:
            delivery["supplier"] = {"reference": supplier_ref}

        if destination_ref:
            delivery["destination"] = {"reference": destination_ref}

        if receiver_ref:
            delivery["receiver"] = [{"reference": receiver_ref}]

        if based_on_ref:
            delivery["basedOn"] = [{"reference": based_on_ref}]

        return delivery
