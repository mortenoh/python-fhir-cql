"""FHIR Server response models."""

from typing import Any

from pydantic import BaseModel, Field


class OperationOutcomeIssue(BaseModel):
    """FHIR OperationOutcome.issue element."""

    severity: str = Field(description="fatal | error | warning | information")
    code: str = Field(description="Error or warning code")
    details: dict[str, Any] | None = Field(default=None, description="Additional details")
    diagnostics: str | None = Field(default=None, description="Additional diagnostic information")
    location: list[str] = Field(default_factory=list, description="Path of element(s) related to issue")
    expression: list[str] = Field(default_factory=list, description="FHIRPath of element(s)")


class OperationOutcome(BaseModel):
    """FHIR OperationOutcome resource."""

    resourceType: str = "OperationOutcome"
    id: str | None = None
    issue: list[OperationOutcomeIssue] = Field(default_factory=list)

    @classmethod
    def error(cls, message: str, code: str = "processing") -> "OperationOutcome":
        """Create an error OperationOutcome."""
        return cls(
            issue=[
                OperationOutcomeIssue(
                    severity="error",
                    code=code,
                    diagnostics=message,
                )
            ]
        )

    @classmethod
    def not_found(cls, resource_type: str, resource_id: str) -> "OperationOutcome":
        """Create a not-found OperationOutcome."""
        return cls(
            issue=[
                OperationOutcomeIssue(
                    severity="error",
                    code="not-found",
                    diagnostics=f"{resource_type}/{resource_id} not found",
                )
            ]
        )

    @classmethod
    def deleted(cls, resource_type: str, resource_id: str) -> "OperationOutcome":
        """Create a deleted OperationOutcome."""
        return cls(
            issue=[
                OperationOutcomeIssue(
                    severity="information",
                    code="deleted",
                    diagnostics=f"{resource_type}/{resource_id} has been deleted",
                )
            ]
        )


class BundleLink(BaseModel):
    """FHIR Bundle.link element."""

    relation: str
    url: str


class BundleEntryRequest(BaseModel):
    """FHIR Bundle.entry.request element."""

    method: str
    url: str


class BundleEntryResponse(BaseModel):
    """FHIR Bundle.entry.response element."""

    status: str
    location: str | None = None
    etag: str | None = None
    lastModified: str | None = None


class BundleEntry(BaseModel):
    """FHIR Bundle.entry element."""

    fullUrl: str | None = None
    resource: dict[str, Any] | None = None
    request: BundleEntryRequest | None = None
    response: BundleEntryResponse | None = None
    search: dict[str, Any] | None = None


