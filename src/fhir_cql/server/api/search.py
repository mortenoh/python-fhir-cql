"""FHIR search parameter handling."""

from datetime import date, datetime
from typing import Any
from urllib.parse import parse_qs

# Search parameter definitions by resource type
SEARCH_PARAMS: dict[str, dict[str, dict[str, Any]]] = {
    "Patient": {
        "_id": {"path": "id", "type": "token"},
        "identifier": {"path": "identifier", "type": "token"},
        "name": {"path": "name", "type": "string", "search_name": True},
        "family": {"path": "name.family", "type": "string"},
        "given": {"path": "name.given", "type": "string"},
        "gender": {"path": "gender", "type": "token"},
        "birthdate": {"path": "birthDate", "type": "date"},
        "address": {"path": "address", "type": "string", "search_address": True},
        "address-city": {"path": "address.city", "type": "string"},
        "address-state": {"path": "address.state", "type": "string"},
        "address-postalcode": {"path": "address.postalCode", "type": "string"},
        "telecom": {"path": "telecom.value", "type": "token"},
        "active": {"path": "active", "type": "token"},
    },
    "Condition": {
        "_id": {"path": "id", "type": "token"},
        "patient": {"path": "subject.reference", "type": "reference"},
        "subject": {"path": "subject.reference", "type": "reference"},
        "code": {"path": "code.coding", "type": "token"},
        "clinical-status": {"path": "clinicalStatus.coding", "type": "token"},
        "verification-status": {"path": "verificationStatus.coding", "type": "token"},
        "category": {"path": "category.coding", "type": "token"},
        "onset-date": {"path": "onsetDateTime", "type": "date"},
        "severity": {"path": "severity.coding", "type": "token"},
    },
    "Observation": {
        "_id": {"path": "id", "type": "token"},
        "patient": {"path": "subject.reference", "type": "reference"},
        "subject": {"path": "subject.reference", "type": "reference"},
        "code": {"path": "code.coding", "type": "token"},
        "category": {"path": "category.coding", "type": "token"},
        "status": {"path": "status", "type": "token"},
        "date": {"path": "effectiveDateTime", "type": "date"},
        "value-quantity": {"path": "valueQuantity.value", "type": "quantity"},
        "encounter": {"path": "encounter.reference", "type": "reference"},
    },
    "MedicationRequest": {
        "_id": {"path": "id", "type": "token"},
        "patient": {"path": "subject.reference", "type": "reference"},
        "subject": {"path": "subject.reference", "type": "reference"},
        "code": {"path": "medicationCodeableConcept.coding", "type": "token"},
        "status": {"path": "status", "type": "token"},
        "intent": {"path": "intent", "type": "token"},
        "authoredon": {"path": "authoredOn", "type": "date"},
        "requester": {"path": "requester.reference", "type": "reference"},
        "encounter": {"path": "encounter.reference", "type": "reference"},
    },
    "Encounter": {
        "_id": {"path": "id", "type": "token"},
        "patient": {"path": "subject.reference", "type": "reference"},
        "subject": {"path": "subject.reference", "type": "reference"},
        "status": {"path": "status", "type": "token"},
        "class": {"path": "class.code", "type": "token"},
        "type": {"path": "type.coding", "type": "token"},
        "date": {"path": "period.start", "type": "date"},
        "participant": {"path": "participant.individual.reference", "type": "reference"},
        "service-provider": {"path": "serviceProvider.reference", "type": "reference"},
    },
    "Procedure": {
        "_id": {"path": "id", "type": "token"},
        "patient": {"path": "subject.reference", "type": "reference"},
        "subject": {"path": "subject.reference", "type": "reference"},
        "code": {"path": "code.coding", "type": "token"},
        "status": {"path": "status", "type": "token"},
        "date": {"path": "performedDateTime", "type": "date"},
        "category": {"path": "category.coding", "type": "token"},
        "performer": {"path": "performer.actor.reference", "type": "reference"},
        "encounter": {"path": "encounter.reference", "type": "reference"},
    },
    "Practitioner": {
        "_id": {"path": "id", "type": "token"},
        "identifier": {"path": "identifier", "type": "token"},
        "name": {"path": "name", "type": "string", "search_name": True},
        "family": {"path": "name.family", "type": "string"},
        "given": {"path": "name.given", "type": "string"},
        "active": {"path": "active", "type": "token"},
    },
    "Organization": {
        "_id": {"path": "id", "type": "token"},
        "identifier": {"path": "identifier", "type": "token"},
        "name": {"path": "name", "type": "string"},
        "active": {"path": "active", "type": "token"},
        "type": {"path": "type.coding", "type": "token"},
        "address": {"path": "address", "type": "string", "search_address": True},
        "address-city": {"path": "address.city", "type": "string"},
        "address-state": {"path": "address.state", "type": "string"},
    },
    "ValueSet": {
        "_id": {"path": "id", "type": "token"},
        "url": {"path": "url", "type": "uri"},
        "name": {"path": "name", "type": "string"},
        "title": {"path": "title", "type": "string"},
        "status": {"path": "status", "type": "token"},
        "version": {"path": "version", "type": "token"},
    },
    "CodeSystem": {
        "_id": {"path": "id", "type": "token"},
        "url": {"path": "url", "type": "uri"},
        "name": {"path": "name", "type": "string"},
        "title": {"path": "title", "type": "string"},
        "status": {"path": "status", "type": "token"},
        "version": {"path": "version", "type": "token"},
    },
    "Library": {
        "_id": {"path": "id", "type": "token"},
        "url": {"path": "url", "type": "uri"},
        "name": {"path": "name", "type": "string"},
        "title": {"path": "title", "type": "string"},
        "status": {"path": "status", "type": "token"},
        "version": {"path": "version", "type": "token"},
        "type": {"path": "type.coding", "type": "token"},
    },
}


