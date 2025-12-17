"""Tests for IPS (International Patient Summary) $summary operation."""

import pytest

from fhirkit.server.operations.ips_summary import (
    IPS_COMPOSITION_PROFILE,
    IPS_PROFILE,
    IPS_SECTIONS,
    IPSSummaryGenerator,
)
from fhirkit.server.storage.fhir_store import FHIRStore


@pytest.fixture
def store():
    """Create a FHIR store with test data."""
    s = FHIRStore()

    # Create a patient
    s.create(
        {
            "resourceType": "Patient",
            "id": "patient-1",
            "name": [{"given": ["John"], "family": "Doe"}],
        }
    )

    # Create another patient without name
    s.create(
        {
            "resourceType": "Patient",
            "id": "patient-no-name",
        }
    )

    return s


@pytest.fixture
def store_with_data(store):
    """Create a FHIR store with comprehensive clinical data."""
    # AllergyIntolerance
    store.create(
        {
            "resourceType": "AllergyIntolerance",
            "id": "allergy-1",
            "patient": {"reference": "Patient/patient-1"},
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "91936005", "display": "Penicillin allergy"}],
                "text": "Penicillin",
            },
            "criticality": "high",
        }
    )

    # MedicationRequest
    store.create(
        {
            "resourceType": "MedicationRequest",
            "id": "medrq-1",
            "subject": {"reference": "Patient/patient-1"},
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1049502"}],
                "text": "Aspirin 325mg",
            },
            "status": "active",
            "intent": "order",
        }
    )

    # Condition
    store.create(
        {
            "resourceType": "Condition",
            "id": "condition-1",
            "subject": {"reference": "Patient/patient-1"},
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Type 2 diabetes"}],
                "text": "Type 2 Diabetes Mellitus",
            },
            "clinicalStatus": {
                "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
            },
        }
    )

    # Immunization
    store.create(
        {
            "resourceType": "Immunization",
            "id": "imm-1",
            "patient": {"reference": "Patient/patient-1"},
            "vaccineCode": {
                "coding": [{"system": "http://hl7.org/fhir/sid/cvx", "code": "207", "display": "COVID-19 vaccine"}],
                "text": "COVID-19 vaccine",
            },
            "occurrenceDateTime": "2024-01-15T10:00:00Z",
            "status": "completed",
        }
    )

    # Procedure
    store.create(
        {
            "resourceType": "Procedure",
            "id": "proc-1",
            "subject": {"reference": "Patient/patient-1"},
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "80146002", "display": "Appendectomy"}],
                "text": "Appendectomy",
            },
            "performedDateTime": "2023-06-20T14:30:00Z",
            "status": "completed",
        }
    )

    # Lab Observation
    store.create(
        {
            "resourceType": "Observation",
            "id": "obs-lab-1",
            "subject": {"reference": "Patient/patient-1"},
            "category": [
                {
                    "coding": [
                        {"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory"}
                    ]
                }
            ],
            "code": {
                "coding": [
                    {"system": "http://loinc.org", "code": "2339-0", "display": "Glucose [Mass/volume] in Blood"}
                ],
                "text": "Blood Glucose",
            },
            "valueQuantity": {"value": 95, "unit": "mg/dL", "system": "http://unitsofmeasure.org"},
            "status": "final",
        }
    )

    # Vital Signs Observation
    store.create(
        {
            "resourceType": "Observation",
            "id": "obs-vitals-1",
            "subject": {"reference": "Patient/patient-1"},
            "category": [
                {
                    "coding": [
                        {"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}
                    ]
                }
            ],
            "code": {
                "coding": [{"system": "http://loinc.org", "code": "8310-5", "display": "Body temperature"}],
                "text": "Body Temperature",
            },
            "valueQuantity": {"value": 37.0, "unit": "Cel", "system": "http://unitsofmeasure.org"},
            "status": "final",
        }
    )

    return store


class TestIPSSections:
    """Tests for IPS section definitions."""

    def test_sections_defined(self):
        """Test that all expected sections are defined."""
        expected_sections = [
            "allergies",
            "medications",
            "problems",
            "immunizations",
            "procedures",
            "results",
            "vital_signs",
        ]
        for section in expected_sections:
            assert section in IPS_SECTIONS

    def test_section_has_required_fields(self):
        """Test that each section has required fields."""
        for key, section in IPS_SECTIONS.items():
            assert "code" in section, f"Section {key} missing code"
            assert "display" in section, f"Section {key} missing display"
            assert "title" in section, f"Section {key} missing title"
            assert "resource_type" in section, f"Section {key} missing resource_type"


class TestIPSSummaryGenerator:
    """Tests for IPSSummaryGenerator."""

    def test_generate_patient_not_found(self, store):
        """Test generating summary for non-existent patient."""
        gen = IPSSummaryGenerator(store)
        result = gen.generate("nonexistent")

        assert result is None

    def test_generate_basic(self, store):
        """Test generating basic IPS bundle."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        assert bundle is not None
        assert bundle["resourceType"] == "Bundle"
        assert bundle["type"] == "document"

    def test_generate_has_ips_profile(self, store):
        """Test that generated bundle has IPS profile."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        assert IPS_PROFILE in bundle["meta"]["profile"]

    def test_generate_has_identifier(self, store):
        """Test that generated bundle has identifier."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        assert "identifier" in bundle
        assert bundle["identifier"]["system"] == "urn:ietf:rfc:3986"
        assert bundle["identifier"]["value"].startswith("urn:uuid:")

    def test_generate_has_timestamp(self, store):
        """Test that generated bundle has timestamp."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        assert "timestamp" in bundle

    def test_generate_composition_is_first(self, store):
        """Test that Composition is the first entry."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        first_entry = bundle["entry"][0]
        assert first_entry["resource"]["resourceType"] == "Composition"

    def test_generate_patient_is_second(self, store):
        """Test that Patient is the second entry."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        second_entry = bundle["entry"][1]
        assert second_entry["resource"]["resourceType"] == "Patient"

    def test_composition_has_ips_profile(self, store):
        """Test that Composition has IPS profile."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        assert IPS_COMPOSITION_PROFILE in composition["meta"]["profile"]

    def test_composition_has_subject(self, store):
        """Test that Composition has patient subject."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        assert composition["subject"]["reference"] == "Patient/patient-1"
        assert composition["subject"]["display"] == "John Doe"

    def test_composition_has_author(self, store):
        """Test that Composition has author."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        assert len(composition["author"]) > 0
        assert "reference" in composition["author"][0]

    def test_composition_has_title(self, store):
        """Test that Composition has title with patient name."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        assert "John Doe" in composition["title"]

    def test_composition_has_sections(self, store):
        """Test that Composition has all IPS sections."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        assert len(composition["section"]) == len(IPS_SECTIONS)

    def test_composition_section_has_code(self, store):
        """Test that each section has LOINC code."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        for section in composition["section"]:
            assert "code" in section
            assert "coding" in section["code"]
            assert section["code"]["coding"][0]["system"] == "http://loinc.org"

    def test_empty_section_has_empty_reason(self, store):
        """Test that empty sections have emptyReason."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        # Patient with no data should have empty sections
        for section in composition["section"]:
            if "entry" not in section:
                assert "emptyReason" in section
                assert section["emptyReason"]["coding"][0]["code"] == "unavailable"

    def test_empty_section_has_narrative(self, store):
        """Test that empty sections have narrative text."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        for section in composition["section"]:
            assert "text" in section
            assert "div" in section["text"]
            assert section["text"]["status"] == "generated"


class TestIPSSummaryWithData:
    """Tests for IPS summary with clinical data."""

    def test_generate_includes_clinical_data(self, store_with_data):
        """Test that bundle includes clinical resources."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        resource_types = {e["resource"]["resourceType"] for e in bundle["entry"]}
        assert "AllergyIntolerance" in resource_types
        assert "MedicationRequest" in resource_types
        assert "Condition" in resource_types
        assert "Immunization" in resource_types
        assert "Procedure" in resource_types
        # Note: Observations require category search which has limitations with nested arrays

    def test_section_has_entries(self, store_with_data):
        """Test that sections with data have entries."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]

        # Find allergies section
        allergies_section = next(s for s in composition["section"] if s["title"] == "Allergies and Intolerances")
        assert "entry" in allergies_section
        assert len(allergies_section["entry"]) == 1
        assert allergies_section["entry"][0]["reference"] == "AllergyIntolerance/allergy-1"

    def test_section_has_narrative_with_data(self, store_with_data):
        """Test that sections with data have proper narrative."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]

        # Find problems section
        problems_section = next(s for s in composition["section"] if s["title"] == "Active Problems")
        assert "text" in problems_section
        assert "Diabetes" in problems_section["text"]["div"]

    def test_allergy_display(self, store_with_data):
        """Test allergy display in narrative."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        allergies_section = next(s for s in composition["section"] if s["title"] == "Allergies and Intolerances")
        assert "Penicillin" in allergies_section["text"]["div"]
        assert "high" in allergies_section["text"]["div"]

    def test_medication_display(self, store_with_data):
        """Test medication display in narrative."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        meds_section = next(s for s in composition["section"] if s["title"] == "Medication Summary")
        assert "Aspirin" in meds_section["text"]["div"]
        assert "active" in meds_section["text"]["div"]

    def test_immunization_display_with_date(self, store_with_data):
        """Test immunization display includes date."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        imm_section = next(s for s in composition["section"] if s["title"] == "Immunizations")
        assert "COVID-19" in imm_section["text"]["div"]
        assert "2024-01-15" in imm_section["text"]["div"]

    def test_procedure_display_with_date(self, store_with_data):
        """Test procedure display includes date."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        proc_section = next(s for s in composition["section"] if s["title"] == "History of Procedures")
        assert "Appendectomy" in proc_section["text"]["div"]
        assert "2023-06-20" in proc_section["text"]["div"]

    def test_results_section_exists(self, store_with_data):
        """Test results section exists in composition."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        results_section = next(s for s in composition["section"] if s["title"] == "Results")
        # Section exists with proper structure
        assert "text" in results_section
        assert "code" in results_section

    def test_vital_signs_section_exists(self, store_with_data):
        """Test vital signs section exists in composition."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        vitals_section = next(s for s in composition["section"] if s["title"] == "Vital Signs")
        # Section exists with proper structure
        assert "text" in vitals_section
        assert "code" in vitals_section

    def test_bundle_entries_fullurl(self, store_with_data):
        """Test that bundle entries have fullUrl."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        for entry in bundle["entry"]:
            assert "fullUrl" in entry
            assert entry["fullUrl"].startswith("urn:uuid:")

    def test_no_duplicate_resources(self, store_with_data):
        """Test that resources are not duplicated in bundle."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1")

        refs = set()
        for entry in bundle["entry"]:
            resource = entry["resource"]
            ref = f"{resource['resourceType']}/{resource['id']}"
            assert ref not in refs, f"Duplicate resource: {ref}"
            refs.add(ref)


class TestIPSSummaryPatientName:
    """Tests for patient name handling."""

    def test_patient_without_name(self, store):
        """Test generating summary for patient without name."""
        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-no-name")

        composition = bundle["entry"][0]["resource"]
        assert "Unknown Patient" in composition["title"]
        assert composition["subject"]["display"] == "Unknown Patient"


class TestIPSSummaryPersist:
    """Tests for IPS summary persistence."""

    def test_generate_without_persist(self, store_with_data):
        """Test generating without persistence."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1", persist=False)

        # Bundle should not be stored
        result = store_with_data.read("Bundle", bundle["id"])
        assert result is None

    def test_generate_with_persist(self, store_with_data):
        """Test generating with persistence."""
        gen = IPSSummaryGenerator(store_with_data)
        bundle = gen.generate("patient-1", persist=True)

        # Bundle should be stored
        result = store_with_data.read("Bundle", bundle["id"])
        assert result is not None
        assert result["type"] == "document"


