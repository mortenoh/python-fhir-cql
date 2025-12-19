"""DeviceDefinition resource generator."""

from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class DeviceDefinitionGenerator(FHIRResourceGenerator):
    """Generator for FHIR DeviceDefinition resources."""

    # Device types (SNOMED CT)
    DEVICE_TYPES = [
        {"code": "43770009", "display": "Sphygmomanometer", "system": "http://snomed.info/sct"},
        {"code": "19257004", "display": "Defibrillator", "system": "http://snomed.info/sct"},
        {"code": "303607000", "display": "Cochlear implant", "system": "http://snomed.info/sct"},
        {"code": "37299003", "display": "Glucose monitor", "system": "http://snomed.info/sct"},
        {"code": "53350007", "display": "Pacemaker", "system": "http://snomed.info/sct"},
        {"code": "462894001", "display": "Insulin pump", "system": "http://snomed.info/sct"},
        {"code": "360063003", "display": "CPAP unit", "system": "http://snomed.info/sct"},
        {"code": "702127004", "display": "Pulse oximeter", "system": "http://snomed.info/sct"},
        {"code": "706767009", "display": "Ventilator", "system": "http://snomed.info/sct"},
        {"code": "714009009", "display": "Infusion pump", "system": "http://snomed.info/sct"},
    ]

    # Safety classifications
    SAFETY_CODES = [
        {
            "code": "C101672",
            "display": "Not made with natural rubber latex",
            "system": "urn:oid:2.16.840.1.113883.3.26.1.1",
        },
        {"code": "C106038", "display": "Contains dry natural rubber", "system": "urn:oid:2.16.840.1.113883.3.26.1.1"},
        {"code": "C106047", "display": "MRI Safe", "system": "urn:oid:2.16.840.1.113883.3.26.1.1"},
        {"code": "C113844", "display": "MRI Conditional", "system": "urn:oid:2.16.840.1.113883.3.26.1.1"},
        {"code": "C113845", "display": "MRI Unsafe", "system": "urn:oid:2.16.840.1.113883.3.26.1.1"},
    ]

    # Manufacturers
    MANUFACTURERS = [
        "Medtronic",
        "Abbott",
        "Boston Scientific",
        "Philips Healthcare",
        "GE Healthcare",
        "Siemens Healthineers",
        "Johnson & Johnson",
        "Stryker",
        "Baxter",
        "Fresenius Kabi",
    ]

    # Device name types
    NAME_TYPES = ["udi-label-name", "user-friendly-name", "patient-reported-name", "manufacturer-name", "model-name"]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        definition_id: str | None = None,
        manufacturer_ref: str | None = None,
        device_type: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate a DeviceDefinition resource.

        Args:
            definition_id: Definition ID (generates UUID if None)
            manufacturer_ref: Reference to Organization (manufacturer)
            device_type: SNOMED CT device type code (random if None)

        Returns:
            DeviceDefinition FHIR resource
        """
        if definition_id is None:
            definition_id = self._generate_id()

        # Select device type
        if device_type is None:
            type_coding = self.faker.random_element(self.DEVICE_TYPES)
        else:
            type_coding = next(
                (t for t in self.DEVICE_TYPES if t["code"] == device_type),
                self.DEVICE_TYPES[0],
            )

        manufacturer = self.faker.random_element(self.MANUFACTURERS)
        model_number = f"{self.faker.lexify('???').upper()}-{self.faker.numerify('####')}"
        safety = self.faker.random_element(self.SAFETY_CODES)

        definition: dict[str, Any] = {
            "resourceType": "DeviceDefinition",
            "id": definition_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/device-definition-ids",
                    value=f"DD-{self.faker.numerify('########')}",
                ),
            ],
            "udiDeviceIdentifier": [
                {
                    "deviceIdentifier": self.faker.numerify("##############"),
                    "issuer": "http://hl7.org/fhir/NamingSystem/gs1-di",
                    "jurisdiction": "http://hl7.org/fhir/NamingSystem/fda-udi",
                }
            ],
            "manufacturerString": manufacturer,
            "deviceName": [
                {
                    "name": f"{manufacturer} {type_coding['display']}",
                    "type": "user-friendly-name",
                },
                {
                    "name": model_number,
                    "type": "model-name",
                },
            ],
            "modelNumber": model_number,
            "type": {
                "coding": [type_coding],
                "text": type_coding["display"],
            },
            "version": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/device-version-type",
                                "code": "firmware",
                                "display": "Firmware",
                            }
                        ]
                    },
                    "value": (
                        f"v{self.faker.random_int(min=1, max=5)}"
                        f".{self.faker.random_int(min=0, max=9)}"
                        f".{self.faker.random_int(min=0, max=99)}"
                    ),
                }
            ],
            "safety": [
                {
                    "coding": [safety],
                    "text": safety["display"],
                }
            ],
            "property": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://example.org/device-property",
                                "code": "operating-temperature",
                                "display": "Operating Temperature",
                            }
                        ]
                    },
                    "valueQuantity": [
                        {
                            "value": self.faker.random_int(min=15, max=25),
                            "unit": "Celsius",
                            "system": "http://unitsofmeasure.org",
                            "code": "Cel",
                        }
                    ],
                },
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://example.org/device-property",
                                "code": "weight",
                                "display": "Weight",
                            }
                        ]
                    },
                    "valueQuantity": [
                        {
                            "value": round(self.faker.random.uniform(0.1, 10.0), 2),
                            "unit": "kilogram",
                            "system": "http://unitsofmeasure.org",
                            "code": "kg",
                        }
                    ],
                },
            ],
            "capability": [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://example.org/device-capability",
                                "code": "data-transmission",
                                "display": "Data Transmission",
                            }
                        ]
                    },
                    "description": [
                        {
                            "text": "Bluetooth 5.0, WiFi 802.11 b/g/n",
                        }
                    ],
                }
            ],
            "note": [
                {
                    "text": f"Device definition for {manufacturer} {type_coding['display']}",
                }
            ],
        }

        if manufacturer_ref:
            definition["manufacturerReference"] = {"reference": manufacturer_ref}

        return definition
