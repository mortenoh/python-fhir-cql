"""OrganizationAffiliation resource generator."""

from datetime import date, timedelta
from typing import Any

from faker import Faker

from .base import FHIRResourceGenerator


class OrganizationAffiliationGenerator(FHIRResourceGenerator):
    """Generator for FHIR OrganizationAffiliation resources."""

    # Affiliation roles
    ROLES = [
        {"code": "provider", "display": "Provider", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "agency", "display": "Agency", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "research", "display": "Research", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "payer", "display": "Payer", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "diagnostics", "display": "Diagnostics", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "supplier", "display": "Supplier", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "HIE/HIO", "display": "HIE/HIO", "system": "http://hl7.org/fhir/organization-role"},
        {"code": "member", "display": "Member", "system": "http://hl7.org/fhir/organization-role"},
    ]

    # Specialties
    SPECIALTIES = [
        {"code": "394579002", "display": "Cardiology", "system": "http://snomed.info/sct"},
        {"code": "394585009", "display": "Obstetrics", "system": "http://snomed.info/sct"},
        {"code": "394582007", "display": "Dermatology", "system": "http://snomed.info/sct"},
        {"code": "394583002", "display": "Endocrinology", "system": "http://snomed.info/sct"},
        {"code": "394584008", "display": "Gastroenterology", "system": "http://snomed.info/sct"},
        {"code": "394802001", "display": "General medicine", "system": "http://snomed.info/sct"},
        {"code": "394586005", "display": "Gynecology", "system": "http://snomed.info/sct"},
        {"code": "394587001", "display": "Psychiatry", "system": "http://snomed.info/sct"},
        {"code": "394589003", "display": "Nephrology", "system": "http://snomed.info/sct"},
        {"code": "394591006", "display": "Neurology", "system": "http://snomed.info/sct"},
    ]

    def __init__(self, faker: Faker | None = None, seed: int | None = None):
        super().__init__(faker, seed)

    def generate(
        self,
        affiliation_id: str | None = None,
        organization_ref: str | None = None,
        participating_org_ref: str | None = None,
        network_refs: list[str] | None = None,
        location_refs: list[str] | None = None,
        service_refs: list[str] | None = None,
        endpoint_refs: list[str] | None = None,
        role: str | None = None,
        active: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate an OrganizationAffiliation resource.

        Args:
            affiliation_id: Affiliation ID (generates UUID if None)
            organization_ref: Reference to parent Organization
            participating_org_ref: Reference to participating Organization
            network_refs: List of references to network Organizations
            location_refs: List of references to Locations
            service_refs: List of references to HealthcareServices
            endpoint_refs: List of references to Endpoints
            role: Affiliation role code (random if None)
            active: Whether the affiliation is active

        Returns:
            OrganizationAffiliation FHIR resource
        """
        if affiliation_id is None:
            affiliation_id = self._generate_id()

        # Select role
        if role is None:
            role_coding = self.faker.random_element(self.ROLES)
        else:
            role_coding = next(
                (r for r in self.ROLES if r["code"] == role),
                self.ROLES[0],
            )

        specialty = self.faker.random_element(self.SPECIALTIES)

        # Generate period
        start_date = self._generate_date(start_date=date.today() - timedelta(days=730))

        affiliation: dict[str, Any] = {
            "resourceType": "OrganizationAffiliation",
            "id": affiliation_id,
            "meta": self._generate_meta(),
            "identifier": [
                self._generate_identifier(
                    system="http://example.org/org-affiliation-ids",
                    value=f"OA-{self.faker.numerify('########')}",
                ),
            ],
            "active": active,
            "period": {
                "start": start_date,
            },
            "code": [
                {
                    "coding": [role_coding],
                    "text": role_coding["display"],
                }
            ],
            "specialty": [
                {
                    "coding": [specialty],
                    "text": specialty["display"],
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": self.faker.phone_number(),
                    "use": "work",
                },
                {
                    "system": "email",
                    "value": self.faker.company_email(),
                    "use": "work",
                },
            ],
        }

        if organization_ref:
            affiliation["organization"] = {"reference": organization_ref}

        if participating_org_ref:
            affiliation["participatingOrganization"] = {"reference": participating_org_ref}

        if network_refs:
            affiliation["network"] = [{"reference": ref} for ref in network_refs]

        if location_refs:
            affiliation["location"] = [{"reference": ref} for ref in location_refs]

        if service_refs:
            affiliation["healthcareService"] = [{"reference": ref} for ref in service_refs]

        if endpoint_refs:
            affiliation["endpoint"] = [{"reference": ref} for ref in endpoint_refs]

        # Add period end if inactive
        if not active:
            affiliation["period"]["end"] = self._generate_date(start_date=date.today() - timedelta(days=30))

        return affiliation