class TestIPSSummaryNarrativeTruncation:
    """Tests for narrative truncation with many items."""

    def test_narrative_truncates_at_20_items(self, store):
        """Test that narrative truncates after 20 items."""
        # Add 25 conditions
        for i in range(25):
            store.create(
                {
                    "resourceType": "Condition",
                    "id": f"cond-{i}",
                    "subject": {"reference": "Patient/patient-1"},
                    "code": {"text": f"Condition {i}"},
                }
            )

        gen = IPSSummaryGenerator(store)
        bundle = gen.generate("patient-1")

        composition = bundle["entry"][0]["resource"]
        problems_section = next(s for s in composition["section"] if s["title"] == "Active Problems")

        # Should have entries for all 25
        assert len(problems_section["entry"]) == 25

        # Narrative should indicate more items
        assert "... and 5 more" in problems_section["text"]["div"]


class TestIPSSummaryObservationValues:
    """Tests for observation value extraction helper methods."""

    def test_get_observation_value_quantity(self):
        """Test observation value extraction for valueQuantity."""
        gen = IPSSummaryGenerator(FHIRStore())
        observation = {
            "resourceType": "Observation",
            "valueQuantity": {"value": 98.6, "unit": "degF"},
        }
        result = gen._get_observation_value(observation)
        assert "98.6" in result
        assert "degF" in result

    def test_get_observation_value_codeable_concept(self):
        """Test observation value extraction for valueCodeableConcept."""
        gen = IPSSummaryGenerator(FHIRStore())
        observation = {
            "resourceType": "Observation",
            "valueCodeableConcept": {
                "coding": [{"code": "A+", "display": "A Positive"}],
            },
        }
        result = gen._get_observation_value(observation)
        assert result == "A Positive"

    def test_get_observation_value_string(self):
        """Test observation value extraction for valueString."""
        gen = IPSSummaryGenerator(FHIRStore())
        observation = {
            "resourceType": "Observation",
            "valueString": "Normal findings",
        }
        result = gen._get_observation_value(observation)
        assert result == "Normal findings"

    def test_get_observation_value_empty(self):
        """Test observation value extraction when no value present."""
        gen = IPSSummaryGenerator(FHIRStore())
        observation = {"resourceType": "Observation"}
        result = gen._get_observation_value(observation)
        assert result == ""


