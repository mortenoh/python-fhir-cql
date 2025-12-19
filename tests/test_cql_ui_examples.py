"""Tests for CQL UI examples.

These tests verify that each externalized CQL example:
1. Parses without errors
2. Evaluates without runtime errors
3. Returns expected result types for basic operations
"""

import pytest

from fhirkit.engine.cql import CQLEvaluator, InMemoryDataSource
from fhirkit.server.cql_examples import (
    CQLExample,
    get_example_ids,
    get_examples_by_category,
    load_all_examples,
    load_example,
    load_manifest,
)
from fhirkit.server.generator import PatientRecordGenerator


class TestExamplesLoader:
    """Test the examples loader module."""

    def test_load_manifest(self) -> None:
        """Manifest should load with version and examples."""
        manifest = load_manifest()
        assert "version" in manifest
        assert "examples" in manifest
        assert len(manifest["examples"]) == 29  # 6 + 9 + 14 examples

    def test_load_example(self) -> None:
        """Should load a specific example by ID."""
        example = load_example("basic-arithmetic")
        assert example is not None
        assert example["id"] == "basic-arithmetic"
        assert "code" in example
        assert "library ArithmeticExamples" in example["code"]

    def test_load_nonexistent_example(self) -> None:
        """Should return None for nonexistent example."""
        example = load_example("nonexistent-example")
        assert example is None

    def test_load_all_examples(self) -> None:
        """Should load all examples with code."""
        examples = load_all_examples()
        assert len(examples) == 29
        for ex in examples:
            assert "code" in ex
            assert len(ex["code"]) > 0

    def test_get_examples_by_category(self) -> None:
        """Should organize examples by category."""
        by_cat = get_examples_by_category()
        assert len(by_cat["beginner"]) == 6
        assert len(by_cat["intermediate"]) == 9
        assert len(by_cat["advanced"]) == 14

    def test_get_example_ids(self) -> None:
        """Should return list of all example IDs."""
        ids = get_example_ids()
        assert len(ids) == 29
        assert "basic-arithmetic" in ids
        assert "adv-queries" in ids


# Load all examples for parameterization
ALL_EXAMPLES = load_all_examples()
BEGINNER_EXAMPLES = [e for e in ALL_EXAMPLES if e["category"] == "beginner"]
PATIENT_EXAMPLES = [e for e in ALL_EXAMPLES if e["requires_patient"]]


class TestCQLExampleParsing:
    """Test that all examples parse correctly."""

    @pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda e: e["id"])
    def test_example_parses(self, example: CQLExample) -> None:
        """Each example should parse without errors."""
        evaluator = CQLEvaluator()
        # This should not raise any exception
        evaluator.compile(example["code"])


class TestBeginnerExamplesNoPatient:
    """Test beginner examples that don't require patient context."""

    @pytest.fixture
    def evaluator(self) -> CQLEvaluator:
        return CQLEvaluator()

    @pytest.mark.parametrize("example", BEGINNER_EXAMPLES, ids=lambda e: e["id"])
    def test_beginner_example_evaluates(self, evaluator: CQLEvaluator, example: CQLExample) -> None:
        """Beginner examples should evaluate without patient context."""
        assert not example["requires_patient"]
        library = evaluator.compile(example["code"])

        # Get all definitions and evaluate each
        for def_name in library.definitions:
            # Should not raise - result can be any type
            evaluator.evaluate_definition(def_name, library=library)


class TestPatientContextExamples:
    """Test examples that require patient context."""

    @pytest.fixture
    def generator(self) -> PatientRecordGenerator:
        return PatientRecordGenerator(seed=42)

    @pytest.fixture
    def patient_resources(self, generator: PatientRecordGenerator) -> list[dict]:
        """Generate patient with diverse data for testing."""
        return generator.generate_patient_record(
            num_conditions=(5, 8),
            num_encounters=(3, 5),
            num_observations_per_encounter=(5, 8),
            num_medications=(4, 6),
            num_procedures=(2, 4),
            num_allergies=(2, 4),
            num_immunizations=(3, 5),
        )

    @pytest.fixture
    def data_source(self, patient_resources: list[dict]) -> InMemoryDataSource:
        ds = InMemoryDataSource()
        for resource in patient_resources:
            ds.add_resource(resource)
        return ds

    @pytest.fixture
    def patient(self, patient_resources: list[dict]) -> dict:
        return next(r for r in patient_resources if r["resourceType"] == "Patient")

    @pytest.mark.parametrize("example", PATIENT_EXAMPLES, ids=lambda e: e["id"])
    def test_patient_example_evaluates(
        self,
        data_source: InMemoryDataSource,
        patient: dict,
        example: CQLExample,
    ) -> None:
        """Patient examples should evaluate with generated data."""
        evaluator = CQLEvaluator(data_source=data_source)
        library = evaluator.compile(example["code"])

        # Evaluate at least one definition - null results are acceptable
        definitions = list(library.definitions.keys())
        if definitions:
            # Should not raise
            evaluator.evaluate_definition(definitions[0], resource=patient, library=library)


