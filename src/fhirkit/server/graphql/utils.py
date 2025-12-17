"""Utility functions for GraphQL operations.

This module provides helper functions for:
- Converting between FHIR and GraphQL parameter naming conventions
- Building search parameters from GraphQL arguments
- Type conversions and validation
"""

from typing import Any


def fhir_param_to_graphql(param_name: str) -> str:
    """Convert a FHIR search parameter name to GraphQL argument name.

    FHIR uses hyphens in parameter names (e.g., 'birth-date'),
    but GraphQL identifiers cannot contain hyphens.

    Args:
        param_name: FHIR search parameter name

    Returns:
        GraphQL-compatible argument name with hyphens replaced by underscores

    Examples:
        >>> fhir_param_to_graphql("birth-date")
        'birth_date'
        >>> fhir_param_to_graphql("general-practitioner")
        'general_practitioner'
        >>> fhir_param_to_graphql("_count")
        '_count'
    """
    return param_name.replace("-", "_")


def graphql_param_to_fhir(param_name: str) -> str:
    """Convert a GraphQL argument name to FHIR search parameter name.

    Reverse of fhir_param_to_graphql - converts underscores back to hyphens,
    but preserves underscore-prefixed special parameters.

    Args:
        param_name: GraphQL argument name

    Returns:
        FHIR search parameter name

    Examples:
        >>> graphql_param_to_fhir("birth_date")
        'birth-date'
        >>> graphql_param_to_fhir("_count")
        '_count'
        >>> graphql_param_to_fhir("general_practitioner")
        'general-practitioner'
    """
    # Special parameters starting with underscore are not converted
    if param_name.startswith("_"):
        return param_name

    return param_name.replace("_", "-")


def build_search_params(graphql_args: dict[str, Any]) -> dict[str, str]:
    """Build FHIR search parameters from GraphQL arguments.

    Converts GraphQL argument names to FHIR parameter names and
    filters out None values.

    Args:
        graphql_args: Dictionary of GraphQL arguments

    Returns:
        Dictionary of FHIR search parameters (non-None values only)

    Example:
        >>> build_search_params({"name": "Smith", "gender": "male", "birthDate": None})
        {"name": "Smith", "gender": "male"}
    """
    result = {}
    for key, value in graphql_args.items():
        if value is not None:
            fhir_key = graphql_param_to_fhir(key)
            result[fhir_key] = str(value)
    return result


def get_search_param_type_map() -> dict[str, type]:
    """Get mapping of FHIR search parameter types to Python types.

    Returns:
        Dictionary mapping FHIR param types to Python types
    """
    return {
        "token": str,
        "string": str,
        "reference": str,
        "date": str,
        "uri": str,
        "quantity": str,
        "number": str,
        "composite": str,
        "special": str,
    }


def sanitize_resource_type_name(name: str) -> str:
    """Sanitize a resource type name for use as a GraphQL type/field name.

    Ensures the name is a valid GraphQL identifier.

    Args:
        name: Resource type name

    Returns:
        Sanitized name safe for GraphQL

    Example:
        >>> sanitize_resource_type_name("Patient")
        'Patient'
        >>> sanitize_resource_type_name("My-Resource")
        'My_Resource'
    """
    # Replace hyphens with underscores
    sanitized = name.replace("-", "_")

    # Ensure it starts with a letter or underscore
    if sanitized and not sanitized[0].isalpha() and sanitized[0] != "_":
        sanitized = "_" + sanitized

    return sanitized


def format_graphql_description(resource_type: str, operation: str) -> str:
    """Generate a description for a GraphQL field.

    Args:
        resource_type: The FHIR resource type
        operation: The operation type (e.g., 'read', 'list', 'create')

    Returns:
        Human-readable description string
    """
    descriptions = {
        "read": f"Fetch a single {resource_type} resource by ID",
        "list": f"Search for {resource_type} resources with optional filters",
        "connection": f"Search {resource_type} resources with cursor-based pagination",
        "create": f"Create a new {resource_type} resource",
        "update": f"Update an existing {resource_type} resource",
        "delete": f"Delete a {resource_type} resource",
    }
    return descriptions.get(operation, f"{operation} {resource_type}")


def extract_reference_parts(reference: str) -> tuple[str | None, str | None]:
    """Extract resource type and ID from a FHIR reference string.

    Args:
        reference: FHIR reference string (e.g., "Patient/123")

    Returns:
        Tuple of (resource_type, resource_id), either may be None

    Examples:
        >>> extract_reference_parts("Patient/123")
        ('Patient', '123')
        >>> extract_reference_parts("123")
        (None, '123')
        >>> extract_reference_parts("")
        (None, None)
    """
    if not reference:
        return None, None

    if "/" in reference:
        parts = reference.split("/", 1)
        return parts[0], parts[1]

    return None, reference
