"""ImagingStudy resource generator."""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class ImagingStudyGenerator(FHIRResourceGenerator):
    """Generator for FHIR ImagingStudy resources."""

    # DICOM Modalities
    MODALITIES = [
        {"code": "CT", "display": "Computed Tomography", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "MR", "display": "Magnetic Resonance", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "US", "display": "Ultrasound", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "DX", "display": "Digital Radiography", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "CR", "display": "Computed Radiography", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "NM", "display": "Nuclear Medicine", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {
            "code": "PT",
            "display": "Positron Emission Tomography",
            "system": "http://dicom.nema.org/resources/ontology/DCM",
        },
        {"code": "XA", "display": "X-Ray Angiography", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "MG", "display": "Mammography", "system": "http://dicom.nema.org/resources/ontology/DCM"},
        {"code": "ES", "display": "Endoscopy", "system": "http://dicom.nema.org/resources/ontology/DCM"},
    ]

    # Body Sites (SNOMED CT)
    BODY_SITES = [
        {"code": "51185008", "display": "Thorax", "system": "http://snomed.info/sct"},
        {"code": "69536005", "display": "Head", "system": "http://snomed.info/sct"},
        {"code": "8205005", "display": "Wrist", "system": "http://snomed.info/sct"},
        {"code": "72696002", "display": "Knee", "system": "http://snomed.info/sct"},
        {"code": "818981001", "display": "Abdomen", "system": "http://snomed.info/sct"},
        {"code": "122494005", "display": "Cervical spine", "system": "http://snomed.info/sct"},
        {"code": "122495006", "display": "Lumbar spine", "system": "http://snomed.info/sct"},
        {"code": "76752008", "display": "Breast", "system": "http://snomed.info/sct"},
        {"code": "40983000", "display": "Upper arm", "system": "http://snomed.info/sct"},
        {"code": "30021000", "display": "Lower leg", "system": "http://snomed.info/sct"},
    ]

    # Study Reason Codes (SNOMED CT)
    REASON_CODES = [
        {"code": "27355003", "display": "Toothache", "system": "http://snomed.info/sct"},
        {"code": "57676002", "display": "Arthralgia", "system": "http://snomed.info/sct"},
        {"code": "25064002", "display": "Headache", "system": "http://snomed.info/sct"},
        {"code": "21522001", "display": "Abdominal pain", "system": "http://snomed.info/sct"},
        {"code": "29857009", "display": "Chest pain", "system": "http://snomed.info/sct"},
        {"code": "125605004", "display": "Fracture", "system": "http://snomed.info/sct"},
        {"code": "417746004", "display": "Traumatic injury", "system": "http://snomed.info/sct"},
        {"code": "363358000", "display": "Malignant tumor", "system": "http://snomed.info/sct"},
        {"code": "171009", "display": "Screening", "system": "http://snomed.info/sct"},
        {"code": "268478000", "display": "Pre-operative evaluation", "system": "http://snomed.info/sct"},
    ]

    STATUS_CODES = ["registered", "available", "cancelled", "entered-in-error", "unknown"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        study_id: str | None = None,
        patient_ref: str | None = None,
        encounter_ref: str | None = None,
        referrer_ref: str | None = None,
        performer_ref: str | None = None,
        location_ref: str | None = None,
        endpoint_ref: str | None = None,
        modality: str | None = None,
        status: str = "available",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate an ImagingStudy resource.

        Args:
            study_id: Study ID (generates UUID if None)
            patient_ref: Reference to Patient
            encounter_ref: Reference to Encounter
            referrer_ref: Reference to Practitioner who ordered study
            performer_ref: Reference to Practitioner who performed study
            location_ref: Reference to Location
            endpoint_ref: Reference to Endpoint for DICOM data
            modality: DICOM modality code (random if None)
            status: Study status

        Returns:
            ImagingStudy FHIR resource
        """
        if study_id is None:
            study_id = self._generate_id()

        # Select modality
        if modality is None:
            modality_coding = self.faker.random_element(self.MODALITIES)
        else:
            modality_coding = next(
                (m for m in self.MODALITIES if m["code"] == modality),
                self.MODALITIES[0],
            )

        body_site = self.faker.random_element(self.BODY_SITES)
        reason = self.faker.random_element(self.REASON_CODES)

        # Generate study datetime
        now = datetime.now(timezone.utc)
        started = self._generate_datetime(start_date=now - timedelta(days=90), end_date=now)

        # Generate DICOM UIDs
        study_uid = f"1.2.826.0.1.{self.faker.numerify('######')}.{self.faker.numerify('########')}"
        series_uid = f"{study_uid}.1"
        sop_uid = f"{series_uid}.1"

        study: dict[str, Any] = {
            "resourceType": "ImagingStudy",
            "id": study_id,
            "meta": self._generate_meta(),
            "identifier": [
                {
                    "system": "urn:dicom:uid",
                    "value": f"urn:oid:{study_uid}",
                },
            ],
            "status": status,
            "modality": [modality_coding],
            "description": f"{modality_coding['display']} of {body_site['display']}",
            "started": started,
            "numberOfSeries": self.faker.random_int(min=1, max=5),
            "numberOfInstances": self.faker.random_int(min=10, max=200),
            "reasonCode": [
                {
                    "coding": [reason],
                    "text": reason["display"],
                }
            ],
            "series": [
                {
                    "uid": series_uid,
                    "number": 1,
                    "modality": modality_coding,
                    "description": f"{body_site['display']} {modality_coding['display']}",
                    "numberOfInstances": self.faker.random_int(min=5, max=50),
                    "bodySite": {
                        "coding": [body_site],
                        "text": body_site["display"],
                    },
                    "instance": [
                        {
                            "uid": sop_uid,
                            "sopClass": {
                                "system": "urn:ietf:rfc:3986",
                                "code": "urn:oid:1.2.840.10008.5.1.4.1.1.2",
                            },
                            "number": 1,
                        }
                    ],
                }
            ],
            "note": [
                {
                    "text": f"Imaging study performed using {modality_coding['display']}",
                }
            ],
        }

        if patient_ref:
            study["subject"] = {"reference": patient_ref}

        if encounter_ref:
            study["encounter"] = {"reference": encounter_ref}

        if referrer_ref:
            study["referrer"] = {"reference": referrer_ref}

        if performer_ref:
            study["series"][0]["performer"] = [
                {
                    "function": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                "code": "PRF",
                                "display": "Performer",
                            }
                        ]
                    },
                    "actor": {"reference": performer_ref},
                }
            ]

        if location_ref:
            study["location"] = {"reference": location_ref}

        if endpoint_ref:
            study["endpoint"] = [{"reference": endpoint_ref}]

        return study