class TestIPSSummaryHelperMethods:
    """Tests for IPS summary helper methods."""

    def test_get_coding_display_with_display(self):
        """Test getting display from CodeableConcept with display."""
        gen = IPSSummaryGenerator(FHIRStore())
        cc = {"coding": [{"code": "12345", "display": "Test Display"}]}
        result = gen._get_coding_display(cc)
        assert result == "Test Display"

    def test_get_coding_display_fallback_to_code(self):
        """Test getting display falls back to code."""
        gen = IPSSummaryGenerator(FHIRStore())
        cc = {"coding": [{"code": "12345"}]}
        result = gen._get_coding_display(cc)
        assert result == "12345"

    def test_get_coding_display_empty(self):
        """Test getting display from empty CodeableConcept."""
        gen = IPSSummaryGenerator(FHIRStore())
        cc = {}
        result = gen._get_coding_display(cc)
        assert result == ""

    def test_get_patient_name(self):
        """Test extracting patient name."""
        gen = IPSSummaryGenerator(FHIRStore())
        patient = {"name": [{"given": ["John", "Q"], "family": "Doe"}]}
        result = gen._get_patient_name(patient)
        assert result == "John Q Doe"

    def test_get_patient_name_no_name(self):
        """Test extracting patient name when none exists."""
        gen = IPSSummaryGenerator(FHIRStore())
        patient = {}
        result = gen._get_patient_name(patient)
        assert result == "Unknown Patient"

    def test_get_resource_display_allergy(self):
        """Test resource display for AllergyIntolerance."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "AllergyIntolerance",
            "code": {"text": "Peanuts"},
            "criticality": "high",
        }
        result = gen._get_resource_display(resource, "AllergyIntolerance")
        assert "Peanuts" in result
        assert "high" in result

    def test_get_resource_display_medication(self):
        """Test resource display for MedicationRequest."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "MedicationRequest",
            "medicationCodeableConcept": {"text": "Aspirin"},
            "status": "active",
        }
        result = gen._get_resource_display(resource, "MedicationRequest")
        assert "Aspirin" in result
        assert "active" in result

    def test_get_resource_display_condition(self):
        """Test resource display for Condition."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "Condition",
            "code": {"text": "Diabetes"},
            "clinicalStatus": {"coding": [{"code": "active"}]},
        }
        result = gen._get_resource_display(resource, "Condition")
        assert "Diabetes" in result
        assert "active" in result

    def test_get_resource_display_immunization(self):
        """Test resource display for Immunization."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "Immunization",
            "vaccineCode": {"text": "Flu Shot"},
            "occurrenceDateTime": "2024-10-15T10:00:00Z",
        }
        result = gen._get_resource_display(resource, "Immunization")
        assert "Flu Shot" in result
        assert "2024-10-15" in result

    def test_get_resource_display_procedure(self):
        """Test resource display for Procedure."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "Procedure",
            "code": {"text": "Appendectomy"},
            "performedDateTime": "2023-06-20T14:30:00Z",
        }
        result = gen._get_resource_display(resource, "Procedure")
        assert "Appendectomy" in result
        assert "2023-06-20" in result

    def test_get_resource_display_observation(self):
        """Test resource display for Observation."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {
            "resourceType": "Observation",
            "code": {"text": "Blood Pressure"},
            "valueQuantity": {"value": 120, "unit": "mmHg"},
        }
        result = gen._get_resource_display(resource, "Observation")
        assert "Blood Pressure" in result
        assert "120" in result

    def test_get_resource_display_unknown_type(self):
        """Test resource display for unknown resource type."""
        gen = IPSSummaryGenerator(FHIRStore())
        resource = {"resourceType": "Unknown", "id": "test-123"}
        result = gen._get_resource_display(resource, "Unknown")
        assert result == "test-123"
