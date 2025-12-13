"""CQL (Clinical Quality Language) evaluation engine.

This module provides comprehensive CQL evaluation capabilities including:
- Library parsing and compilation
- Expression evaluation
- Support for CQL types (Code, Interval, Tuple, etc.)
- Query execution
- Retrieve operations (with data source integration)

Basic Usage:
    from fhir_cql.engine.cql import CQLEvaluator, evaluate

    # Quick expression evaluation
    result = evaluate("1 + 2 * 3")  # Returns 7

    # Full library compilation and evaluation
    evaluator = CQLEvaluator()
    library = evaluator.compile('''
        library Example version '1.0'
        using FHIR version '4.0.1'

        define Sum: 1 + 2 + 3
        define IsAdult: AgeInYears() >= 18
    ''')

    # Evaluate specific definition
    result = evaluator.evaluate_definition("Sum")  # Returns 6

    # Evaluate with patient context
    patient = {"resourceType": "Patient", "birthDate": "1990-01-01"}
    result = evaluator.evaluate_definition("IsAdult", resource=patient)
"""

from .context import CQLContext, DataSource, EncounterContext, PatientContext, UnfilteredContext
from .datasource import BundleDataSource, FHIRDataSource, InMemoryDataSource, PatientBundleDataSource
from .evaluator import CQLEvaluator, compile_library, evaluate
from .library import (
    CodeDefinition,
    CodeSystemDefinition,
    ConceptDefinition,
    CQLLibrary,
    ExpressionDefinition,
    FunctionDefinition,
    IncludeDefinition,
    LibraryManager,
    ParameterDefinition,
    UsingDefinition,
    ValueSetDefinition,
)
from .measure import (
    GroupResult,
    MeasureEvaluator,
    MeasureGroup,
    MeasurePopulation,
    MeasureReport,
    MeasureScoring,
    PatientResult,
    PopulationCount,
    PopulationType,
    StratifierResult,
)
from .types import (
    CQLBoolean,
    CQLCode,
    CQLConcept,
    CQLDate,
    CQLDateTime,
    CQLDecimal,
    CQLInteger,
    CQLInterval,
    CQLList,
    CQLQuantity,
    CQLRatio,
    CQLString,
    CQLTuple,
    cql_type_name,
    is_cql_type,
)
from .visitor import CQLEvaluatorVisitor

__all__ = [
    # Main evaluator
    "CQLEvaluator",
    "CQLEvaluatorVisitor",
    "compile_library",
    "evaluate",
    # Context
    "CQLContext",
    "PatientContext",
    "UnfilteredContext",
    "EncounterContext",
    "DataSource",
    # Data Sources
    "FHIRDataSource",
    "InMemoryDataSource",
    "BundleDataSource",
    "PatientBundleDataSource",
    # Library management
    "CQLLibrary",
    "LibraryManager",
    "UsingDefinition",
    "IncludeDefinition",
    "ParameterDefinition",
    "CodeSystemDefinition",
    "ValueSetDefinition",
    "CodeDefinition",
    "ConceptDefinition",
    "ExpressionDefinition",
    "FunctionDefinition",
    # Types
    "CQLCode",
    "CQLConcept",
    "CQLInterval",
    "CQLTuple",
    "CQLRatio",
    # Type aliases
    "CQLBoolean",
    "CQLInteger",
    "CQLDecimal",
    "CQLString",
    "CQLDate",
    "CQLDateTime",
    "CQLQuantity",
    "CQLList",
    # Type utilities
    "is_cql_type",
    "cql_type_name",
    # Measure evaluation
    "MeasureEvaluator",
    "MeasureReport",
    "MeasureGroup",
    "MeasurePopulation",
    "MeasureScoring",
    "PopulationType",
    "PopulationCount",
    "PatientResult",
    "GroupResult",
    "StratifierResult",
]
