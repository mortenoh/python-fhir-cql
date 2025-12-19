"""ResearchStudy resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class ResearchStudyGenerator(FHIRResourceGenerator):
    """Generator for FHIR ResearchStudy resources."""

    # Study phases
    PHASES = [
        {"code": "n-a", "display": "N/A", "system": "http://terminology.hl7.org/CodeSystem/research-study-phase"},
        {
            "code": "early-phase-1",
            "display": "Early Phase 1",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-1",
            "display": "Phase 1",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-1-phase-2",
            "display": "Phase 1/Phase 2",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-2",
            "display": "Phase 2",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-2-phase-3",
            "display": "Phase 2/Phase 3",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-3",
            "display": "Phase 3",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
        {
            "code": "phase-4",
            "display": "Phase 4",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-phase",
        },
    ]

    # Study statuses
    STATUS_CODES = [
        "active",
        "administratively-completed",
        "approved",
        "closed-to-accrual",
        "closed-to-accrual-and-intervention",
        "completed",
        "disapproved",
        "in-review",
        "temporarily-closed-to-accrual",
        "temporarily-closed-to-accrual-and-intervention",
        "withdrawn",
    ]

    # Primary purpose types
    PRIMARY_PURPOSES = [
        {
            "code": "treatment",
            "display": "Treatment",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "prevention",
            "display": "Prevention",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "diagnostic",
            "display": "Diagnostic",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "supportive-care",
            "display": "Supportive Care",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "screening",
            "display": "Screening",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "health-services-research",
            "display": "Health Services Research",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "basic-science",
            "display": "Basic Science",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
        {
            "code": "device-feasibility",
            "display": "Device Feasibility",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type",
        },
    ]

    # Categories
    CATEGORIES = [
        {
            "code": "C98388",
            "display": "Interventional",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-category",
        },
        {
            "code": "C16084",
            "display": "Observational",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-category",
        },
        {
            "code": "C142615",
            "display": "Expanded Access",
            "system": "http://terminology.hl7.org/CodeSystem/research-study-category",
        },
    ]

    # Focus conditions (SNOMED CT)
    CONDITIONS = [
        {"code": "73211009", "display": "Diabetes mellitus", "system": "http://snomed.info/sct"},
        {"code": "38341003", "display": "Hypertensive disorder", "system": "http://snomed.info/sct"},
        {"code": "254837009", "display": "Malignant neoplasm of breast", "system": "http://snomed.info/sct"},
        {"code": "13645005", "display": "Chronic obstructive lung disease", "system": "http://snomed.info/sct"},
        {"code": "84757009", "display": "Epilepsy", "system": "http://snomed.info/sct"},
        {"code": "35489007", "display": "Depressive disorder", "system": "http://snomed.info/sct"},
        {"code": "195967001", "display": "Asthma", "system": "http://snomed.info/sct"},
        {"code": "22298006", "display": "Myocardial infarction", "system": "http://snomed.info/sct"},
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        study_id: str | None = None,
        sponsor_ref: str | None = None,
        principal_investigator_ref: str | None = None,
        site_refs: list[str] | None = None,
        phase: str | None = None,
        status: str = "active",
        title: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a ResearchStudy resource.

        Args:
            study_id: Study ID (generates UUID if None)
            sponsor_ref: Reference to sponsoring Organization
            principal_investigator_ref: Reference to Practitioner PI
            site_refs: List of references to study site Locations
            phase: Study phase code (random if None)
            status: Study status
            title: Study title (auto-generated if None)

        Returns:
            ResearchStudy FHIR resource
        """
        if study_id is None:
            study_id = self._generate_id()

        # Select phase
        if phase is None:
            phase_coding = self.faker.random_element(self.PHASES)
        else:
            phase_coding = next(
                (p for p in self.PHASES if p["code"] == phase),
                self.PHASES[0],
            )

        purpose = self.faker.random_element(self.PRIMARY_PURPOSES)
        category = self.faker.random_element(self.CATEGORIES)
        condition = self.faker.random_element(self.CONDITIONS)

        # Generate study identifiers
        nct_number = f"NCT{self.faker.numerify('########')}"

        # Generate title
        if title is None:
            title = f"A {phase_coding['display']} {category['display']} Study of {condition['display']}"

        # Generate dates
        start_date = self._generate_date(start_date=date.today() - timedelta(days=365))

        study: dict[str, Any] = {
            "resourceType": "ResearchStudy",
            "id": study_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://clinicaltrials.gov",
                    value=nct_number,
                ),
                self._generate_identifier(
                    system="http://example.org/study-ids",
                    value=f"STUDY-{self.faker.numerify('####')}",
                ),
            ],
            "title": title,
            "status": status,
            "primaryPurposeType": {
                "coding": [purpose],
                "text": purpose["display"],
            },
            "phase": {
                "coding": [phase_coding],
                "text": phase_coding["display"],
            },
            "category": [
                {
                    "coding": [category],
                    "text": category["display"],
                }
            ],
            "focus": [
                {
                    "coding": [condition],
                    "text": condition["display"],
                }
            ],
            "condition": [
                {
                    "coding": [condition],
                    "text": condition["display"],
                }
            ],
            "description": (
                f"This is a {phase_coding['display']} {category['display'].lower()} study "
                f"investigating {condition['display'].lower()}."
            ),
            "enrollment": [
                {
                    "display": f"Target enrollment: {self.faker.random_int(min=50, max=500)} participants",
                }
            ],
            "period": {
                "start": start_date,
            },
            "arm": [
                {
                    "name": "Treatment Arm",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/research-study-arm-type",
                                "code": "experimental",
                                "display": "Experimental",
                            }
                        ]
                    },
                    "description": "Participants receiving the experimental intervention",
                },
                {
                    "name": "Control Arm",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/research-study-arm-type",
                                "code": "placebo-comparator",
                                "display": "Placebo Comparator",
                            }
                        ]
                    },
                    "description": "Participants receiving placebo",
                },
            ],
            "objective": [
                {
                    "name": "Primary Objective",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/research-study-objective-type",
                                "code": "primary",
                                "display": "Primary",
                            }
                        ]
                    },
                }
            ],
        }

        if sponsor_ref:
            study["sponsor"] = {"reference": sponsor_ref}

        if principal_investigator_ref:
            study["principalInvestigator"] = {"reference": principal_investigator_ref}

        if site_refs:
            study["site"] = [{"reference": ref} for ref in site_refs]

        return study
