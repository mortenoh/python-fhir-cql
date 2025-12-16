"""Built-in CQL libraries.

This module provides built-in libraries like FHIRHelpers that are
automatically available without requiring user configuration.
"""

from pathlib import Path

from ..library_resolver import InMemoryLibraryResolver


def get_builtin_resolver() -> InMemoryLibraryResolver:
    """Create a resolver for built-in libraries.

    Returns:
        InMemoryLibraryResolver with FHIRHelpers and other built-in libraries loaded.
    """
    resolver = InMemoryLibraryResolver()
    builtin_dir = Path(__file__).parent

    # Load FHIRHelpers
    fhirhelpers_path = builtin_dir / "FHIRHelpers.cql"
    if fhirhelpers_path.exists():
        fhirhelpers_source = fhirhelpers_path.read_text(encoding="utf-8")
        resolver.add_library("FHIRHelpers", fhirhelpers_source, "4.0.1")

    return resolver


__all__ = ["get_builtin_resolver"]
