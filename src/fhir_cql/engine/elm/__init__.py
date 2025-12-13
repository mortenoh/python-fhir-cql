"""ELM (Expression Logical Model) support for CQL.

This module provides bidirectional ELM support:
- Parse and execute ELM JSON from external CQL compilers
- Export CQL libraries to ELM JSON format
"""

from fhir_cql.engine.elm.evaluator import ELMEvaluator
from fhir_cql.engine.elm.exceptions import ELMError, ELMExecutionError, ELMValidationError
from fhir_cql.engine.elm.loader import ELMLoader
from fhir_cql.engine.elm.models import ELMLibrary
from fhir_cql.engine.elm.visitor import ELMExpressionVisitor

__all__ = [
    "ELMEvaluator",
    "ELMLoader",
    "ELMLibrary",
    "ELMExpressionVisitor",
    "ELMError",
    "ELMValidationError",
    "ELMExecutionError",
]
