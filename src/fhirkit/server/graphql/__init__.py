"""GraphQL API for FHIR resources.

This module provides a FHIR-compliant GraphQL endpoint following the
[FHIR GraphQL specification](https://hl7.org/fhir/graphql.html).

Features:
- Query any FHIR resource by ID
- Search resources with FHIR search parameters
- Cursor-based pagination via GraphQL Connections
- Inline reference resolution
- Create, Update, Delete mutations

Usage:
    from fhirkit.server.graphql import create_graphql_router
    from fhirkit.server.storage.fhir_store import FHIRStore

    store = FHIRStore()
    graphql_router = create_graphql_router(store)

    # Mount in FastAPI app
    app.include_router(graphql_router, prefix="/baseR4/$graphql")
"""

from .resolvers import (
    ConnectionResolver,
    ListResolver,
    MutationResolver,
    ResourceResolver,
)
from .schema import create_graphql_router, create_schema
from .types import (
    Address,
    CodeableConcept,
    Coding,
    ContactPoint,
    HumanName,
    Identifier,
    Meta,
    PageInfo,
    Period,
    Quantity,
    Reference,
    Resource,
    ResourceConnection,
    ResourceEdge,
    ResourceInput,
    SearchEntryMode,
    decode_cursor,
    encode_cursor,
)
from .utils import (
    build_search_params,
    fhir_param_to_graphql,
    graphql_param_to_fhir,
)

__all__ = [
    # Schema creation
    "create_graphql_router",
    "create_schema",
    # Types
    "Resource",
    "ResourceConnection",
    "ResourceEdge",
    "ResourceInput",
    "PageInfo",
    "SearchEntryMode",
    "Reference",
    "HumanName",
    "ContactPoint",
    "Address",
    "Coding",
    "CodeableConcept",
    "Identifier",
    "Meta",
    "Period",
    "Quantity",
    # Cursor utilities
    "encode_cursor",
    "decode_cursor",
    # Resolvers
    "ResourceResolver",
    "ListResolver",
    "ConnectionResolver",
    "MutationResolver",
    # Utilities
    "fhir_param_to_graphql",
    "graphql_param_to_fhir",
    "build_search_params",
]