def get_nested_value(resource: dict[str, Any], path: str) -> Any:
    """Get a value from a nested path in a resource.

    Args:
        resource: The FHIR resource
        path: Dot-separated path (e.g., "subject.reference")

    Returns:
        The value at the path, or None if not found
    """
    parts = path.split(".")
    current: Any = resource

    for part in parts:
        if current is None:
            return None
        if isinstance(current, list):
            # For lists, collect all values at this path
            values = []
            for item in current:
                if isinstance(item, dict) and part in item:
                    values.append(item[part])
            return values if values else None
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None

    return current


def match_token(resource_value: Any, search_value: str) -> bool:
    """Match a token search parameter.

    Token format: [system|]code or |code (no system) or system| (any code)

    Args:
        resource_value: Value from the resource
        search_value: Search parameter value

    Returns:
        True if matches
    """
    if resource_value is None:
        return False

    # Parse search value
    if "|" in search_value:
        system, code = search_value.split("|", 1)
    else:
        system, code = None, search_value

    # Handle different value types
    if isinstance(resource_value, str):
        # Simple string match (e.g., status field)
        return code.lower() == resource_value.lower() if code else True

    if isinstance(resource_value, bool):
        return code.lower() in ("true", "1") if resource_value else code.lower() in ("false", "0")

    if isinstance(resource_value, list):
        # List of codings or identifiers
        for item in resource_value:
            if match_token(item, search_value):
                return True
        return False

    if isinstance(resource_value, dict):
        # Coding or Identifier
        if "coding" in resource_value:
            # CodeableConcept - check each coding
            return match_token(resource_value["coding"], search_value)

        item_system = resource_value.get("system", "")
        item_code = resource_value.get("code") or resource_value.get("value", "")

        if system and code:
            return system == item_system and code.lower() == str(item_code).lower()
        if system and not code:
            return system == item_system
        if code:
            return code.lower() == str(item_code).lower()

    return False


def match_string(resource_value: Any, search_value: str) -> bool:
    """Match a string search parameter (case-insensitive, starts-with).

    Args:
        resource_value: Value from the resource
        search_value: Search parameter value

    Returns:
        True if matches
    """
    if resource_value is None:
        return False

    search_lower = search_value.lower()

    if isinstance(resource_value, str):
        return resource_value.lower().startswith(search_lower)

    if isinstance(resource_value, list):
        for item in resource_value:
            if match_string(item, search_value):
                return True
        return False

    if isinstance(resource_value, dict):
        # For HumanName, search across all text fields
        for key in ["text", "family", "given", "prefix", "suffix"]:
            if key in resource_value:
                if match_string(resource_value[key], search_value):
                    return True
        # For Address
        for key in ["text", "line", "city", "state", "postalCode", "country"]:
            if key in resource_value:
                if match_string(resource_value[key], search_value):
                    return True
        return False

    return False


def match_reference(resource_value: Any, search_value: str) -> bool:
    """Match a reference search parameter.

    Reference format: [Type/]id or full URL

    Args:
        resource_value: Value from the resource (e.g., "Patient/123")
        search_value: Search parameter value

    Returns:
        True if matches
    """
    if resource_value is None:
        return False

    if isinstance(resource_value, str):
        # Normalize both to just the reference part
        if "/" in search_value:
            return resource_value == search_value or resource_value.endswith(f"/{search_value}")
        # Search by ID only
        return resource_value.endswith(f"/{search_value}")

    if isinstance(resource_value, list):
        for item in resource_value:
            if match_reference(item, search_value):
                return True
        return False

    return False


