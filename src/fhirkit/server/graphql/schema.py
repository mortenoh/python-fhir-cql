"""GraphQL schema generation for FHIR resources.

This module dynamically generates a GraphQL schema that supports all FHIR
resource types defined in SUPPORTED_TYPES. It creates:

- Single resource queries: Patient(_id: "123")
- List queries with search: PatientList(name: "Smith", _count: 10)
- Connection queries: PatientConnection(first: 10, after: "cursor")
- Mutations: PatientCreate, PatientUpdate, PatientDelete

The schema is generated dynamically at runtime to support all resource types
without manually defining each one.
"""

import logging
from typing import Annotated, Any, Optional

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON

from ..api.routes import SUPPORTED_TYPES
from ..storage.fhir_store import FHIRStore
from .resolvers import ConnectionResolver, ListResolver, MutationResolver, ResourceResolver
from .types import Resource, ResourceConnection

logger = logging.getLogger(__name__)

# Type aliases for FHIR-specific argument names (underscore prefix)
# Strawberry would normally convert _id to Id, but FHIR uses _id
FhirId = Annotated[str, strawberry.argument(name="id")]
FhirCount = Annotated[int, strawberry.argument(name="_count")]
FhirOffset = Annotated[int, strawberry.argument(name="_offset")]
FhirSort = Annotated[Optional[str], strawberry.argument(name="_sort")]