class TestSpecificExampleResults:
    """Test specific examples with expected results."""

    def test_basic_arithmetic_addition(self) -> None:
        """Test arithmetic Addition returns 8."""
        example = load_example("basic-arithmetic")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("Addition", library=library)
        assert result == 8

    def test_basic_arithmetic_multiplication(self) -> None:
        """Test arithmetic Multiplication returns 42."""
        example = load_example("basic-arithmetic")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("Multiplication", library=library)
        assert result == 42

    def test_basic_strings_length(self) -> None:
        """Test string Length returns 5."""
        example = load_example("basic-strings")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("Length", library=library)
        assert result == 5

    def test_basic_strings_upper_case(self) -> None:
        """Test string Upper Case returns 'HELLO'."""
        example = load_example("basic-strings")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("Upper Case", library=library)
        assert result == "HELLO"

    def test_basic_lists_count(self) -> None:
        """Test list Count returns 5."""
        example = load_example("basic-lists")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("Count", library=library)
        assert result == 5

    def test_basic_lists_first(self) -> None:
        """Test list First returns 1."""
        example = load_example("basic-lists")
        assert example is not None
        evaluator = CQLEvaluator()
        library = evaluator.compile(example["code"])
        result = evaluator.evaluate_definition("First", library=library)
        assert result == 1


class TestExamplesWithGeneratedData:
    """Integration tests with generator-produced data."""

    @pytest.fixture
    def generator(self) -> PatientRecordGenerator:
        return PatientRecordGenerator(seed=42)

    @pytest.fixture
    def patient_resources(self, generator: PatientRecordGenerator) -> list[dict]:
        return generator.generate_patient_record(
            num_conditions=(3, 5),
            num_encounters=(2, 4),
            num_observations_per_encounter=(3, 5),
            num_medications=(2, 4),
        )

    @pytest.fixture
    def data_source(self, patient_resources: list[dict]) -> InMemoryDataSource:
        ds = InMemoryDataSource()
        for resource in patient_resources:
            ds.add_resource(resource)
        return ds

    @pytest.fixture
    def patient(self, patient_resources: list[dict]) -> dict:
        return next(r for r in patient_resources if r["resourceType"] == "Patient")

    def test_patient_age_example(self, data_source: InMemoryDataSource, patient: dict) -> None:
        """Patient age example should return age values."""
        example = load_example("patient-age")
        assert example is not None
        evaluator = CQLEvaluator(data_source=data_source)
        library = evaluator.compile(example["code"])

        age = evaluator.evaluate_definition("Age In Years", resource=patient, library=library)
        assert age is not None
        assert isinstance(age, int)
        assert 0 <= age <= 120

    def test_active_conditions_example(
        self, data_source: InMemoryDataSource, patient: dict, patient_resources: list[dict]
    ) -> None:
        """Active conditions example should find conditions."""
        example = load_example("cond-active")
        assert example is not None
        evaluator = CQLEvaluator(data_source=data_source)
        library = evaluator.compile(example["code"])

        count = evaluator.evaluate_definition("Condition Count", resource=patient, library=library)
        expected = sum(1 for r in patient_resources if r.get("resourceType") == "Condition")
        assert count == expected

    def test_active_medications_example(self, data_source: InMemoryDataSource, patient: dict) -> None:
        """Active medications example should return medication data."""
        example = load_example("med-active")
        assert example is not None
        evaluator = CQLEvaluator(data_source=data_source)
        library = evaluator.compile(example["code"])

        meds = evaluator.evaluate_definition("All Medication Requests", resource=patient, library=library)
        assert isinstance(meds, list)
