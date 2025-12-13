"""FHIR REST API routes."""

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import JSONResponse

from ..models.responses import Bundle, BundleEntry, BundleEntryRequest, CapabilityStatement, OperationOutcome
from ..storage.fhir_store import FHIRStore

# FHIR content type
FHIR_JSON = "application/fhir+json"

# Supported resource types
SUPPORTED_TYPES = [
    "Patient",
    "Practitioner",
    "Organization",
    "Encounter",
    "Condition",
    "Observation",
    "MedicationRequest",
    "Procedure",
    "ValueSet",
    "CodeSystem",
    "Library",
]


def create_router(store: FHIRStore, base_url: str = "") -> APIRouter:
    """Create FHIR API router.

    Args:
        store: The FHIR data store
        base_url: Base URL for the server

    Returns:
        Configured APIRouter
    """
    router = APIRouter()

    def get_base_url(request: Request) -> str:
        """Get base URL from request or config."""
        if base_url:
            return base_url.rstrip("/")
        return str(request.base_url).rstrip("/")

    # =========================================================================
    # Capability Statement (metadata)
    # =========================================================================

    @router.get("/metadata", tags=["Capability"])
    async def get_metadata(request: Request) -> Response:
        """Return the CapabilityStatement for this server.

        This endpoint describes the server's capabilities including:
        - Supported resource types
        - Supported interactions (read, search, create, update, delete)
        - Supported search parameters
        - Server information
        """
        capability = CapabilityStatement.default(base_url=get_base_url(request))
        return JSONResponse(
            content=capability.model_dump(exclude_none=True),
            media_type=FHIR_JSON,
        )

    @router.get("/.well-known/smart-configuration", tags=["Capability"])
    async def get_smart_config(request: Request) -> Response:
        """Return SMART on FHIR configuration.

        Basic SMART configuration for discovery.
        """
        config = {
            "issuer": get_base_url(request),
            "authorization_endpoint": f"{get_base_url(request)}/auth/authorize",
            "token_endpoint": f"{get_base_url(request)}/auth/token",
            "capabilities": [
                "launch-standalone",
                "client-public",
                "client-confidential-symmetric",
                "context-standalone-patient",
                "permission-offline",
                "permission-patient",
            ],
        }
        return JSONResponse(content=config, media_type="application/json")

    # =========================================================================
    # Resource Operations
    # =========================================================================

    @router.get("/{resource_type}", tags=["Search"])
    async def search_type(
        request: Request,
        resource_type: str,
        _count: int = Query(default=100, ge=1, le=1000, alias="_count"),
        _offset: int = Query(default=0, ge=0, alias="_offset"),
        _sort: str | None = Query(default=None, alias="_sort"),
        _include: list[str] | None = Query(default=None, alias="_include"),
        _revinclude: list[str] | None = Query(default=None, alias="_revinclude"),
    ) -> Response:
        """Search for resources of a specific type.

        Supports standard FHIR search parameters for each resource type.
        Common parameters:
        - _id: Resource ID
        - _count: Number of results per page (default 100, max 1000)
        - _offset: Offset for pagination
        - _sort: Sort order (prefix with - for descending)
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Get search params from query string
        params: dict[str, Any] = {}
        for key, value in request.query_params.multi_items():
            if not key.startswith("_") or key in ("_id", "_lastUpdated"):
                if key in params:
                    if isinstance(params[key], list):
                        params[key].append(value)
                    else:
                        params[key] = [params[key], value]
                else:
                    params[key] = value

        # Search with pagination
        resources, total = store.search(
            resource_type=resource_type,
            params=params,
            _count=_count,
            _offset=_offset,
        )

        # Apply sorting if specified
        if _sort:
            reverse = _sort.startswith("-")
            sort_field = _sort.lstrip("-")
            try:
                resources = sorted(
                    resources,
                    key=lambda r: r.get(sort_field, "") or "",
                    reverse=reverse,
                )
            except (TypeError, KeyError):
                pass  # Ignore sort errors

        # Build bundle
        bundle = Bundle.searchset(
            resources=resources,
            total=total,
            base_url=get_base_url(request),
            resource_type=resource_type,
            params=params,
            offset=_offset,
            count=_count,
        )

        return JSONResponse(
            content=bundle.model_dump(exclude_none=True),
            media_type=FHIR_JSON,
        )

    @router.get("/{resource_type}/{resource_id}", tags=["Read"])
    async def read(
        request: Request,
        resource_type: str,
        resource_id: str,
    ) -> Response:
        """Read a specific resource by ID.

        Returns the current version of the resource.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        resource = store.read(resource_type, resource_id)
        if resource is None:
            outcome = OperationOutcome.not_found(resource_type, resource_id)
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        # Set ETag header
        version = resource.get("meta", {}).get("versionId", "1")
        return JSONResponse(
            content=resource,
            media_type=FHIR_JSON,
            headers={"ETag": f'W/"{version}"'},
        )

    @router.get("/{resource_type}/{resource_id}/_history", tags=["History"])
    async def history_instance(
        request: Request,
        resource_type: str,
        resource_id: str,
    ) -> Response:
        """Get the history of a specific resource.

        Returns all versions of the resource as a Bundle.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        versions = store.history(resource_type, resource_id)
        if not versions:
            outcome = OperationOutcome.not_found(resource_type, resource_id)
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        # Build history bundle
        bundle = Bundle(
            resourceType="Bundle",
            id=str(uuid.uuid4()),
            type="history",
            total=len(versions),
            entry=[
                BundleEntry(
                    fullUrl=f"{get_base_url(request)}/{resource_type}/{resource_id}",
                    resource=v,
                    request=BundleEntryRequest(
                        method="GET",
                        url=f"{resource_type}/{resource_id}/_history/{v.get('meta', {}).get('versionId', '1')}",
                    ),
                )
                for v in versions
            ],
        )

        return JSONResponse(
            content=bundle.model_dump(exclude_none=True),
            media_type=FHIR_JSON,
        )

    @router.get("/{resource_type}/{resource_id}/_history/{version_id}", tags=["History"])
    async def vread(
        request: Request,
        resource_type: str,
        resource_id: str,
        version_id: str,
    ) -> Response:
        """Read a specific version of a resource.

        Returns the specified version of the resource.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        versions = store.history(resource_type, resource_id)
        for v in versions:
            if v.get("meta", {}).get("versionId") == version_id:
                return JSONResponse(
                    content=v,
                    media_type=FHIR_JSON,
                    headers={"ETag": f'W/"{version_id}"'},
                )

        outcome = OperationOutcome.not_found(resource_type, f"{resource_id}/_history/{version_id}")
        return JSONResponse(
            content=outcome.model_dump(exclude_none=True),
            status_code=404,
            media_type=FHIR_JSON,
        )

    @router.post("/{resource_type}", tags=["Create"], status_code=201)
    async def create(
        request: Request,
        resource_type: str,
    ) -> Response:
        """Create a new resource.

        The server assigns an ID to the resource.
        Returns 201 Created with Location header.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        try:
            body = await request.json()
        except Exception as e:
            outcome = OperationOutcome.error(f"Invalid JSON: {e}", code="invalid")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Validate resource type matches
        if body.get("resourceType") != resource_type:
            outcome = OperationOutcome.error(
                f"Resource type in body ({body.get('resourceType')}) does not match URL ({resource_type})",
                code="invalid",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Create resource
        created = store.create(body)
        resource_id = created["id"]
        version = created.get("meta", {}).get("versionId", "1")

        return JSONResponse(
            content=created,
            status_code=201,
            media_type=FHIR_JSON,
            headers={
                "Location": f"{get_base_url(request)}/{resource_type}/{resource_id}",
                "ETag": f'W/"{version}"',
            },
        )

    @router.put("/{resource_type}/{resource_id}", tags=["Update"])
    async def update(
        request: Request,
        resource_type: str,
        resource_id: str,
    ) -> Response:
        """Update an existing resource or create with specific ID.

        If the resource exists, updates it and increments version.
        If not, creates it with the specified ID.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        try:
            body = await request.json()
        except Exception as e:
            outcome = OperationOutcome.error(f"Invalid JSON: {e}", code="invalid")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Validate resource type
        if body.get("resourceType") != resource_type:
            outcome = OperationOutcome.error(
                f"Resource type in body ({body.get('resourceType')}) does not match URL ({resource_type})",
                code="invalid",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Validate ID matches
        if body.get("id") and body.get("id") != resource_id:
            outcome = OperationOutcome.error(
                f"Resource ID in body ({body.get('id')}) does not match URL ({resource_id})",
                code="invalid",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Check if creating or updating
        existing = store.read(resource_type, resource_id)
        is_create = existing is None

        # Update or create
        updated = store.update(resource_type, resource_id, body)
        version = updated.get("meta", {}).get("versionId", "1")

        return JSONResponse(
            content=updated,
            status_code=201 if is_create else 200,
            media_type=FHIR_JSON,
            headers={
                "Location": f"{get_base_url(request)}/{resource_type}/{resource_id}",
                "ETag": f'W/"{version}"',
            },
        )

    @router.delete("/{resource_type}/{resource_id}", tags=["Delete"])
    async def delete(
        request: Request,
        resource_type: str,
        resource_id: str,
    ) -> Response:
        """Delete a resource.

        Returns 204 No Content on success, 404 if not found.
        """
        if resource_type not in SUPPORTED_TYPES:
            outcome = OperationOutcome.error(
                f"Resource type '{resource_type}' is not supported",
                code="not-supported",
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        deleted = store.delete(resource_type, resource_id)
        if not deleted:
            outcome = OperationOutcome.not_found(resource_type, resource_id)
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        return Response(status_code=204)

    # =========================================================================
    # Terminology Operations
    # =========================================================================

    @router.get("/ValueSet/$expand", tags=["Terminology"])
    @router.post("/ValueSet/$expand", tags=["Terminology"])
    async def expand_valueset(
        request: Request,
        url: str | None = Query(default=None),
        filter: str | None = Query(default=None),
        count: int = Query(default=100, ge=1, le=1000),
        offset: int = Query(default=0, ge=0),
    ) -> Response:
        """Expand a ValueSet.

        Expands the ValueSet to include all codes.
        Supports filtering by code/display text.
        """
        # For POST, get parameters from body
        if request.method == "POST":
            try:
                body = await request.json()
                url = body.get("parameter", [{}])[0].get("valueUri", url)
                for param in body.get("parameter", []):
                    if param.get("name") == "url":
                        url = param.get("valueUri")
                    elif param.get("name") == "filter":
                        filter = param.get("valueString")
            except Exception:
                pass

        if not url:
            outcome = OperationOutcome.error("ValueSet URL is required", code="required")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Find ValueSet by URL
        valuesets, _ = store.search("ValueSet", {"url": url})
        if not valuesets:
            outcome = OperationOutcome.error(f"ValueSet not found: {url}", code="not-found")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        valueset = valuesets[0]

        # Extract codes from compose
        codes = []
        compose = valueset.get("compose", {})
        for include in compose.get("include", []):
            system = include.get("system", "")
            for concept in include.get("concept", []):
                codes.append(
                    {
                        "system": system,
                        "code": concept.get("code"),
                        "display": concept.get("display"),
                    }
                )

        # Apply filter if specified
        if filter:
            filter_lower = filter.lower()
            codes = [
                c
                for c in codes
                if filter_lower in (c.get("display", "").lower()) or filter_lower in (c.get("code", "").lower())
            ]

        # Apply pagination
        total = len(codes)
        codes = codes[offset : offset + count]

        # Build expansion
        expansion = {
            "resourceType": "ValueSet",
            "id": valueset.get("id"),
            "url": url,
            "status": valueset.get("status", "active"),
            "expansion": {
                "identifier": f"urn:uuid:{uuid.uuid4()}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total": total,
                "offset": offset,
                "contains": codes,
            },
        }

        return JSONResponse(content=expansion, media_type=FHIR_JSON)

    @router.get("/ValueSet/{valueset_id}/$expand", tags=["Terminology"])
    async def expand_valueset_by_id(
        request: Request,
        valueset_id: str,
        filter: str | None = Query(default=None),
        count: int = Query(default=100, ge=1, le=1000),
        offset: int = Query(default=0, ge=0),
    ) -> Response:
        """Expand a specific ValueSet by ID."""
        valueset = store.read("ValueSet", valueset_id)
        if valueset is None:
            outcome = OperationOutcome.not_found("ValueSet", valueset_id)
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        # Extract codes
        codes = []
        compose = valueset.get("compose", {})
        for include in compose.get("include", []):
            system = include.get("system", "")
            for concept in include.get("concept", []):
                codes.append(
                    {
                        "system": system,
                        "code": concept.get("code"),
                        "display": concept.get("display"),
                    }
                )

        # Apply filter
        if filter:
            filter_lower = filter.lower()
            codes = [
                c
                for c in codes
                if filter_lower in (c.get("display", "").lower()) or filter_lower in (c.get("code", "").lower())
            ]

        # Pagination
        total = len(codes)
        codes = codes[offset : offset + count]

        expansion = {
            "resourceType": "ValueSet",
            "id": valueset_id,
            "url": valueset.get("url"),
            "status": valueset.get("status", "active"),
            "expansion": {
                "identifier": f"urn:uuid:{uuid.uuid4()}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total": total,
                "offset": offset,
                "contains": codes,
            },
        }

        return JSONResponse(content=expansion, media_type=FHIR_JSON)

    @router.get("/CodeSystem/$lookup", tags=["Terminology"])
    @router.post("/CodeSystem/$lookup", tags=["Terminology"])
    async def lookup_code(
        request: Request,
        system: str | None = Query(default=None),
        code: str | None = Query(default=None),
    ) -> Response:
        """Look up a code in a CodeSystem.

        Returns information about the code including display text.
        """
        # For POST, get parameters from body
        if request.method == "POST":
            try:
                body = await request.json()
                for param in body.get("parameter", []):
                    if param.get("name") == "system":
                        system = param.get("valueUri")
                    elif param.get("name") == "code":
                        code = param.get("valueCode")
            except Exception:
                pass

        if not system or not code:
            outcome = OperationOutcome.error("Both system and code are required", code="required")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Find CodeSystem by URL
        codesystems, _ = store.search("CodeSystem", {"url": system})
        if not codesystems:
            outcome = OperationOutcome.error(f"CodeSystem not found: {system}", code="not-found")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        codesystem = codesystems[0]

        # Find the code
        for concept in codesystem.get("concept", []):
            if concept.get("code") == code:
                params: list[dict[str, Any]] = [
                    {"name": "name", "valueString": codesystem.get("name")},
                    {"name": "display", "valueString": concept.get("display")},
                    {"name": "code", "valueCode": code},
                    {"name": "system", "valueUri": system},
                ]
                if concept.get("definition"):
                    params.append({"name": "definition", "valueString": concept.get("definition")})
                result = {"resourceType": "Parameters", "parameter": params}
                return JSONResponse(content=result, media_type=FHIR_JSON)

        outcome = OperationOutcome.error(f"Code '{code}' not found in CodeSystem", code="not-found")
        return JSONResponse(
            content=outcome.model_dump(exclude_none=True),
            status_code=404,
            media_type=FHIR_JSON,
        )

    @router.get("/ValueSet/$validate-code", tags=["Terminology"])
    @router.post("/ValueSet/$validate-code", tags=["Terminology"])
    async def validate_code(
        request: Request,
        url: str | None = Query(default=None),
        system: str | None = Query(default=None),
        code: str | None = Query(default=None),
    ) -> Response:
        """Validate that a code is in a ValueSet.

        Returns whether the code is valid and its display text.
        """
        # For POST, get parameters from body
        if request.method == "POST":
            try:
                body = await request.json()
                for param in body.get("parameter", []):
                    if param.get("name") == "url":
                        url = param.get("valueUri")
                    elif param.get("name") == "system":
                        system = param.get("valueUri")
                    elif param.get("name") == "code":
                        code = param.get("valueCode")
            except Exception:
                pass

        if not url or not code:
            outcome = OperationOutcome.error("ValueSet URL and code are required", code="required")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        # Find ValueSet
        valuesets, _ = store.search("ValueSet", {"url": url})
        if not valuesets:
            outcome = OperationOutcome.error(f"ValueSet not found: {url}", code="not-found")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=404,
                media_type=FHIR_JSON,
            )

        valueset = valuesets[0]

        # Check if code is in ValueSet
        found = False
        display = None
        compose = valueset.get("compose", {})
        for include in compose.get("include", []):
            include_system = include.get("system", "")
            if system and include_system != system:
                continue
            for concept in include.get("concept", []):
                if concept.get("code") == code:
                    found = True
                    display = concept.get("display")
                    break
            if found:
                break

        params: list[dict[str, Any]] = [{"name": "result", "valueBoolean": found}]
        if found and display:
            params.append({"name": "display", "valueString": display})
        if not found:
            params.append({"name": "message", "valueString": f"Code '{code}' not found in ValueSet"})

        result = {"resourceType": "Parameters", "parameter": params}
        return JSONResponse(content=result, media_type=FHIR_JSON)

    # =========================================================================
    # Batch/Transaction
    # =========================================================================

    @router.post("/", tags=["Batch"])
    async def batch_transaction(request: Request) -> Response:
        """Process a batch or transaction Bundle.

        Processes all entries in the bundle and returns results.
        """
        try:
            body = await request.json()
        except Exception as e:
            outcome = OperationOutcome.error(f"Invalid JSON: {e}", code="invalid")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        if body.get("resourceType") != "Bundle":
            outcome = OperationOutcome.error("Expected a Bundle resource", code="invalid")
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        bundle_type = body.get("type")
        if bundle_type not in ("batch", "transaction"):
            outcome = OperationOutcome.error(
                f"Bundle type must be 'batch' or 'transaction', got '{bundle_type}'", code="invalid"
            )
            return JSONResponse(
                content=outcome.model_dump(exclude_none=True),
                status_code=400,
                media_type=FHIR_JSON,
            )

        entries = body.get("entry", [])
        response_entries = []

        for entry in entries:
            resource = entry.get("resource")
            req = entry.get("request", {})
            method = req.get("method", "").upper()
            url = req.get("url", "")

            # Parse URL to get resource type and ID
            url_parts = url.strip("/").split("/")
            resource_type = url_parts[0] if url_parts else ""
            resource_id = url_parts[1] if len(url_parts) > 1 else None

            response_entry: dict[str, Any] = {"response": {}}

            try:
                if method == "GET":
                    if resource_id:
                        result = store.read(resource_type, resource_id)
                        if result:
                            response_entry["resource"] = result
                            response_entry["response"]["status"] = "200 OK"
                        else:
                            response_entry["response"]["status"] = "404 Not Found"
                    else:
                        # Search - simplified
                        resources, total = store.search(resource_type, {})
                        response_entry["resource"] = {
                            "resourceType": "Bundle",
                            "type": "searchset",
                            "total": total,
                            "entry": [{"resource": r} for r in resources[:100]],
                        }
                        response_entry["response"]["status"] = "200 OK"

                elif method == "POST":
                    if resource and resource_type:
                        created = store.create(resource)
                        response_entry["resource"] = created
                        response_entry["response"]["status"] = "201 Created"
                        response_entry["response"]["location"] = f"{resource_type}/{created['id']}"
                    else:
                        response_entry["response"]["status"] = "400 Bad Request"

                elif method == "PUT":
                    if resource and resource_type and resource_id:
                        updated = store.update(resource_type, resource_id, resource)
                        response_entry["resource"] = updated
                        response_entry["response"]["status"] = "200 OK"
                    else:
                        response_entry["response"]["status"] = "400 Bad Request"

                elif method == "DELETE":
                    if resource_type and resource_id:
                        deleted = store.delete(resource_type, resource_id)
                        response_entry["response"]["status"] = "204 No Content" if deleted else "404 Not Found"
                    else:
                        response_entry["response"]["status"] = "400 Bad Request"

                else:
                    response_entry["response"]["status"] = "400 Bad Request"

            except Exception as e:
                response_entry["response"]["status"] = "500 Internal Server Error"
                response_entry["response"]["outcome"] = OperationOutcome.error(str(e)).model_dump(exclude_none=True)

            response_entries.append(response_entry)

        response_bundle = {
            "resourceType": "Bundle",
            "id": str(uuid.uuid4()),
            "type": "batch-response" if bundle_type == "batch" else "transaction-response",
            "entry": response_entries,
        }

        return JSONResponse(content=response_bundle, media_type=FHIR_JSON)

    return router