def create_schema(store: FHIRStore) -> strawberry.Schema:
    """Create the GraphQL schema with all FHIR resource queries and mutations.

    This function dynamically generates:
    - Query fields for each resource type (read, list, connection)
    - Mutation fields for each resource type (create, update, delete)

    Args:
        store: FHIRStore instance for data access

    Returns:
        Configured Strawberry GraphQL schema
    """
    # Initialize resolvers
    resource_resolver = ResourceResolver(store)
    list_resolver = ListResolver(store)
    connection_resolver = ConnectionResolver(store)
    mutation_resolver = MutationResolver(store)

    # =========================================================================
    # Query Type
    # =========================================================================

    @strawberry.type(description="GraphQL queries for FHIR resources")
    class Query:
        """Root query type with all FHIR resource queries.

        Provides three query patterns for each resource type:
        - {Type}(_id): Fetch single resource by ID
        - {Type}List(...): Search with parameters and offset pagination
        - {Type}Connection(...): Search with cursor-based pagination
        """

        # Generic resource query (for any type)
        @strawberry.field(description="Fetch any FHIR resource by type and ID")
        def resource(
            self,
            resourceType: str,
            _id: FhirId,
        ) -> Optional[Resource]:
            """Generic resource query for any type."""
            if resourceType not in SUPPORTED_TYPES:
                return None
            return resource_resolver.resolve(resourceType, _id)

        @strawberry.field(description="Search any FHIR resource type")
        def resourceList(
            self,
            resourceType: str,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
        ) -> list[Resource]:
            """Generic resource list query for any type."""
            if resourceType not in SUPPORTED_TYPES:
                return []
            return list_resolver.resolve(resourceType, _count=_count, _offset=_offset, _sort=_sort)

        @strawberry.field(description="Search any FHIR resource type with cursor pagination")
        def resourceConnection(
            self,
            resourceType: str,
            first: Optional[int] = None,
            after: Optional[str] = None,
            last: Optional[int] = None,
            before: Optional[str] = None,
            _sort: FhirSort = None,
        ) -> ResourceConnection:
            """Generic resource connection query for any type."""
            return connection_resolver.resolve(
                resourceType, first=first, after=after, last=last, before=before, _sort=_sort
            )

        # =====================================================================
        # Administrative Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Patient by ID")
        def patient(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Patient", _id)

        @strawberry.field(description="Search Patient resources")
        def patients(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            # Patient-specific search params
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            family: Optional[str] = None,
            given: Optional[str] = None,
            gender: Optional[str] = None,
            birthdate: Optional[str] = None,
            address: Optional[str] = None,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            general_practitioner: Optional[str] = None,
            organization: Optional[str] = None,
            active: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Patient",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                identifier=identifier,
                name=name,
                family=family,
                given=given,
                gender=gender,
                birthdate=birthdate,
                address=address,
                phone=phone,
                email=email,
                general_practitioner=general_practitioner,
                organization=organization,
                active=active,
            )

        @strawberry.field(description="Search Patient resources with cursor pagination")
        def patientConnection(
            self,
            first: Optional[int] = None,
            after: Optional[str] = None,
            last: Optional[int] = None,
            before: Optional[str] = None,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            gender: Optional[str] = None,
            birthdate: Optional[str] = None,
        ) -> ResourceConnection:
            return connection_resolver.resolve(
                "Patient",
                first=first,
                after=after,
                last=last,
                before=before,
                _sort=_sort,
                name=name,
                gender=gender,
                birthdate=birthdate,
            )

        @strawberry.field(description="Fetch a Practitioner by ID")
        def practitioner(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Practitioner", _id)

        @strawberry.field(description="Search Practitioner resources")
        def practitioners(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            family: Optional[str] = None,
            given: Optional[str] = None,
            active: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Practitioner",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                identifier=identifier,
                name=name,
                family=family,
                given=given,
                active=active,
            )

        @strawberry.field(description="Fetch an Organization by ID")
        def organization(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Organization", _id)

        @strawberry.field(description="Search Organization resources")
        def organizations(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            type: Optional[str] = None,
            active: Optional[str] = None,
            partof: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Organization",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                identifier=identifier,
                name=name,
                type=type,
                active=active,
                partof=partof,
            )

        @strawberry.field(description="Fetch a Location by ID")
        def location(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Location", _id)

        @strawberry.field(description="Search Location resources")
        def locations(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            identifier: Optional[str] = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            type: Optional[str] = None,
            organization: Optional[str] = None,
            partof: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Location",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                identifier=identifier,
                name=name,
                status=status,
                type=type,
                organization=organization,
                partof=partof,
            )

        @strawberry.field(description="Fetch a PractitionerRole by ID")
        def practitionerRole(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("PractitionerRole", _id)

        @strawberry.field(description="Search PractitionerRole resources")
        def practitionerRoles(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            practitioner: Optional[str] = None,
            organization: Optional[str] = None,
            specialty: Optional[str] = None,
            active: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "PractitionerRole",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                practitioner=practitioner,
                organization=organization,
                specialty=specialty,
                active=active,
            )

        @strawberry.field(description="Fetch a RelatedPerson by ID")
        def relatedPerson(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("RelatedPerson", _id)

        @strawberry.field(description="Search RelatedPerson resources")
        def relatedPersons(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            name: Optional[str] = None,
            relationship: Optional[str] = None,
            active: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "RelatedPerson",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                name=name,
                relationship=relationship,
                active=active,
            )

        # =====================================================================
        # Clinical Resources
        # =====================================================================

        @strawberry.field(description="Fetch an Encounter by ID")
        def encounter(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Encounter", _id)

        @strawberry.field(description="Search Encounter resources")
        def encounters(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            class_: Optional[str] = None,
            type: Optional[str] = None,
            date: Optional[str] = None,
            participant: Optional[str] = None,
            service_provider: Optional[str] = None,
        ) -> list[Resource]:
            params: dict[str, Any] = {
                "patient": patient,
                "subject": subject,
                "status": status,
                "type": type,
                "date": date,
                "participant": participant,
                "service_provider": service_provider,
            }
            if class_:
                params["class"] = class_
            return list_resolver.resolve(
                "Encounter",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                **params,
            )

        @strawberry.field(description="Fetch a Condition by ID")
        def condition(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Condition", _id)

        @strawberry.field(description="Search Condition resources")
        def conditions(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            code: Optional[str] = None,
            clinical_status: Optional[str] = None,
            verification_status: Optional[str] = None,
            category: Optional[str] = None,
            onset_date: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Condition",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                code=code,
                clinical_status=clinical_status,
                verification_status=verification_status,
                category=category,
                onset_date=onset_date,
                encounter=encounter,
            )

        @strawberry.field(description="Fetch an Observation by ID")
        def observation(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Observation", _id)

        @strawberry.field(description="Search Observation resources")
        def observations(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            code: Optional[str] = None,
            category: Optional[str] = None,
            status: Optional[str] = None,
            date: Optional[str] = None,
            encounter: Optional[str] = None,
            performer: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Observation",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                code=code,
                category=category,
                status=status,
                date=date,
                encounter=encounter,
                performer=performer,
            )

        @strawberry.field(description="Fetch a Procedure by ID")
        def procedure(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Procedure", _id)

        @strawberry.field(description="Search Procedure resources")
        def procedures(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            code: Optional[str] = None,
            status: Optional[str] = None,
            date: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Procedure",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                code=code,
                status=status,
                date=date,
                encounter=encounter,
            )

        @strawberry.field(description="Fetch a DiagnosticReport by ID")
        def diagnosticReport(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("DiagnosticReport", _id)

        @strawberry.field(description="Search DiagnosticReport resources")
        def diagnosticReports(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            code: Optional[str] = None,
            category: Optional[str] = None,
            status: Optional[str] = None,
            date: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "DiagnosticReport",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                code=code,
                category=category,
                status=status,
                date=date,
                encounter=encounter,
            )

        @strawberry.field(description="Fetch an AllergyIntolerance by ID")
        def allergyIntolerance(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("AllergyIntolerance", _id)

        @strawberry.field(description="Search AllergyIntolerance resources")
        def allergyIntolerances(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            code: Optional[str] = None,
            clinical_status: Optional[str] = None,
            verification_status: Optional[str] = None,
            type: Optional[str] = None,
            category: Optional[str] = None,
            criticality: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "AllergyIntolerance",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                code=code,
                clinical_status=clinical_status,
                verification_status=verification_status,
                type=type,
                category=category,
                criticality=criticality,
            )

        @strawberry.field(description="Fetch an Immunization by ID")
        def immunization(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Immunization", _id)

        @strawberry.field(description="Search Immunization resources")
        def immunizations(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            vaccine_code: Optional[str] = None,
            status: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Immunization",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                vaccine_code=vaccine_code,
                status=status,
                date=date,
            )

        # =====================================================================
        # Medication Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Medication by ID")
        def medication(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Medication", _id)

        @strawberry.field(description="Search Medication resources")
        def medications(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            code: Optional[str] = None,
            status: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Medication",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                code=code,
                status=status,
            )

        @strawberry.field(description="Fetch a MedicationRequest by ID")
        def medicationRequest(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("MedicationRequest", _id)

        @strawberry.field(description="Search MedicationRequest resources")
        def medicationRequests(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            intent: Optional[str] = None,
            medication: Optional[str] = None,
            authoredon: Optional[str] = None,
            encounter: Optional[str] = None,
            requester: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "MedicationRequest",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                intent=intent,
                medication=medication,
                authoredon=authoredon,
                encounter=encounter,
                requester=requester,
            )

        # =====================================================================
        # Care Management Resources
        # =====================================================================

        @strawberry.field(description="Fetch a CarePlan by ID")
        def carePlan(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("CarePlan", _id)

        @strawberry.field(description="Search CarePlan resources")
        def carePlans(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            intent: Optional[str] = None,
            category: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "CarePlan",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                intent=intent,
                category=category,
            )

        @strawberry.field(description="Fetch a CareTeam by ID")
        def careTeam(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("CareTeam", _id)

        @strawberry.field(description="Search CareTeam resources")
        def careTeams(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            category: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "CareTeam",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                category=category,
            )

        @strawberry.field(description="Fetch a Goal by ID")
        def goal(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Goal", _id)

        @strawberry.field(description="Search Goal resources")
        def goals(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            lifecycle_status: Optional[str] = None,
            category: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Goal",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                lifecycle_status=lifecycle_status,
                category=category,
            )

        @strawberry.field(description="Fetch a Task by ID")
        def task(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Task", _id)

        @strawberry.field(description="Search Task resources")
        def tasks(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            intent: Optional[str] = None,
            owner: Optional[str] = None,
            requester: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Task",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                intent=intent,
                owner=owner,
                requester=requester,
            )

        # =====================================================================
        # Scheduling Resources
        # =====================================================================

        @strawberry.field(description="Fetch an Appointment by ID")
        def appointment(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Appointment", _id)

        @strawberry.field(description="Search Appointment resources")
        def appointments(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            actor: Optional[str] = None,
            status: Optional[str] = None,
            date: Optional[str] = None,
            service_type: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Appointment",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                actor=actor,
                status=status,
                date=date,
                service_type=service_type,
            )

        @strawberry.field(description="Fetch a Schedule by ID")
        def schedule(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Schedule", _id)

        @strawberry.field(description="Search Schedule resources")
        def schedules(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            actor: Optional[str] = None,
            active: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Schedule",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                actor=actor,
                active=active,
            )

        @strawberry.field(description="Fetch a Slot by ID")
        def slot(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Slot", _id)

        @strawberry.field(description="Search Slot resources")
        def slots(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            schedule: Optional[str] = None,
            status: Optional[str] = None,
            start: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Slot",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                schedule=schedule,
                status=status,
                start=start,
            )

        # =====================================================================
        # Financial Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Coverage by ID")
        def coverage(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Coverage", _id)

        @strawberry.field(description="Search Coverage resources")
        def coverages(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            beneficiary: Optional[str] = None,
            payor: Optional[str] = None,
            status: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Coverage",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                beneficiary=beneficiary,
                payor=payor,
                status=status,
            )

        @strawberry.field(description="Fetch a Claim by ID")
        def claim(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Claim", _id)

        @strawberry.field(description="Search Claim resources")
        def claims(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            created: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Claim",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                created=created,
            )

        @strawberry.field(description="Fetch an ExplanationOfBenefit by ID")
        def explanationOfBenefit(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ExplanationOfBenefit", _id)

        @strawberry.field(description="Search ExplanationOfBenefit resources")
        def explanationOfBenefits(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            created: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ExplanationOfBenefit",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                created=created,
            )

        # =====================================================================
        # Device Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Device by ID")
        def device(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Device", _id)

        @strawberry.field(description="Search Device resources")
        def devices(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            type: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Device",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                type=type,
            )

        # =====================================================================
        # Document Resources
        # =====================================================================

        @strawberry.field(description="Fetch a ServiceRequest by ID")
        def serviceRequest(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ServiceRequest", _id)

        @strawberry.field(description="Search ServiceRequest resources")
        def serviceRequests(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            code: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ServiceRequest",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                code=code,
                encounter=encounter,
            )

        @strawberry.field(description="Fetch a DocumentReference by ID")
        def documentReference(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("DocumentReference", _id)

        @strawberry.field(description="Search DocumentReference resources")
        def documentReferences(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            type: Optional[str] = None,
            category: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "DocumentReference",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                type=type,
                category=category,
                date=date,
            )

        @strawberry.field(description="Fetch a Binary by ID")
        def binary(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Binary", _id)

        @strawberry.field(description="Search Binary resources")
        def binaries(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Binary",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
            )

        # =====================================================================
        # Quality Measure Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Measure by ID")
        def measure(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Measure", _id)

        @strawberry.field(description="Search Measure resources")
        def measures(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Measure",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
            )

        @strawberry.field(description="Fetch a MeasureReport by ID")
        def measureReport(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("MeasureReport", _id)

        @strawberry.field(description="Search MeasureReport resources")
        def measureReports(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            measure: Optional[str] = None,
            period: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "MeasureReport",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                measure=measure,
                period=period,
            )

        @strawberry.field(description="Fetch a Library by ID")
        def library(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Library", _id)

        @strawberry.field(description="Search Library resources")
        def libraries(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            type: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Library",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
                type=type,
            )

        # =====================================================================
        # Terminology Resources
        # =====================================================================

        @strawberry.field(description="Fetch a ValueSet by ID")
        def valueSet(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ValueSet", _id)

        @strawberry.field(description="Search ValueSet resources")
        def valueSets(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            url: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ValueSet",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
                url=url,
            )

        @strawberry.field(description="Fetch a CodeSystem by ID")
        def codeSystem(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("CodeSystem", _id)

        @strawberry.field(description="Search CodeSystem resources")
        def codeSystems(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            url: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "CodeSystem",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
                url=url,
            )

        @strawberry.field(description="Fetch a ConceptMap by ID")
        def conceptMap(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ConceptMap", _id)

        @strawberry.field(description="Search ConceptMap resources")
        def conceptMaps(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            url: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ConceptMap",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
                url=url,
            )

        # =====================================================================
        # Clinical Document Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Composition by ID")
        def composition(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Composition", _id)

        @strawberry.field(description="Search Composition resources")
        def compositions(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            type: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Composition",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                type=type,
                date=date,
            )

        # =====================================================================
        # Form Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Questionnaire by ID")
        def questionnaire(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Questionnaire", _id)

        @strawberry.field(description="Search Questionnaire resources")
        def questionnaires(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            url: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Questionnaire",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                title=title,
                url=url,
            )

        @strawberry.field(description="Fetch a QuestionnaireResponse by ID")
        def questionnaireResponse(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("QuestionnaireResponse", _id)

        @strawberry.field(description="Search QuestionnaireResponse resources")
        def questionnaireResponses(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            questionnaire: Optional[str] = None,
            authored: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "QuestionnaireResponse",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                questionnaire=questionnaire,
                authored=authored,
            )

        # =====================================================================
        # Group Resources
        # =====================================================================

        @strawberry.field(description="Fetch a Group by ID")
        def group(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Group", _id)

        @strawberry.field(description="Search Group resources")
        def groups(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            type: Optional[str] = None,
            actual: Optional[str] = None,
            code: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Group",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                type=type,
                actual=actual,
                code=code,
            )

        # =====================================================================
        # Imaging Resources
        # =====================================================================

        @strawberry.field(description="Fetch an ImagingStudy by ID")
        def imagingStudy(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ImagingStudy", _id)

        @strawberry.field(description="Search ImagingStudy resources")
        def imagingStudies(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            modality: Optional[str] = None,
            started: Optional[str] = None,
            referrer: Optional[str] = None,
            encounter: Optional[str] = None,
            endpoint: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ImagingStudy",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                modality=modality,
                started=started,
                referrer=referrer,
                encounter=encounter,
                endpoint=endpoint,
            )

        @strawberry.field(description="Fetch a BodyStructure by ID")
        def bodyStructure(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("BodyStructure", _id)

        @strawberry.field(description="Search BodyStructure resources")
        def bodyStructures(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            morphology: Optional[str] = None,
            location: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "BodyStructure",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                morphology=morphology,
                location=location,
            )

        # =====================================================================
        # Care Management Resources (Phase 2)
        # =====================================================================

        @strawberry.field(description="Fetch an EpisodeOfCare by ID")
        def episodeOfCare(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("EpisodeOfCare", _id)

        @strawberry.field(description="Search EpisodeOfCare resources")
        def episodesOfCare(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            type: Optional[str] = None,
            organization: Optional[str] = None,
            care_manager: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "EpisodeOfCare",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                type=type,
                organization=organization,
                care_manager=care_manager,
                date=date,
            )

        @strawberry.field(description="Fetch a List by ID")
        def fhirList(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("List", _id)

        @strawberry.field(description="Search List resources")
        def fhirLists(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            code: Optional[str] = None,
            date: Optional[str] = None,
            source: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "List",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                code=code,
                date=date,
                source=source,
                encounter=encounter,
            )

        @strawberry.field(description="Fetch a CommunicationRequest by ID")
        def communicationRequest(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("CommunicationRequest", _id)

        @strawberry.field(description="Search CommunicationRequest resources")
        def communicationRequests(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            category: Optional[str] = None,
            priority: Optional[str] = None,
            authored: Optional[str] = None,
            requester: Optional[str] = None,
            recipient: Optional[str] = None,
            sender: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "CommunicationRequest",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                category=category,
                priority=priority,
                authored=authored,
                requester=requester,
                recipient=recipient,
                sender=sender,
            )

        @strawberry.field(description="Fetch a RequestGroup by ID")
        def requestGroup(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("RequestGroup", _id)

        @strawberry.field(description="Search RequestGroup resources")
        def requestGroups(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            subject: Optional[str] = None,
            status: Optional[str] = None,
            intent: Optional[str] = None,
            priority: Optional[str] = None,
            code: Optional[str] = None,
            authored: Optional[str] = None,
            author: Optional[str] = None,
            encounter: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "RequestGroup",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                subject=subject,
                status=status,
                intent=intent,
                priority=priority,
                code=code,
                authored=authored,
                author=author,
                encounter=encounter,
            )

        # =====================================================================
        # Medication Knowledge Resources
        # =====================================================================

        @strawberry.field(description="Fetch a MedicationKnowledge by ID")
        def medicationKnowledge(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("MedicationKnowledge", _id)

        @strawberry.field(description="Search MedicationKnowledge resources")
        def medicationKnowledges(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            code: Optional[str] = None,
            status: Optional[str] = None,
            manufacturer: Optional[str] = None,
            doseform: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "MedicationKnowledge",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                code=code,
                status=status,
                manufacturer=manufacturer,
                doseform=doseform,
            )

        # =====================================================================
        # Device Resources (Phase 2)
        # =====================================================================

        @strawberry.field(description="Fetch a DeviceMetric by ID")
        def deviceMetric(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("DeviceMetric", _id)

        @strawberry.field(description="Search DeviceMetric resources")
        def deviceMetrics(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            type: Optional[str] = None,
            source: Optional[str] = None,
            parent: Optional[str] = None,
            category: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "DeviceMetric",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                type=type,
                source=source,
                parent=parent,
                category=category,
            )

        @strawberry.field(description="Fetch a DeviceDefinition by ID")
        def deviceDefinition(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("DeviceDefinition", _id)

        @strawberry.field(description="Search DeviceDefinition resources")
        def deviceDefinitions(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            type: Optional[str] = None,
            manufacturer: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "DeviceDefinition",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                type=type,
                manufacturer=manufacturer,
            )

        # =====================================================================
        # Research Resources
        # =====================================================================

        @strawberry.field(description="Fetch a ResearchStudy by ID")
        def researchStudy(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ResearchStudy", _id)

        @strawberry.field(description="Search ResearchStudy resources")
        def researchStudies(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            title: Optional[str] = None,
            status: Optional[str] = None,
            phase: Optional[str] = None,
            focus: Optional[str] = None,
            sponsor: Optional[str] = None,
            principalinvestigator: Optional[str] = None,
            site: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ResearchStudy",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                title=title,
                status=status,
                phase=phase,
                focus=focus,
                sponsor=sponsor,
                principalinvestigator=principalinvestigator,
                site=site,
                date=date,
            )

        @strawberry.field(description="Fetch a ResearchSubject by ID")
        def researchSubject(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("ResearchSubject", _id)

        @strawberry.field(description="Search ResearchSubject resources")
        def researchSubjects(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            individual: Optional[str] = None,
            status: Optional[str] = None,
            study: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "ResearchSubject",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                individual=individual,
                status=status,
                study=study,
                date=date,
            )

        # =====================================================================
        # Infrastructure Resources
        # =====================================================================

        @strawberry.field(description="Fetch an Endpoint by ID")
        def fhirEndpoint(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("Endpoint", _id)

        @strawberry.field(description="Search Endpoint resources")
        def fhirEndpoints(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            name: Optional[str] = None,
            status: Optional[str] = None,
            connection_type: Optional[str] = None,
            organization: Optional[str] = None,
            payload_type: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "Endpoint",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                name=name,
                status=status,
                connection_type=connection_type,
                organization=organization,
                payload_type=payload_type,
            )

        @strawberry.field(description="Fetch an OrganizationAffiliation by ID")
        def organizationAffiliation(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("OrganizationAffiliation", _id)

        @strawberry.field(description="Search OrganizationAffiliation resources")
        def organizationAffiliations(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            active: Optional[str] = None,
            primary_organization: Optional[str] = None,
            participating_organization: Optional[str] = None,
            role: Optional[str] = None,
            specialty: Optional[str] = None,
            location: Optional[str] = None,
            service: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "OrganizationAffiliation",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                active=active,
                primary_organization=primary_organization,
                participating_organization=participating_organization,
                role=role,
                specialty=specialty,
                location=location,
                service=service,
            )

        @strawberry.field(description="Fetch a SupplyRequest by ID")
        def supplyRequest(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("SupplyRequest", _id)

        @strawberry.field(description="Search SupplyRequest resources")
        def supplyRequests(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            status: Optional[str] = None,
            category: Optional[str] = None,
            supplier: Optional[str] = None,
            requester: Optional[str] = None,
            date: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "SupplyRequest",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                status=status,
                category=category,
                supplier=supplier,
                requester=requester,
                date=date,
            )

        @strawberry.field(description="Fetch a SupplyDelivery by ID")
        def supplyDelivery(self, _id: FhirId) -> Optional[Resource]:
            return resource_resolver.resolve("SupplyDelivery", _id)

        @strawberry.field(description="Search SupplyDelivery resources")
        def supplyDeliveries(
            self,
            _count: FhirCount = 100,
            _offset: FhirOffset = 0,
            _sort: FhirSort = None,
            patient: Optional[str] = None,
            status: Optional[str] = None,
            supplier: Optional[str] = None,
            receiver: Optional[str] = None,
        ) -> list[Resource]:
            return list_resolver.resolve(
                "SupplyDelivery",
                _count=_count,
                _offset=_offset,
                _sort=_sort,
                patient=patient,
                status=status,
                supplier=supplier,
                receiver=receiver,
            )

    # =========================================================================
    # Mutation Type
    # =========================================================================

    @strawberry.type(description="GraphQL mutations for FHIR resources")
    class Mutation:
        """Root mutation type with all FHIR resource mutations.

        Provides Create, Update, and Delete mutations for each resource type.
        """

        # Generic mutations (for any type)
        @strawberry.mutation(description="Create a FHIR resource of any type")
        def resourceCreate(
            self,
            resourceType: str,
            data: JSON,  # type: ignore[valid-type]
        ) -> Resource:
            """Generic resource create mutation."""
            if resourceType not in SUPPORTED_TYPES:
                raise ValueError(f"Unsupported resource type: {resourceType}")
            return mutation_resolver.create(resourceType, dict(data))

        @strawberry.mutation(description="Update a FHIR resource of any type")
        def resourceUpdate(
            self,
            resourceType: str,
            _id: str,
            data: JSON,  # type: ignore[valid-type]
        ) -> Optional[Resource]:
            """Generic resource update mutation."""
            if resourceType not in SUPPORTED_TYPES:
                raise ValueError(f"Unsupported resource type: {resourceType}")
            return mutation_resolver.update(resourceType, _id, dict(data))

        @strawberry.mutation(description="Delete a FHIR resource of any type")
        def resourceDelete(
            self,
            resourceType: str,
            _id: str,
        ) -> Optional[Resource]:
            """Generic resource delete mutation."""
            if resourceType not in SUPPORTED_TYPES:
                raise ValueError(f"Unsupported resource type: {resourceType}")
            return mutation_resolver.delete(resourceType, _id)

        # =====================================================================
        # Resource-specific mutations
        # =====================================================================

        @strawberry.mutation(description="Create a Patient resource")
        def createPatient(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Patient", dict(data))

        @strawberry.mutation(description="Update a Patient resource")
        def updatePatient(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Patient", _id, dict(data))

        @strawberry.mutation(description="Delete a Patient resource")
        def deletePatient(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Patient", _id)

        @strawberry.mutation(description="Create a Practitioner resource")
        def createPractitioner(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Practitioner", dict(data))

        @strawberry.mutation(description="Update a Practitioner resource")
        def updatePractitioner(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Practitioner", _id, dict(data))

        @strawberry.mutation(description="Delete a Practitioner resource")
        def deletePractitioner(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Practitioner", _id)

        @strawberry.mutation(description="Create an Organization resource")
        def createOrganization(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Organization", dict(data))

        @strawberry.mutation(description="Update an Organization resource")
        def updateOrganization(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Organization", _id, dict(data))

        @strawberry.mutation(description="Delete an Organization resource")
        def deleteOrganization(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Organization", _id)

        @strawberry.mutation(description="Create an Observation resource")
        def createObservation(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Observation", dict(data))

        @strawberry.mutation(description="Update an Observation resource")
        def updateObservation(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Observation", _id, dict(data))

        @strawberry.mutation(description="Delete an Observation resource")
        def deleteObservation(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Observation", _id)

        @strawberry.mutation(description="Create a Condition resource")
        def createCondition(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Condition", dict(data))

        @strawberry.mutation(description="Update a Condition resource")
        def updateCondition(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Condition", _id, dict(data))

        @strawberry.mutation(description="Delete a Condition resource")
        def deleteCondition(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Condition", _id)

        @strawberry.mutation(description="Create an Encounter resource")
        def createEncounter(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Encounter", dict(data))

        @strawberry.mutation(description="Update an Encounter resource")
        def updateEncounter(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Encounter", _id, dict(data))

        @strawberry.mutation(description="Delete an Encounter resource")
        def deleteEncounter(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Encounter", _id)

        @strawberry.mutation(description="Create a MedicationRequest resource")
        def createMedicationRequest(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("MedicationRequest", dict(data))

        @strawberry.mutation(description="Update a MedicationRequest resource")
        def updateMedicationRequest(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("MedicationRequest", _id, dict(data))

        @strawberry.mutation(description="Delete a MedicationRequest resource")
        def deleteMedicationRequest(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("MedicationRequest", _id)

        # =====================================================================
        # Imaging Resource Mutations
        # =====================================================================

        @strawberry.mutation(description="Create an ImagingStudy resource")
        def createImagingStudy(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("ImagingStudy", dict(data))

        @strawberry.mutation(description="Update an ImagingStudy resource")
        def updateImagingStudy(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("ImagingStudy", _id, dict(data))

        @strawberry.mutation(description="Delete an ImagingStudy resource")
        def deleteImagingStudy(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("ImagingStudy", _id)

        @strawberry.mutation(description="Create a BodyStructure resource")
        def createBodyStructure(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("BodyStructure", dict(data))

        @strawberry.mutation(description="Update a BodyStructure resource")
        def updateBodyStructure(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("BodyStructure", _id, dict(data))

        @strawberry.mutation(description="Delete a BodyStructure resource")
        def deleteBodyStructure(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("BodyStructure", _id)

        # =====================================================================
        # Care Management Mutations
        # =====================================================================

        @strawberry.mutation(description="Create an EpisodeOfCare resource")
        def createEpisodeOfCare(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("EpisodeOfCare", dict(data))

        @strawberry.mutation(description="Update an EpisodeOfCare resource")
        def updateEpisodeOfCare(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("EpisodeOfCare", _id, dict(data))

        @strawberry.mutation(description="Delete an EpisodeOfCare resource")
        def deleteEpisodeOfCare(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("EpisodeOfCare", _id)

        @strawberry.mutation(description="Create a List resource")
        def createList(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("List", dict(data))

        @strawberry.mutation(description="Update a List resource")
        def updateList(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("List", _id, dict(data))

        @strawberry.mutation(description="Delete a List resource")
        def deleteList(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("List", _id)

        @strawberry.mutation(description="Create a CommunicationRequest resource")
        def createCommunicationRequest(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("CommunicationRequest", dict(data))

        @strawberry.mutation(description="Update a CommunicationRequest resource")
        def updateCommunicationRequest(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("CommunicationRequest", _id, dict(data))

        @strawberry.mutation(description="Delete a CommunicationRequest resource")
        def deleteCommunicationRequest(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("CommunicationRequest", _id)

        @strawberry.mutation(description="Create a RequestGroup resource")
        def createRequestGroup(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("RequestGroup", dict(data))

        @strawberry.mutation(description="Update a RequestGroup resource")
        def updateRequestGroup(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("RequestGroup", _id, dict(data))

        @strawberry.mutation(description="Delete a RequestGroup resource")
        def deleteRequestGroup(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("RequestGroup", _id)

        # =====================================================================
        # Medication Knowledge Mutations
        # =====================================================================

        @strawberry.mutation(description="Create a MedicationKnowledge resource")
        def createMedicationKnowledge(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("MedicationKnowledge", dict(data))

        @strawberry.mutation(description="Update a MedicationKnowledge resource")
        def updateMedicationKnowledge(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("MedicationKnowledge", _id, dict(data))

        @strawberry.mutation(description="Delete a MedicationKnowledge resource")
        def deleteMedicationKnowledge(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("MedicationKnowledge", _id)

        # =====================================================================
        # Device Mutations
        # =====================================================================

        @strawberry.mutation(description="Create a DeviceMetric resource")
        def createDeviceMetric(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("DeviceMetric", dict(data))

        @strawberry.mutation(description="Update a DeviceMetric resource")
        def updateDeviceMetric(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("DeviceMetric", _id, dict(data))

        @strawberry.mutation(description="Delete a DeviceMetric resource")
        def deleteDeviceMetric(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("DeviceMetric", _id)

        @strawberry.mutation(description="Create a DeviceDefinition resource")
        def createDeviceDefinition(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("DeviceDefinition", dict(data))

        @strawberry.mutation(description="Update a DeviceDefinition resource")
        def updateDeviceDefinition(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("DeviceDefinition", _id, dict(data))

        @strawberry.mutation(description="Delete a DeviceDefinition resource")
        def deleteDeviceDefinition(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("DeviceDefinition", _id)

        # =====================================================================
        # Research Mutations
        # =====================================================================

        @strawberry.mutation(description="Create a ResearchStudy resource")
        def createResearchStudy(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("ResearchStudy", dict(data))

        @strawberry.mutation(description="Update a ResearchStudy resource")
        def updateResearchStudy(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("ResearchStudy", _id, dict(data))

        @strawberry.mutation(description="Delete a ResearchStudy resource")
        def deleteResearchStudy(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("ResearchStudy", _id)

        @strawberry.mutation(description="Create a ResearchSubject resource")
        def createResearchSubject(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("ResearchSubject", dict(data))

        @strawberry.mutation(description="Update a ResearchSubject resource")
        def updateResearchSubject(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("ResearchSubject", _id, dict(data))

        @strawberry.mutation(description="Delete a ResearchSubject resource")
        def deleteResearchSubject(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("ResearchSubject", _id)

        # =====================================================================
        # Infrastructure Mutations
        # =====================================================================

        @strawberry.mutation(description="Create an Endpoint resource")
        def createEndpoint(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("Endpoint", dict(data))

        @strawberry.mutation(description="Update an Endpoint resource")
        def updateEndpoint(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("Endpoint", _id, dict(data))

        @strawberry.mutation(description="Delete an Endpoint resource")
        def deleteEndpoint(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("Endpoint", _id)

        @strawberry.mutation(description="Create an OrganizationAffiliation resource")
        def createOrganizationAffiliation(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("OrganizationAffiliation", dict(data))

        @strawberry.mutation(description="Update an OrganizationAffiliation resource")
        def updateOrganizationAffiliation(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("OrganizationAffiliation", _id, dict(data))

        @strawberry.mutation(description="Delete an OrganizationAffiliation resource")
        def deleteOrganizationAffiliation(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("OrganizationAffiliation", _id)

        @strawberry.mutation(description="Create a SupplyRequest resource")
        def createSupplyRequest(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("SupplyRequest", dict(data))

        @strawberry.mutation(description="Update a SupplyRequest resource")
        def updateSupplyRequest(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("SupplyRequest", _id, dict(data))

        @strawberry.mutation(description="Delete a SupplyRequest resource")
        def deleteSupplyRequest(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("SupplyRequest", _id)

        @strawberry.mutation(description="Create a SupplyDelivery resource")
        def createSupplyDelivery(self, data: JSON) -> Resource:  # type: ignore[valid-type]
            return mutation_resolver.create("SupplyDelivery", dict(data))

        @strawberry.mutation(description="Update a SupplyDelivery resource")
        def updateSupplyDelivery(self, _id: FhirId, data: JSON) -> Optional[Resource]:  # type: ignore[valid-type]
            return mutation_resolver.update("SupplyDelivery", _id, dict(data))

        @strawberry.mutation(description="Delete a SupplyDelivery resource")
        def deleteSupplyDelivery(self, _id: FhirId) -> Optional[Resource]:
            return mutation_resolver.delete("SupplyDelivery", _id)

    # Create and return schema
    return strawberry.Schema(query=Query, mutation=Mutation)


def create_graphql_router(store: FHIRStore) -> GraphQLRouter:
    """Create a FastAPI router for the GraphQL endpoint.

    This creates a GraphQL router that can be mounted in the FastAPI app
    at the desired path (typically /$graphql per FHIR spec).

    Args:
        store: FHIRStore instance for data access

    Returns:
        Configured GraphQLRouter ready to be mounted
    """
    schema = create_schema(store)

    def get_context():
        """Provide context to resolvers."""
        return {"store": store}

    import json

    from fastapi.responses import HTMLResponse
    from starlette.requests import Request

    # Custom GraphQL router with default query in GraphiQL
    class FHIRGraphQLRouter(GraphQLRouter):
        """GraphQL router with custom GraphiQL default query."""

        _custom_html: str = ""

        async def render_graphql_ide(self, request: Request) -> HTMLResponse:
            return HTMLResponse(self._custom_html)

    router = FHIRGraphQLRouter(
        schema=schema,
        context_getter=get_context,  # type: ignore[arg-type]
        graphql_ide="graphiql",
    )

    # Define examples for the dropdown
    examples = [
        {
            "group": "Queries",
            "name": "List patients",
            "query": "{\n  patients(_count: 5) {\n    id\n    resourceType\n    data\n  }\n}",
        },
        {
            "group": "Queries",
            "name": "Search patients by gender",
            "query": '{\n  patients(gender: "female", _count: 5) {\n    id\n    data\n  }\n}',
        },
        {
            "group": "Queries",
            "name": "Get patient by ID",
            "query": '{\n  patient(id: "PATIENT_ID") {\n    id\n    resourceType\n    data\n  }\n}',
        },
        {
            "group": "Queries",
            "name": "List observations",
            "query": "{\n  observations(_count: 10) {\n    id\n    data\n  }\n}",
        },
        {
            "group": "Queries",
            "name": "Observations for patient",
            "query": '{\n  observations(patient: "Patient/PATIENT_ID", _count: 10) {\n    id\n    data\n  }\n}',
        },
        {
            "group": "Queries",
            "name": "List conditions",
            "query": "{\n  conditions(_count: 10) {\n    id\n    data\n  }\n}",
        },
        {
            "group": "Queries",
            "name": "Multiple resources",
            "query": (
                "{\n  p: patients(_count: 3) { id data }\n"
                "  obs: observations(_count: 3) { id data }\n"
                "  cond: conditions(_count: 3) { id data }\n}"
            ),
        },
        {
            "group": "Queries",
            "name": "Generic resource query",
            "query": (
                '{\n  resource(resourceType: "Observation", id: "OBS_ID") {\n    id\n    resourceType\n    data\n  }\n}'
            ),
        },
        {
            "group": "Pagination",
            "name": "Cursor pagination",
            "query": (
                "{\n  patientConnection(first: 5) {\n    edges {\n      cursor\n"
                "      node {\n        id\n        data\n      }\n    }\n"
                "    pageInfo {\n      hasNextPage\n      endCursor\n    }\n"
                "    total\n  }\n}"
            ),
        },
        {
            "group": "Pagination",
            "name": "Offset pagination",
            "query": "{\n  patients(_count: 5, _offset: 0) {\n    id\n    data\n  }\n}",
        },
        {
            "group": "Pagination",
            "name": "Pagination with cursor",
            "query": (
                '{\n  patientConnection(first: 5, after: "CURSOR") {\n    edges {\n'
                "      cursor\n      node { id data }\n    }\n    pageInfo {\n"
                "      hasNextPage\n      hasPreviousPage\n      endCursor\n    }\n  }\n}"
            ),
        },
        {
            "group": "Mutations",
            "name": "Create patient",
            "query": (
                'mutation {\n  createPatient(data: {\n    resourceType: "Patient"\n'
                '    name: [{ family: "Smith", given: ["John"] }]\n    gender: "male"\n'
                '    birthDate: "1990-01-15"\n  }) {\n    id\n    resourceType\n'
                "    data\n  }\n}"
            ),
        },
        {
            "group": "Mutations",
            "name": "Update patient",
            "query": (
                'mutation {\n  updatePatient(id: "PATIENT_ID", data: {\n'
                '    resourceType: "Patient"\n'
                '    name: [{ family: "Updated", given: ["Name"] }]\n'
                '    gender: "male"\n  }) {\n    id\n    data\n  }\n}'
            ),
        },
        {
            "group": "Mutations",
            "name": "Delete patient",
            "query": 'mutation {\n  deletePatient(id: "PATIENT_ID") {\n    id\n  }\n}',
        },
        {
            "group": "Mutations",
            "name": "Generic create",
            "query": (
                'mutation {\n  resourceCreate(resourceType: "Observation", data: {\n'
                '    resourceType: "Observation"\n    status: "final"\n'
                '    code: { text: "Heart Rate" }\n'
                '    valueQuantity: { value: 72, unit: "bpm" }\n'
                "  }) {\n    id\n    resourceType\n    data\n  }\n}"
            ),
        },
    ]

    # Set custom GraphiQL HTML with examples dropdown
    router._custom_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>FHIR GraphQL</title>
    <style>
        body {{ height: 100%; margin: 0; width: 100%; overflow: hidden; }}
        #graphiql {{ height: calc(100vh - 40px); }}
        .toolbar {{
            height: 40px;
            background: #1e1e1e;
            display: flex;
            align-items: center;
            padding: 0 12px;
            border-bottom: 1px solid #333;
        }}
        .toolbar label {{
            color: #ccc;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 13px;
            margin-right: 8px;
        }}
        .toolbar select {{
            background: #2d2d2d;
            color: #fff;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 13px;
            cursor: pointer;
            min-width: 200px;
        }}
        .toolbar select:hover {{
            border-color: #e535ab;
        }}
        .toolbar select optgroup {{
            background: #2d2d2d;
            color: #e535ab;
            font-weight: bold;
        }}
        .toolbar select option {{
            background: #2d2d2d;
            color: #fff;
            padding: 4px;
        }}
    </style>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/graphiql@3/graphiql.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/graphiql@3/graphiql.min.css" />
</head>
<body>
    <div class="toolbar">
        <label for="examples">Examples:</label>
        <select id="examples">
            <option value="">-- Select an example --</option>
        </select>
    </div>
    <div id="graphiql"></div>
    <script>
        const examples = {json.dumps(examples)};

        // Populate dropdown with grouped options
        const select = document.getElementById('examples');
        const groups = {{}};
        examples.forEach((ex, idx) => {{
            if (!groups[ex.group]) {{
                groups[ex.group] = document.createElement('optgroup');
                groups[ex.group].label = ex.group;
                select.appendChild(groups[ex.group]);
            }}
            const option = document.createElement('option');
            option.value = idx;
            option.textContent = ex.name;
            groups[ex.group].appendChild(option);
        }});

        const fetcher = GraphiQL.createFetcher({{
            url: window.location.href,
        }});

        const defaultQuery = "# FHIR GraphQL API\\n" +
            "# Select an example from the dropdown above, or write your own query\\n\\n" +
            "{{\\n  patients(_count: 5) {{\\n    id\\n    resourceType\\n    data\\n  }}\\n}}";

        let graphiqlInstance = null;

        const root = ReactDOM.createRoot(document.getElementById('graphiql'));
        root.render(
            React.createElement(GraphiQL, {{
                fetcher: fetcher,
                defaultQuery: defaultQuery,
                ref: (instance) => {{ graphiqlInstance = instance; }}
            }})
        );

        // Handle example selection
        select.addEventListener('change', (e) => {{
            if (e.target.value !== '') {{
                const example = examples[parseInt(e.target.value)];
                // Access the query editor through GraphiQL's API
                if (graphiqlInstance && graphiqlInstance.getQueryEditor) {{
                    graphiqlInstance.getQueryEditor().setValue(example.query);
                }} else {{
                    // Fallback: find and update the CodeMirror instance
                    const cm = document.querySelector('.graphiql-query-editor .CodeMirror');
                    if (cm && cm.CodeMirror) {{
                        cm.CodeMirror.setValue(example.query);
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    logger.info("GraphQL schema created with %d resource types", len(SUPPORTED_TYPES))

    return router
