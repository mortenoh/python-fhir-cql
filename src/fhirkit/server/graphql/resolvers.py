"""GraphQL resolvers for FHIR resources.

This module contains resolver functions that bridge GraphQL queries/mutations
to the underlying FHIR store operations.
"""

from typing import Any, Optional

from .types import (
    PageInfo,
    Resource,
    ResourceConnection,
    ResourceEdge,
    SearchEntryMode,
    decode_cursor,
    encode_cursor,
)
from .utils import graphql_param_to_fhir


class ResourceResolver:
    """Resolver for single resource queries.

    Handles queries like:
        Patient(_id: "123") -> Resource
    """

    def __init__(self, store: Any):
        """Initialize resolver with FHIR store.

        Args:
            store: FHIRStore instance
        """
        self.store = store

    def resolve(self, resource_type: str, _id: str) -> Optional[Resource]:
        """Resolve a single resource by ID.

        Args:
            resource_type: The FHIR resource type (e.g., "Patient")
            _id: The resource ID

        Returns:
            Resource if found, None otherwise
        """
        data = self.store.read(resource_type, _id)
        if data:
            return Resource.from_dict(data)
        return None


class ListResolver:
    """Resolver for list queries with search parameters.

    Handles queries like:
        PatientList(name: "Smith", gender: "male", _count: 10) -> [Resource]
    """

    def __init__(self, store: Any):
        """Initialize resolver with FHIR store.

        Args:
            store: FHIRStore instance
        """
        self.store = store

    def resolve(
        self,
        resource_type: str,
        _count: int = 100,
        _offset: int = 0,
        _sort: Optional[str] = None,
        **search_params: Any,
    ) -> list[Resource]:
        """Resolve a list query with search parameters.

        Args:
            resource_type: The FHIR resource type
            _count: Maximum number of results to return
            _offset: Number of results to skip
            _sort: Sort parameter (e.g., "-date" for descending)
            **search_params: Additional search parameters

        Returns:
            List of matching resources
        """
        # Import here to avoid circular imports
        from ..api.search import filter_resources_advanced, sort_resources

        # Convert GraphQL param names to FHIR param names
        fhir_params = {}
        for key, value in search_params.items():
            if value is not None:
                fhir_key = graphql_param_to_fhir(key)
                fhir_params[fhir_key] = value

        # Get all resources of type
        resources = self.store.get_all_resources(resource_type)

        # Apply filters
        if fhir_params:
            filtered = filter_resources_advanced(resources, resource_type, fhir_params, self.store)
        else:
            filtered = resources

        # Apply sorting
        if _sort:
            filtered = sort_resources(filtered, _sort, resource_type)

        # Apply pagination
        paginated = filtered[_offset : _offset + _count]

        # Convert to Resource types
        return [Resource.from_dict(r) for r in paginated]


class ConnectionResolver:
    """Resolver for connection queries with cursor-based pagination.

    Handles queries like:
        PatientConnection(first: 10, after: "cursor") -> ResourceConnection

    Implements the Relay-style connection pattern for FHIR resources.
    """

    def __init__(self, store: Any):
        """Initialize resolver with FHIR store.

        Args:
            store: FHIRStore instance
        """
        self.store = store

    def resolve(
        self,
        resource_type: str,
        first: Optional[int] = None,
        after: Optional[str] = None,
        last: Optional[int] = None,
        before: Optional[str] = None,
        _sort: Optional[str] = None,
        **search_params: Any,
    ) -> ResourceConnection:
        """Resolve a connection query with cursor-based pagination.

        Args:
            resource_type: The FHIR resource type
            first: Number of items to fetch from start
            after: Cursor to fetch items after
            last: Number of items to fetch from end
            before: Cursor to fetch items before
            _sort: Sort parameter
            **search_params: Additional search parameters

        Returns:
            ResourceConnection with edges and page info
        """
        # Import here to avoid circular imports
        from ..api.search import filter_resources_advanced, sort_resources

        # Convert GraphQL param names to FHIR param names
        fhir_params = {}
        for key, value in search_params.items():
            if value is not None:
                fhir_key = graphql_param_to_fhir(key)
                fhir_params[fhir_key] = value

        # Get all resources of type
        resources = self.store.get_all_resources(resource_type)

        # Apply filters
        if fhir_params:
            filtered = filter_resources_advanced(resources, resource_type, fhir_params, self.store)
        else:
            filtered = resources

        # Apply sorting
        if _sort:
            filtered = sort_resources(filtered, _sort, resource_type)

        total = len(filtered)

        # Calculate offset from cursor
        offset = 0
        count = first or last or 10  # Default to 10

        if after:
            offset = decode_cursor(after) + 1
        elif before:
            before_offset = decode_cursor(before)
            if last:
                offset = max(0, before_offset - last)
            else:
                offset = max(0, before_offset - count)

        # Slice results
        results = filtered[offset : offset + count]

        # Build edges
        edges = []
        for i, resource in enumerate(results):
            edge = ResourceEdge(
                cursor=encode_cursor(offset + i),
                node=Resource.from_dict(resource),
                search=SearchEntryMode(mode="match", score=None),
            )
            edges.append(edge)

        # Build page info
        has_next = offset + count < total
        has_prev = offset > 0

        page_info = PageInfo(
            hasNextPage=has_next,
            hasPreviousPage=has_prev,
            startCursor=edges[0].cursor if edges else None,
            endCursor=edges[-1].cursor if edges else None,
        )

        return ResourceConnection(
            edges=edges,
            pageInfo=page_info,
            total=total,
        )


class MutationResolver:
    """Resolver for mutation operations.

    Handles mutations like:
        PatientCreate(data: {...}) -> Resource
        PatientUpdate(id: "123", data: {...}) -> Resource
        PatientDelete(id: "123") -> Resource
    """

    def __init__(self, store: Any):
        """Initialize resolver with FHIR store.

        Args:
            store: FHIRStore instance
        """
        self.store = store

    def create(self, resource_type: str, data: dict[str, Any]) -> Resource:
        """Create a new resource.

        Args:
            resource_type: The FHIR resource type
            data: Resource data as dictionary

        Returns:
            Created resource
        """
        # Ensure resourceType is set
        data["resourceType"] = resource_type

        # Create in store
        created = self.store.create(data)

        return Resource.from_dict(created)

    def update(self, resource_type: str, _id: str, data: dict[str, Any]) -> Optional[Resource]:
        """Update an existing resource.

        Args:
            resource_type: The FHIR resource type
            _id: Resource ID to update
            data: Updated resource data

        Returns:
            Updated resource if found, None otherwise
        """
        # Check if resource exists
        existing = self.store.read(resource_type, _id)
        if not existing:
            return None

        # Ensure resourceType and id are set
        data["resourceType"] = resource_type
        data["id"] = _id

        # Update in store
        updated = self.store.update(resource_type, _id, data)

        return Resource.from_dict(updated)

    def delete(self, resource_type: str, _id: str) -> Optional[Resource]:
        """Delete a resource.

        Args:
            resource_type: The FHIR resource type
            _id: Resource ID to delete

        Returns:
            Deleted resource if found, None otherwise
        """
        # Get resource before deletion
        existing = self.store.read(resource_type, _id)
        if not existing:
            return None

        # Delete from store
        self.store.delete(resource_type, _id)

        return Resource.from_dict(existing)
