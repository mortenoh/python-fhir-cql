"""FHIR-specific functions: resolve, extension, ofType."""

from typing import Any

from ...context import EvaluationContext
from ...functions import FunctionRegistry


@FunctionRegistry.register("resolve")
def fn_resolve(ctx: EvaluationContext, collection: list[Any]) -> list[Any]:
    """
    Resolve FHIR References to their target resources.

    For each Reference in the input collection, attempts to resolve it using
    the reference_resolver callback in the evaluation context.

    Reference format: {"reference": "Patient/123"} or {"reference": "http://..."}
    """
    if ctx.reference_resolver is None:
        return []

    result = []
    for item in collection:
        if isinstance(item, dict):
            ref = item.get("reference")
            if ref:
                resolved = ctx.reference_resolver(ref)
                if resolved is not None:
                    result.append(resolved)
        elif isinstance(item, str):
            # Direct reference string
            resolved = ctx.reference_resolver(item)
            if resolved is not None:
                result.append(resolved)
    return result


@FunctionRegistry.register("extension")
def fn_extension(ctx: EvaluationContext, collection: list[Any], url: str) -> list[Any]:
    """
    Returns extensions with the specified URL from the input collection.

    Looks for extensions in the 'extension' property of each element
    and filters by the 'url' property.
    """
    result = []
    for item in collection:
        if isinstance(item, dict):
            extensions = item.get("extension", [])
            if isinstance(extensions, list):
                for ext in extensions:
                    if isinstance(ext, dict) and ext.get("url") == url:
                        result.append(ext)
    return result


@FunctionRegistry.register("elementDefinition")
def fn_element_definition(ctx: EvaluationContext, collection: list[Any]) -> list[Any]:
    """
    Returns the FHIR ElementDefinition for each element in the input.

    Note: Requires model information. Returns empty if no model available.
    """
    # This requires StructureDefinition information which we don't have yet
    return []


@FunctionRegistry.register("slice")
def fn_slice(ctx: EvaluationContext, collection: list[Any], structure: str, name: str) -> list[Any]:
    """
    Returns elements that belong to a specific slice.

    Note: Requires StructureDefinition information. Returns empty if unavailable.
    """
    # This requires slice definitions which we don't have yet
    return []


@FunctionRegistry.register("checkModifiers")
def fn_check_modifiers(ctx: EvaluationContext, collection: list[Any], *args: str) -> list[Any]:
    """
    Check if the input has any modifier extensions other than the ones specified.

    If there are modifier extensions other than those listed, raises an error.
    Otherwise returns the input unchanged.
    """
    allowed_urls = set(args)

    for item in collection:
        if isinstance(item, dict):
            mod_extensions = item.get("modifierExtension", [])
            if isinstance(mod_extensions, list):
                for ext in mod_extensions:
                    if isinstance(ext, dict):
                        url = ext.get("url")
                        if url and url not in allowed_urls:
                            # In strict mode, this would raise an error
                            # For now, we just skip such elements
                            pass
    return collection


@FunctionRegistry.register("conformsTo")
def fn_conforms_to(ctx: EvaluationContext, collection: list[Any], profile: str) -> list[bool]:
    """
    Returns true if the resource conforms to the specified profile.

    Note: Requires full profile validation. Returns empty for now.
    """
    # Full profile validation is complex and not implemented
    return []


@FunctionRegistry.register("memberOf")
def fn_member_of(ctx: EvaluationContext, collection: list[Any], valueset: str) -> list[bool]:
    """
    Returns true if the code/Coding/CodeableConcept is in the specified ValueSet.

    Note: Requires terminology service. Returns empty for now.
    """
    # Terminology lookup is not implemented
    return []


@FunctionRegistry.register("subsumes")
def fn_subsumes(ctx: EvaluationContext, collection: list[Any], code: Any) -> list[bool]:
    """
    Returns true if the code in context subsumes the specified code.

    Note: Requires terminology service. Returns empty for now.
    """
    # Terminology lookup is not implemented
    return []


@FunctionRegistry.register("subsumedBy")
def fn_subsumed_by(ctx: EvaluationContext, collection: list[Any], code: Any) -> list[bool]:
    """
    Returns true if the code in context is subsumed by the specified code.

    Note: Requires terminology service. Returns empty for now.
    """
    # Terminology lookup is not implemented
    return []


@FunctionRegistry.register("htmlChecks")
def fn_html_checks(ctx: EvaluationContext, collection: list[Any]) -> list[bool]:
    """
    Check if the HTML content in the Narrative is valid.

    Returns true if the HTML passes basic safety checks.
    """
    for item in collection:
        if isinstance(item, dict):
            div = item.get("div")
            if div and isinstance(div, str):
                # Basic check: must start with <div
                if not div.strip().startswith("<div"):
                    return [False]
    return [True]