def match_date(resource_value: Any, search_value: str) -> bool:
    """Match a date search parameter.

    Date format: [prefix]YYYY[-MM[-DD[Thh:mm:ss[Z]]]]
    Prefixes: eq, ne, gt, lt, ge, le, sa, eb, ap

    Args:
        resource_value: Value from the resource (ISO date string)
        search_value: Search parameter value

    Returns:
        True if matches
    """
    if resource_value is None:
        return False

    # Parse prefix
    prefixes = ["eq", "ne", "gt", "lt", "ge", "le", "sa", "eb", "ap"]
    prefix = "eq"
    date_str = search_value

    for p in prefixes:
        if search_value.startswith(p):
            prefix = p
            date_str = search_value[len(p) :]
            break

    # Parse resource date
    try:
        if "T" in str(resource_value):
            resource_dt = datetime.fromisoformat(str(resource_value).replace("Z", "+00:00"))
            resource_date = resource_dt.date()
        else:
            resource_date = date.fromisoformat(str(resource_value)[:10])
    except (ValueError, TypeError):
        return False

    # Parse search date
    try:
        search_date = date.fromisoformat(date_str[:10])
    except (ValueError, TypeError):
        return False

    # Apply prefix comparison
    if prefix == "eq":
        return resource_date == search_date
    if prefix == "ne":
        return resource_date != search_date
    if prefix == "gt" or prefix == "sa":
        return resource_date > search_date
    if prefix == "lt" or prefix == "eb":
        return resource_date < search_date
    if prefix == "ge":
        return resource_date >= search_date
    if prefix == "le":
        return resource_date <= search_date
    if prefix == "ap":
        # Approximate - within a reasonable range (let's say 7 days)

        return abs((resource_date - search_date).days) <= 7

    return False


def match_uri(resource_value: Any, search_value: str) -> bool:
    """Match a URI search parameter (exact match).

    Args:
        resource_value: Value from the resource
        search_value: Search parameter value

    Returns:
        True if matches
    """
    if resource_value is None:
        return False

    if isinstance(resource_value, str):
        return resource_value == search_value

    return False


def matches_search_param(
    resource: dict[str, Any],
    param_name: str,
    param_value: str,
    param_def: dict[str, Any],
) -> bool:
    """Check if a resource matches a single search parameter.

    Args:
        resource: The FHIR resource
        param_name: Name of the search parameter
        param_value: Value to search for
        param_def: Parameter definition from SEARCH_PARAMS

    Returns:
        True if the resource matches
    """
    path = param_def["path"]
    param_type = param_def["type"]

    # Handle special search flags
    if param_def.get("search_name"):
        # Search across all name parts
        names = resource.get("name", [])
        if isinstance(names, dict):
            names = [names]
        for name in names:
            if match_string(name, param_value):
                return True
        return False

    if param_def.get("search_address"):
        # Search across all address parts
        addresses = resource.get("address", [])
        if isinstance(addresses, dict):
            addresses = [addresses]
        for addr in addresses:
            if match_string(addr, param_value):
                return True
        return False

    # Get value from resource
    value = get_nested_value(resource, path)

    # Match based on type
    if param_type == "token":
        return match_token(value, param_value)
    if param_type == "string":
        return match_string(value, param_value)
    if param_type == "reference":
        return match_reference(value, param_value)
    if param_type == "date":
        return match_date(value, param_value)
    if param_type == "uri":
        return match_uri(value, param_value)
    if param_type == "quantity":
        # Simple quantity comparison
        try:
            search_val = float(param_value)
            return value is not None and float(value) == search_val
        except (ValueError, TypeError):
            return False

    return False


def filter_resources(
    resources: list[dict[str, Any]],
    resource_type: str,
    params: dict[str, str | list[str]],
) -> list[dict[str, Any]]:
    """Filter resources based on search parameters.

    Args:
        resources: List of FHIR resources
        resource_type: The resource type
        params: Search parameters

    Returns:
        Filtered list of resources
    """
    if not params:
        return resources

    # Get search param definitions for this type
    type_params = SEARCH_PARAMS.get(resource_type, {})

    # Add common params
    common_params = {
        "_id": {"path": "id", "type": "token"},
        "_lastUpdated": {"path": "meta.lastUpdated", "type": "date"},
    }
    type_params = {**common_params, **type_params}

    filtered = resources

    for param_name, param_values in params.items():
        # Skip special parameters handled elsewhere
        if param_name.startswith("_") and param_name not in ("_id", "_lastUpdated"):
            continue

        # Get param definition
        param_def = type_params.get(param_name)
        if param_def is None:
            # Unknown parameter - skip (could also raise error)
            continue

        # Ensure values is a list
        if isinstance(param_values, str):
            param_values = [param_values]

        # Filter: resource must match at least one value (OR within param)
        filtered = [r for r in filtered if any(matches_search_param(r, param_name, v, param_def) for v in param_values)]

    return filtered


def parse_search_params(query_string: str) -> dict[str, list[str]]:
    """Parse a query string into search parameters.

    Args:
        query_string: URL query string

    Returns:
        Dict of parameter name to list of values
    """
    return parse_qs(query_string)
