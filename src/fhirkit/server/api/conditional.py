"""Conditional request utilities for FHIR server.

Implements HTTP conditional request handling per RFC 7232:
- If-None-Match: Compare ETags for caching
- If-Modified-Since: Compare timestamps for caching
- If-Match: Compare ETags for updates (optimistic locking)
"""

import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def parse_etag(etag: str) -> str:
    """Extract version from ETag value.

    ETags can be weak (W/"version") or strong ("version").
    FHIR uses weak ETags.

    Args:
        etag: ETag value like W/"2" or "2"

    Returns:
        The version string without quotes or W/ prefix
    """
    etag = etag.strip()
    # Remove weak indicator
    if etag.startswith("W/"):
        etag = etag[2:]
    # Remove quotes
    if etag.startswith('"') and etag.endswith('"'):
        etag = etag[1:-1]
    return etag


def parse_if_none_match(header: str) -> list[str]:
    """Parse If-None-Match header value.

    Args:
        header: Header value, can be:
            - Single ETag: W/"2"
            - Multiple ETags: W/"1", W/"2"
            - Wildcard: *

    Returns:
        List of version strings, or ["*"] for wildcard
    """
    header = header.strip()

    # Handle wildcard
    if header == "*":
        return ["*"]

    # Parse comma-separated ETags
    etags = []
    # Match ETag pattern: optional W/ followed by quoted string
    pattern = r'(W/)?"([^"]*)"'
    for match in re.finditer(pattern, header):
        etags.append(match.group(2))

    return etags


def parse_if_modified_since(header: str) -> datetime | None:
    """Parse If-Modified-Since header value.

    Args:
        header: HTTP-date format string, e.g.:
            - "Tue, 15 Nov 2024 12:30:45 GMT"

    Returns:
        datetime object with timezone, or None if parse fails
    """
    try:
        return parsedate_to_datetime(header)
    except (ValueError, TypeError):
        return None


def etag_matches(resource_version: str, if_none_match_values: list[str]) -> bool:
    """Check if resource version matches any If-None-Match value.

    Args:
        resource_version: Current resource versionId
        if_none_match_values: List of versions from If-None-Match header

    Returns:
        True if resource version matches (client should get 304)
    """
    if "*" in if_none_match_values:
        return True
    return resource_version in if_none_match_values


def parse_last_updated(last_updated: str) -> datetime | None:
    """Parse resource meta.lastUpdated to datetime.

    Args:
        last_updated: ISO 8601 datetime string

    Returns:
        datetime object with timezone, or None if parse fails
    """
    try:
        # Handle various ISO 8601 formats
        if last_updated.endswith("Z"):
            last_updated = last_updated[:-1] + "+00:00"
        return datetime.fromisoformat(last_updated)
    except (ValueError, TypeError):
        return None


def is_modified_since(last_updated: str, if_modified_since: datetime) -> bool:
    """Check if resource was modified since given datetime.

    Args:
        last_updated: Resource's meta.lastUpdated ISO 8601 string
        if_modified_since: Datetime from If-Modified-Since header

    Returns:
        True if resource was modified after if_modified_since
        (i.e., client should get full response, not 304)
    """
    resource_dt = parse_last_updated(last_updated)
    if resource_dt is None:
        # Can't determine, assume modified
        return True

    # Ensure both have timezone info for comparison
    if if_modified_since.tzinfo is None:
        if_modified_since = if_modified_since.replace(tzinfo=timezone.utc)
    if resource_dt.tzinfo is None:
        resource_dt = resource_dt.replace(tzinfo=timezone.utc)

    return resource_dt > if_modified_since


def check_conditional_read(
    resource: dict,
    if_none_match: str | None,
    if_modified_since: str | None,
) -> bool:
    """Check if conditional read should return 304 Not Modified.

    Per RFC 7232, If-None-Match takes precedence over If-Modified-Since.

    Args:
        resource: The FHIR resource with meta.versionId and meta.lastUpdated
        if_none_match: If-None-Match header value or None
        if_modified_since: If-Modified-Since header value or None

    Returns:
        True if should return 304 Not Modified
    """
    meta = resource.get("meta", {})

    # Check If-None-Match first (takes precedence)
    if if_none_match:
        etags = parse_if_none_match(if_none_match)
        version = meta.get("versionId", "1")
        if etag_matches(version, etags):
            return True

    # Check If-Modified-Since
    if if_modified_since and not if_none_match:
        parsed_date = parse_if_modified_since(if_modified_since)
        if parsed_date:
            last_updated = meta.get("lastUpdated")
            if last_updated and not is_modified_since(last_updated, parsed_date):
                return True

    return False
