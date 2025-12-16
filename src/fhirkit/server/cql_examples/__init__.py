"""CQL Examples module for the FHIR Server UI.

This module provides functions to load CQL examples from external files.
Examples are organized by category: beginner, intermediate, advanced.
"""

import json
from pathlib import Path
from typing import TypedDict

# Directory containing this module
EXAMPLES_DIR = Path(__file__).parent


class CQLExample(TypedDict):
    """Type definition for a CQL example."""

    id: str
    name: str
    description: str
    file: str
    category: str
    requires_patient: bool
    code: str


# Cache for loaded examples
_manifest_cache: dict | None = None
_examples_cache: dict[str, CQLExample] = {}


def load_manifest() -> dict:
    """Load the examples manifest.

    Returns:
        The manifest dictionary containing version and examples list.
    """
    global _manifest_cache
    if _manifest_cache is None:
        manifest_path = EXAMPLES_DIR / "manifest.json"
        with open(manifest_path) as f:
            _manifest_cache = json.load(f)
    assert _manifest_cache is not None
    return _manifest_cache


def load_example(example_id: str) -> CQLExample | None:
    """Load a specific CQL example by ID.

    Args:
        example_id: The unique identifier for the example.

    Returns:
        The example dict with code loaded, or None if not found.
    """
    global _examples_cache

    if example_id in _examples_cache:
        return _examples_cache[example_id]

    manifest = load_manifest()
    for example in manifest["examples"]:
        if example["id"] == example_id:
            # Load the CQL code from file
            cql_path = EXAMPLES_DIR / example["file"]
            if cql_path.exists():
                code = cql_path.read_text()
                result: CQLExample = {
                    "id": example["id"],
                    "name": example["name"],
                    "description": example["description"],
                    "file": example["file"],
                    "category": example["category"],
                    "requires_patient": example["requires_patient"],
                    "code": code,
                }
                _examples_cache[example_id] = result
                return result
            break

    return None


def load_all_examples() -> list[CQLExample]:
    """Load all CQL examples with their code.

    Returns:
        List of all examples with code loaded.
    """
    manifest = load_manifest()
    examples = []
    for example in manifest["examples"]:
        loaded = load_example(example["id"])
        if loaded:
            examples.append(loaded)
    return examples


def get_examples_by_category() -> dict[str, list[CQLExample]]:
    """Get examples organized by category.

    Returns:
        Dictionary mapping category names to lists of examples.
    """
    examples = load_all_examples()
    by_category: dict[str, list[CQLExample]] = {
        "beginner": [],
        "intermediate": [],
        "advanced": [],
    }
    for example in examples:
        category = example["category"]
        if category in by_category:
            by_category[category].append(example)
    return by_category


def get_example_ids() -> list[str]:
    """Get list of all example IDs.

    Returns:
        List of example ID strings.
    """
    manifest = load_manifest()
    return [e["id"] for e in manifest["examples"]]


def clear_cache() -> None:
    """Clear the examples cache (useful for testing)."""
    global _manifest_cache, _examples_cache
    _manifest_cache = None
    _examples_cache = {}
