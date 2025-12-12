"""Collection functions."""

from typing import Any

from ...context import EvaluationContext
from ...functions import FunctionRegistry


@FunctionRegistry.register("distinct")
def fn_distinct(ctx: EvaluationContext, collection: list[Any]) -> list[Any]:
    """Returns collection with duplicates removed."""
    seen: list[Any] = []
    for item in collection:
        # Use custom equality check for complex types
        found = False
        for s in seen:
            if _deep_equals(item, s):
                found = True
                break
        if not found:
            seen.append(item)
    return seen


@FunctionRegistry.register("isDistinct")
def fn_is_distinct(ctx: EvaluationContext, collection: list[Any]) -> list[bool]:
    """Returns true if all elements in collection are distinct."""
    distinct = fn_distinct(ctx, collection)
    return [len(distinct) == len(collection)]


@FunctionRegistry.register("union")
def fn_union(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[Any]:
    """Returns union of two collections (with duplicates removed)."""
    combined = left + right
    return fn_distinct(ctx, combined)


@FunctionRegistry.register("intersect")
def fn_intersect(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[Any]:
    """Returns intersection of two collections."""
    result = []
    for item in left:
        for r_item in right:
            if _deep_equals(item, r_item):
                result.append(item)
                break
    return fn_distinct(ctx, result)


@FunctionRegistry.register("exclude")
def fn_exclude(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[Any]:
    """Returns elements in left that are not in right."""
    result = []
    for item in left:
        found = False
        for r_item in right:
            if _deep_equals(item, r_item):
                found = True
                break
        if not found:
            result.append(item)
    return result


@FunctionRegistry.register("combine")
def fn_combine(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[Any]:
    """Combines two collections (preserves duplicates)."""
    return left + right


@FunctionRegistry.register("flatten")
def fn_flatten(ctx: EvaluationContext, collection: list[Any]) -> list[Any]:
    """Flattens nested collections one level."""
    result = []
    for item in collection:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


@FunctionRegistry.register("subsetOf")
def fn_subset_of(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Returns true if left is a subset of right."""
    for item in left:
        found = False
        for r_item in right:
            if _deep_equals(item, r_item):
                found = True
                break
        if not found:
            return [False]
    return [True]


@FunctionRegistry.register("supersetOf")
def fn_superset_of(ctx: EvaluationContext, left: list[Any], right: list[Any]) -> list[bool]:
    """Returns true if left is a superset of right."""
    return fn_subset_of(ctx, right, left)


def _deep_equals(a: Any, b: Any) -> bool:
    """Deep equality check for FHIRPath values."""
    if type(a) is not type(b):
        # Special case for int/float comparison
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a == b
        return False

    if isinstance(a, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(_deep_equals(a[k], b[k]) for k in a.keys())

    if isinstance(a, list):
        if len(a) != len(b):
            return False
        return all(_deep_equals(a[i], b[i]) for i in range(len(a)))

    return a == b
