"""RequestGroup resource generator."""

from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class RequestGroupGenerator(FHIRResourceGenerator):
    """Generator for FHIR RequestGroup resources."""

    # Request group codes (order sets)
    GROUP_CODES = [
        {
            "code": "chronic-pain-protocol",
            "display": "Chronic Pain Management Protocol",
            "system": "http://example.org/orderset",
        },
        {"code": "diabetes-care-bundle", "display": "Diabetes Care Bundle", "system": "http://example.org/orderset"},
        {"code": "sepsis-bundle", "display": "Sepsis Management Bundle", "system": "http://example.org/orderset"},
        {"code": "cardiac-workup", "display": "Cardiac Workup Order Set", "system": "http://example.org/orderset"},
        {"code": "preop-clearance", "display": "Pre-operative Clearance", "system": "http://example.org/orderset"},
        {"code": "discharge-bundle", "display": "Discharge Order Bundle", "system": "http://example.org/orderset"},
        {"code": "admission-orders", "display": "Admission Order Set", "system": "http://example.org/orderset"},
        {
            "code": "medication-reconciliation",
            "display": "Medication Reconciliation",
            "system": "http://example.org/orderset",
        },
    ]

    # Status codes
    STATUS_CODES = ["draft", "active", "on-hold", "revoked", "completed", "entered-in-error", "unknown"]

    # Intent codes
    INTENTS = [
        "proposal",
        "plan",
        "directive",
        "order",
        "original-order",
        "reflex-order",
        "filler-order",
        "instance-order",
        "option",
    ]

    # Priority codes
    PRIORITIES = ["routine", "urgent", "asap", "stat"]

    # Action selection behavior
    SELECTION_BEHAVIORS = ["any", "all", "all-or-none", "exactly-one", "at-most-one", "one-or-more"]

    # Action grouping behavior
    GROUPING_BEHAVIORS = ["visual-group", "logical-group", "sentence-group"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        group_id: str | None = None,
        patient_ref: str | None = None,
        encounter_ref: str | None = None,
        author_ref: str | None = None,
        action_refs: list[str] | None = None,
        group_code: str | None = None,
        status: str = "active",
        intent: str = "order",
        priority: str = "routine",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a RequestGroup resource.

        Args:
            group_id: Group ID (generates UUID if None)
            patient_ref: Reference to Patient (subject)
            encounter_ref: Reference to Encounter
            author_ref: Reference to author (Practitioner/Device)
            action_refs: List of references to actions (ServiceRequest, MedicationRequest, etc.)
            group_code: Group code (random if None)
            status: Group status
            intent: Group intent
            priority: Group priority

        Returns:
            RequestGroup FHIR resource
        """
        if group_id is None:
            group_id = self._generate_id()

        # Select group code
        if group_code is None:
            code_obj = self.faker.random_element(self.GROUP_CODES)
        else:
            code_obj = next(
                (c for c in self.GROUP_CODES if c["code"] == group_code),
                self.GROUP_CODES[0],
            )

        # Generate dates
        authored_on = self._generate_datetime()

        group: dict[str, Any] = {
            "resourceType": "RequestGroup",
            "id": group_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/request-group-ids",
                    value=f"RG-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "intent": intent,
            "priority": priority,
            "code": {
                "coding": [code_obj],
                "text": code_obj["display"],
            },
            "authoredOn": authored_on,
        }

        if patient_ref:
            group["subject"] = {"reference": patient_ref}

        if encounter_ref:
            group["encounter"] = {"reference": encounter_ref}

        if author_ref:
            group["author"] = {"reference": author_ref}

        # Add actions
        if action_refs and len(action_refs) > 0:
            selection_behavior = self.faker.random_element(self.SELECTION_BEHAVIORS)
            group["action"] = []

            for i, ref in enumerate(action_refs):
                action: dict[str, Any] = {
                    "prefix": str(i + 1),
                    "title": f"Action {i + 1}",
                    "description": f"Step {i + 1} of {code_obj['display']}",
                    "priority": self.faker.random_element(self.PRIORITIES),
                    "resource": {"reference": ref},
                }

                # Add timing for some actions
                if self.faker.boolean(chance_of_getting_true=40):
                    action["timingDuration"] = {
                        "value": self.faker.random_int(min=1, max=48),
                        "unit": "h",
                        "system": "http://unitsofmeasure.org",
                        "code": "h",
                    }

                group["action"].append(action)

            # Set selection behavior at group level
            if len(action_refs) > 1:
                group["action"][0]["selectionBehavior"] = selection_behavior
        else:
            # Add placeholder action when no resources provided
            group["action"] = [
                {
                    "title": code_obj["display"],
                    "description": f"Order set for {code_obj['display'].lower()}",
                    "selectionBehavior": "all",
                    "action": [
                        {
                            "prefix": "1",
                            "title": "Initial Assessment",
                            "description": "Perform initial patient assessment",
                        },
                        {
                            "prefix": "2",
                            "title": "Lab Orders",
                            "description": "Order required laboratory tests",
                        },
                        {
                            "prefix": "3",
                            "title": "Medication Orders",
                            "description": "Prescribe required medications",
                        },
                    ],
                }
            ]

        return group
