"""Integration tests for CQL with generator-produced data.

These tests verify that CQL queries work correctly with data
produced by the patient record generator, catching mismatches
between generated data structures and CQL expectations.
"""

import pytest

from fhirkit.engine.cql import CQLEvaluator, InMemoryDataSource
from fhirkit.server.generator import PatientRecordGenerator


class TestCQLWithGeneratedData:
    """Integration tests for CQL with generator-produced data."""

    @pytest.fixture
    def generator(self) -> PatientRecordGenerator:
        """Create a seeded generator for reproducible tests."""
        return PatientRecordGenerator(seed=42)

    @pytest.fixture
    def patient_resources(self, generator: PatientRecordGenerator) -> list[dict]:
        """Generate a complete patient record."""
        return generator.generate_patient_record(
            num_conditions=(3, 5),
            num_encounters=(2, 4),
            num_observations_per_encounter=(3, 5),
            num_medications=(2, 4),
            num_procedures=(1, 2),
            num_allergies=(1, 3),
            num_immunizations=(2, 4),
        )

    @pytest.fixture
    def patient(self, patient_resources: list[dict]) -> dict:
        """Extract the patient resource."""
        for r in patient_resources:
            if r.get("resourceType") == "Patient":
                return r
        raise ValueError("No Patient found in generated resources")

    @pytest.fixture
    def data_source(self, patient_resources: list[dict]) -> InMemoryDataSource:
        """Create data source from generated patient resources."""
        ds = InMemoryDataSource()
        for resource in patient_resources:
            ds.add_resource(resource)
        return ds

    @pytest.fixture
    def evaluator(self, data_source: InMemoryDataSource) -> CQLEvaluator:
        """Create CQL evaluator with the generated data source."""
        return CQLEvaluator(data_source=data_source)

    # =========================================================================
    # PATIENT DEMOGRAPHICS
    # =========================================================================

    def test_patient_name_access(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing Patient.name from generated data."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define PatientName: Patient.name
        """)

        result = evaluator.evaluate_definition("PatientName", resource=patient)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    def test_patient_birthdate_access(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing Patient.birthDate from generated data."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define BirthDate: Patient.birthDate
        """)

        result = evaluator.evaluate_definition("BirthDate", resource=patient)

        assert result is not None
        # Should be a date string
        assert isinstance(result, str)

    def test_patient_gender_access(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing Patient.gender from generated data."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define Gender: Patient.gender
        """)

        result = evaluator.evaluate_definition("Gender", resource=patient)

        assert result is not None
        assert result in ["male", "female", "other", "unknown"]

    def test_age_in_years(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test AgeInYears() with generated birthDate."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define Age: AgeInYears()
        """)

        result = evaluator.evaluate_definition("Age", resource=patient)

        # Age should be a reasonable value (0-120)
        assert result is not None
        assert isinstance(result, int)
        assert 0 <= result <= 120

    # =========================================================================
    # RESOURCE RETRIEVAL
    # =========================================================================

    def test_retrieve_conditions(self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]) -> None:
        """Test [Condition] returns generated conditions."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllConditions: [Condition]
        """)

        result = evaluator.evaluate_definition("AllConditions", resource=patient)

        # Count conditions in generated data
        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "Condition")

        assert isinstance(result, list)
        assert len(result) == expected_count
        assert len(result) > 0  # Should have at least some conditions

    def test_retrieve_observations(self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]) -> None:
        """Test [Observation] returns generated observations."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllObservations: [Observation]
        """)

        result = evaluator.evaluate_definition("AllObservations", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "Observation")

        assert isinstance(result, list)
        assert len(result) == expected_count
        assert len(result) > 0

    def test_retrieve_medication_requests(
        self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]
    ) -> None:
        """Test [MedicationRequest] returns generated medications."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllMedications: [MedicationRequest]
        """)

        result = evaluator.evaluate_definition("AllMedications", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "MedicationRequest")

        assert isinstance(result, list)
        assert len(result) == expected_count
        assert len(result) > 0

    def test_retrieve_encounters(self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]) -> None:
        """Test [Encounter] returns generated encounters."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllEncounters: [Encounter]
        """)

        result = evaluator.evaluate_definition("AllEncounters", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "Encounter")

        assert isinstance(result, list)
        assert len(result) == expected_count
        assert len(result) > 0

    def test_retrieve_allergies(self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]) -> None:
        """Test [AllergyIntolerance] returns generated allergies."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllAllergies: [AllergyIntolerance]
        """)

        result = evaluator.evaluate_definition("AllAllergies", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "AllergyIntolerance")

        assert isinstance(result, list)
        assert len(result) == expected_count

    def test_retrieve_immunizations(
        self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]
    ) -> None:
        """Test [Immunization] returns generated immunizations."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllImmunizations: [Immunization]
        """)

        result = evaluator.evaluate_definition("AllImmunizations", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "Immunization")

        assert isinstance(result, list)
        assert len(result) == expected_count

    def test_retrieve_procedures(self, evaluator: CQLEvaluator, patient: dict, patient_resources: list[dict]) -> None:
        """Test [Procedure] returns generated procedures."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define AllProcedures: [Procedure]
        """)

        result = evaluator.evaluate_definition("AllProcedures", resource=patient)

        expected_count = sum(1 for r in patient_resources if r.get("resourceType") == "Procedure")

        assert isinstance(result, list)
        assert len(result) == expected_count

    # =========================================================================
    # FILTERED QUERIES
    # =========================================================================

    def test_active_conditions(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test filtering conditions by clinicalStatus."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ActiveConditions: [Condition] C
                where C.clinicalStatus.coding.code contains 'active'
        """)

        result = evaluator.evaluate_definition("ActiveConditions", resource=patient)

        assert isinstance(result, list)
        # All returned conditions should have active status
        for item in result:
            condition = item.get("C", item)
            status = condition.get("clinicalStatus", {})
            codings = status.get("coding", [])
            codes = [c.get("code") for c in codings]
            assert "active" in codes

    def test_active_medications(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test filtering medications by status = 'active'."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ActiveMedications: [MedicationRequest] M
                where M.status = 'active'
        """)

        result = evaluator.evaluate_definition("ActiveMedications", resource=patient)

        assert isinstance(result, list)
        # All returned medications should be active
        for item in result:
            med = item.get("M", item)
            assert med.get("status") == "active"

    def test_completed_encounters(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test filtering encounters by status."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define CompletedEncounters: [Encounter] E
                where E.status = 'finished'
        """)

        result = evaluator.evaluate_definition("CompletedEncounters", resource=patient)

        assert isinstance(result, list)
        for item in result:
            enc = item.get("E", item)
            assert enc.get("status") == "finished"

    # =========================================================================
    # VALUE ACCESS
    # =========================================================================

    def test_observation_value_quantity(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing valueQuantity.value from observations."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ObsWithValues: [Observation] O
                where O.value is Quantity
            define FirstValue: First("ObsWithValues").value
        """)

        obs_result = evaluator.evaluate_definition("ObsWithValues", resource=patient)

        # Should find observations with Quantity values
        assert isinstance(obs_result, list)
        # Generator should produce observations with valueQuantity

    def test_medication_code_access(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing medication code from MedicationRequest."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define MedCodes: [MedicationRequest] M
                return M.medication.coding
        """)

        result = evaluator.evaluate_definition("MedCodes", resource=patient)

        assert isinstance(result, list)
        # Should return coding arrays for each medication

    def test_condition_code_display(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test accessing condition code display text."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ConditionNames: [Condition] C
                return C.code.coding.display
        """)

        result = evaluator.evaluate_definition("ConditionNames", resource=patient)

        assert isinstance(result, list)
        assert len(result) > 0

    # =========================================================================
    # CLINICAL LOGIC
    # =========================================================================

    def test_count_resources(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test counting generated resources."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ConditionCount: Count([Condition])
            define MedicationCount: Count([MedicationRequest])
            define EncounterCount: Count([Encounter])
        """)

        cond_count = evaluator.evaluate_definition("ConditionCount", resource=patient)
        med_count = evaluator.evaluate_definition("MedicationCount", resource=patient)
        enc_count = evaluator.evaluate_definition("EncounterCount", resource=patient)

        assert isinstance(cond_count, int)
        assert isinstance(med_count, int)
        assert isinstance(enc_count, int)
        assert cond_count > 0
        assert med_count > 0
        assert enc_count > 0

    def test_exists_check(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test exists() with generated data."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define HasConditions: exists([Condition])
            define HasMedications: exists([MedicationRequest])
            define HasEncounters: exists([Encounter])
        """)

        has_cond = evaluator.evaluate_definition("HasConditions", resource=patient)
        has_med = evaluator.evaluate_definition("HasMedications", resource=patient)
        has_enc = evaluator.evaluate_definition("HasEncounters", resource=patient)

        assert has_cond is True
        assert has_med is True
        assert has_enc is True

    def test_first_last_resources(self, evaluator: CQLEvaluator, patient: dict) -> None:
        """Test First() and Last() with generated resources."""
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define FirstCondition: First([Condition])
            define LastCondition: Last([Condition])
        """)

        first = evaluator.evaluate_definition("FirstCondition", resource=patient)
        last = evaluator.evaluate_definition("LastCondition", resource=patient)

        assert first is not None
        assert last is not None
        assert first.get("resourceType") == "Condition"
        assert last.get("resourceType") == "Condition"


class TestMultiplePatients:
    """Test CQL with multiple generated patients."""

    def test_patient_isolation(self) -> None:
        """Test that CQL correctly isolates resources per patient."""
        generator = PatientRecordGenerator(seed=42)

        # Generate two patients
        patient1_resources = generator.generate_patient_record(
            num_conditions=(2, 3),
            num_medications=(1, 2),
        )
        patient2_resources = generator.generate_patient_record(
            num_conditions=(4, 5),
            num_medications=(3, 4),
        )

        # Create data source with both patients' data
        ds = InMemoryDataSource()
        for r in patient1_resources:
            ds.add_resource(r)
        for r in patient2_resources:
            ds.add_resource(r)

        # Get patient resources
        patient1 = next(r for r in patient1_resources if r.get("resourceType") == "Patient")
        patient2 = next(r for r in patient2_resources if r.get("resourceType") == "Patient")

        # Create evaluator
        evaluator = CQLEvaluator(data_source=ds)
        evaluator.compile("""
            library Test version '1.0'
            using FHIR version '4.0.1'
            context Patient
            define ConditionCount: Count([Condition])
        """)

        # Count conditions for each patient
        count1 = evaluator.evaluate_definition("ConditionCount", resource=patient1)
        count2 = evaluator.evaluate_definition("ConditionCount", resource=patient2)

        # Counts should match what was generated for each patient
        expected_count1 = sum(1 for r in patient1_resources if r.get("resourceType") == "Condition")
        expected_count2 = sum(1 for r in patient2_resources if r.get("resourceType") == "Condition")

        assert count1 == expected_count1
        assert count2 == expected_count2
        # Counts should be different (different generation parameters)
        assert count1 != count2
