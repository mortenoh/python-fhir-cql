"""Endpoint resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class EndpointGenerator(FHIRResourceGenerator):
    """Generator for FHIR Endpoint resources."""

    # Connection types
    CONNECTION_TYPES = [
        {
            "code": "hl7-fhir-rest",
            "display": "HL7 FHIR REST",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "hl7-fhir-msg",
            "display": "HL7 FHIR Messaging",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "hl7v2-mllp",
            "display": "HL7 v2 MLLP",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "dicom-wado-rs",
            "display": "DICOM WADO-RS",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "dicom-qido-rs",
            "display": "DICOM QIDO-RS",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "dicom-stow-rs",
            "display": "DICOM STOW-RS",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "ihe-xcpd",
            "display": "IHE XCPD",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "ihe-xdr",
            "display": "IHE XDR",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "ihe-xds",
            "display": "IHE XDS",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
        {
            "code": "secure-email",
            "display": "Secure Email",
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
        },
    ]

    # Payload types
    PAYLOAD_TYPES = [
        {
            "code": "urn:hl7-org:sdwg:ccda-structuredBody:1.1",
            "display": "C-CDA Structured Body",
            "system": "http://hl7.org/fhir/endpoint-payload-type",
        },
        {
            "code": "urn:hl7-org:sdwg:ccda-nonXMLBody:1.1",
            "display": "C-CDA Non-XML Body",
            "system": "http://hl7.org/fhir/endpoint-payload-type",
        },
        {
            "code": "urn:ihe:pcc:xphr:2007",
            "display": "IHE XPHR",
            "system": "http://ihe.net/fhir/ihe.formatcode.fhir/CodeSystem/formatcode",
        },
        {"code": "any", "display": "Any", "system": "http://terminology.hl7.org/CodeSystem/endpoint-payload-type"},
    ]

    # Status codes
    STATUS_CODES = ["active", "suspended", "error", "off", "entered-in-error", "test"]

    # MIME types
    MIME_TYPES = [
        "application/fhir+json",
        "application/fhir+xml",
        "application/hl7-v2",
        "application/dicom",
        "text/xml",
        "application/pdf",
        "text/plain",
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        endpoint_id: str | None = None,
        managing_org_ref: str | None = None,
        connection_type: str | None = None,
        status: str = "active",
        name: str | None = None,
        address: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate an Endpoint resource.

        Args:
            endpoint_id: Endpoint ID (generates UUID if None)
            managing_org_ref: Reference to managing Organization
            connection_type: Connection type code (random if None)
            status: Endpoint status
            name: Endpoint name (auto-generated if None)
            address: Endpoint URL (auto-generated if None)

        Returns:
            Endpoint FHIR resource
        """
        if endpoint_id is None:
            endpoint_id = self._generate_id()

        # Select connection type
        if connection_type is None:
            conn_type = self.faker.random_element(self.CONNECTION_TYPES)
        else:
            conn_type = next(
                (c for c in self.CONNECTION_TYPES if c["code"] == connection_type),
                self.CONNECTION_TYPES[0],
            )

        payload_type = self.faker.random_element(self.PAYLOAD_TYPES)

        # Generate name
        if name is None:
            name = f"{self.faker.company()} {conn_type['display']} Endpoint"

        # Generate address
        if address is None:
            domain = self.faker.domain_name()
            if "fhir" in conn_type["code"].lower():
                address = f"https://{domain}/fhir/r4"
            elif "dicom" in conn_type["code"].lower():
                address = f"https://{domain}/dicom"
            elif "hl7v2" in conn_type["code"].lower():
                address = f"mllp://{domain}:2575"
            else:
                address = f"https://{domain}/api"

        # Select appropriate MIME types
        if "fhir" in conn_type["code"].lower():
            mime_types = ["application/fhir+json", "application/fhir+xml"]
        elif "dicom" in conn_type["code"].lower():
            mime_types = ["application/dicom"]
        elif "hl7v2" in conn_type["code"].lower():
            mime_types = ["application/hl7-v2"]
        else:
            mime_types = list(self.faker.random_elements(self.MIME_TYPES, length=2, unique=True))

        endpoint: dict[str, Any] = {
            "resourceType": "Endpoint",
            "id": endpoint_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/endpoint-ids",
                    value=f"EP-{self.faker.numerify('########')}",
                ),
            ],
            "status": status,
            "connectionType": conn_type,
            "name": name,
            "payloadType": [
                {
                    "coding": [payload_type],
                    "text": payload_type["display"],
                }
            ],
            "payloadMimeType": mime_types,
            "address": address,
        }

        if managing_org_ref:
            endpoint["managingOrganization"] = {"reference": managing_org_ref}

        # Add contact information
        endpoint["contact"] = [
            {
                "system": "email",
                "value": f"integration-support@{self.faker.domain_name()}",
                "use": "work",
            }
        ]

        # Add period for non-active endpoints
        if status in ["suspended", "off"]:
            endpoint["period"] = {
                "start": self._generate_date(start_date=date.today() - timedelta(days=365)),
                "end": self._generate_date(start_date=date.today() - timedelta(days=7)),
            }
        else:
            endpoint["period"] = {
                "start": self._generate_date(start_date=date.today() - timedelta(days=365)),
            }

        # Add headers for REST endpoints
        if "rest" in conn_type["code"].lower():
            endpoint["header"] = [
                "Authorization: Bearer <token>",
                "Content-Type: application/fhir+json",
            ]

        return endpoint