class Bundle(BaseModel):
    """FHIR Bundle resource."""

    resourceType: str = "Bundle"
    id: str | None = None
    type: str = Field(..., description="document | message | transaction | searchset | collection | ...")
    total: int | None = None
    link: list[BundleLink] = Field(default_factory=list)
    entry: list[BundleEntry] = Field(default_factory=list)
    timestamp: str | None = None

    @classmethod
    def searchset(
        cls,
        resources: list[dict[str, Any]],
        total: int,
        base_url: str,
        resource_type: str,
        params: dict[str, str] | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> "Bundle":
        """Create a searchset Bundle from resources."""
        entries = []
        for resource in resources:
            rid = resource.get("id", "")
            rtype = resource.get("resourceType", resource_type)
            entries.append(
                BundleEntry(
                    fullUrl=f"{base_url}/{rtype}/{rid}",
                    resource=resource,
                    search={"mode": "match"},
                )
            )

        # Build links
        links = [BundleLink(relation="self", url=f"{base_url}/{resource_type}")]

        # Add pagination links
        if offset > 0:
            prev_offset = max(0, offset - count)
            links.append(
                BundleLink(relation="previous", url=f"{base_url}/{resource_type}?_offset={prev_offset}&_count={count}")
            )

        if offset + count < total:
            next_offset = offset + count
            links.append(
                BundleLink(relation="next", url=f"{base_url}/{resource_type}?_offset={next_offset}&_count={count}")
            )

        return cls(
            type="searchset",
            total=total,
            link=links,
            entry=entries,
        )

    @classmethod
    def collection(cls, resources: list[dict[str, Any]], base_url: str = "") -> "Bundle":
        """Create a collection Bundle from resources."""
        entries = []
        for resource in resources:
            rid = resource.get("id", "")
            rtype = resource.get("resourceType", "")
            entries.append(
                BundleEntry(
                    fullUrl=f"{base_url}/{rtype}/{rid}" if base_url else f"urn:uuid:{rid}",
                    resource=resource,
                )
            )

        return cls(
            type="collection",
            entry=entries,
        )


class CapabilityStatementRestResource(BaseModel):
    """FHIR CapabilityStatement.rest.resource element."""

    type: str
    interaction: list[dict[str, str]] = Field(default_factory=list)
    searchParam: list[dict[str, str]] = Field(default_factory=list)
    searchInclude: list[str] = Field(default_factory=list)
    searchRevInclude: list[str] = Field(default_factory=list)
    versioning: str = "versioned"
    readHistory: bool = True
    updateCreate: bool = True
    operation: list[dict[str, Any]] = Field(default_factory=list)


class CapabilityStatementRest(BaseModel):
    """FHIR CapabilityStatement.rest element."""

    mode: str = "server"
    resource: list[CapabilityStatementRestResource] = Field(default_factory=list)
    operation: list[dict[str, Any]] = Field(default_factory=list)


class CapabilityStatement(BaseModel):
    """FHIR CapabilityStatement resource."""

    resourceType: str = "CapabilityStatement"
    id: str = "fhir-server"
    url: str | None = None
    version: str = "1.0.0"
    name: str = "FHIRServer"
    title: str = "FHIR Server"
    status: str = "active"
    experimental: bool = True
    date: str | None = None
    publisher: str = "python-fhir-cql"
    description: str = "Simple FHIR R4 server with synthetic data generation"
    kind: str = "instance"
    fhirVersion: str = "4.0.1"
    format: list[str] = Field(default_factory=lambda: ["json"])
    rest: list[CapabilityStatementRest] = Field(default_factory=list)

    @classmethod
    def default(cls, base_url: str = "") -> "CapabilityStatement":
        """Create a default CapabilityStatement with all supported resources and operations."""
        from datetime import datetime, timezone

        from ..api.include_handler import get_search_includes, get_search_rev_includes
        from ..api.routes import SUPPORTED_TYPES
        from ..api.search import SEARCH_PARAMS

        # Resource-specific operations
        RESOURCE_OPERATIONS: dict[str, list[dict[str, str]]] = {
            "Patient": [
                {"name": "everything", "definition": "http://hl7.org/fhir/OperationDefinition/Patient-everything"},
                {"name": "summary", "definition": "http://hl7.org/fhir/uv/ips/OperationDefinition/summary"},
                {"name": "export", "definition": "http://hl7.org/fhir/uv/bulkdata/OperationDefinition/patient-export"},
                {"name": "match", "definition": "http://hl7.org/fhir/OperationDefinition/Patient-match"},
                {"name": "validate", "definition": "http://hl7.org/fhir/OperationDefinition/Resource-validate"},
            ],
            "Group": [
                {"name": "export", "definition": "http://hl7.org/fhir/uv/bulkdata/OperationDefinition/group-export"},
            ],
            "Measure": [
                {
                    "name": "evaluate-measure",
                    "definition": "http://hl7.org/fhir/OperationDefinition/Measure-evaluate-measure",
                },
            ],
            "ValueSet": [
                {"name": "expand", "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-expand"},
                {
                    "name": "validate-code",
                    "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-validate-code",
                },
            ],
            "CodeSystem": [
                {"name": "lookup", "definition": "http://hl7.org/fhir/OperationDefinition/CodeSystem-lookup"},
                {"name": "subsumes", "definition": "http://hl7.org/fhir/OperationDefinition/CodeSystem-subsumes"},
            ],
            "ConceptMap": [
                {"name": "translate", "definition": "http://hl7.org/fhir/OperationDefinition/ConceptMap-translate"},
            ],
            "Composition": [
                {"name": "document", "definition": "http://hl7.org/fhir/OperationDefinition/Composition-document"},
            ],
        }

        resources = []
        for rtype in SUPPORTED_TYPES:
            # Get search parameters with correct types from SEARCH_PARAMS
            search_params_def = SEARCH_PARAMS.get(rtype, {})
            search_params = [
                {"name": name, "type": info.get("type", "string")} for name, info in search_params_def.items()
            ]
            # Add common params if not already present
            common_params = [
                {"name": "_lastUpdated", "type": "date"},
                {"name": "_contained", "type": "token"},
            ]
            existing_names = {p["name"] for p in search_params}
            for p in common_params:
                if p["name"] not in existing_names:
                    search_params.append(p)

            # Get _include and _revinclude capabilities
            search_include = get_search_includes(rtype)
            search_rev_include = get_search_rev_includes(rtype)

            # Get resource-specific operations
            resource_operations = RESOURCE_OPERATIONS.get(rtype, [])

            # Add validate operation to all resources
            if rtype not in RESOURCE_OPERATIONS or not any(
                op["name"] == "validate" for op in RESOURCE_OPERATIONS.get(rtype, [])
            ):
                resource_operations = list(resource_operations) + [
                    {"name": "validate", "definition": "http://hl7.org/fhir/OperationDefinition/Resource-validate"}
                ]

            resources.append(
                CapabilityStatementRestResource(
                    type=rtype,
                    interaction=[
                        {"code": "read"},
                        {"code": "vread"},
                        {"code": "update"},
                        {"code": "delete"},
                        {"code": "history-instance"},
                        {"code": "create"},
                        {"code": "search-type"},
                    ],
                    searchParam=search_params,
                    searchInclude=search_include,
                    searchRevInclude=search_rev_include,
                    operation=resource_operations,
                )
            )

        # Server-level operations
        server_operations = [
            {"name": "fhirpath", "definition": "http://hl7.org/fhir/OperationDefinition/fhirpath"},
            {"name": "cql", "definition": "http://cql.hl7.org/OperationDefinition/cql-cql"},
            {"name": "export", "definition": "http://hl7.org/fhir/uv/bulkdata/OperationDefinition/export"},
        ]

        return cls(
            url=f"{base_url}/metadata" if base_url else None,
            date=datetime.now(timezone.utc).isoformat(),
            rest=[
                CapabilityStatementRest(
                    mode="server",
                    resource=resources,
                    operation=server_operations,
                )
            ],
        )
