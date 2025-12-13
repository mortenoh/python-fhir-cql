"""Tests for terminology service."""

import pytest

from fhir_cql.terminology import (
    InMemoryTerminologyService,
    MemberOfRequest,
    SubsumesRequest,
    ValidateCodeRequest,
    ValueSet,
    ValueSetCompose,
    ValueSetComposeInclude,
    ValueSetComposeIncludeConcept,
    ValueSetExpansion,
    ValueSetExpansionContains,
)


@pytest.fixture
def service() -> InMemoryTerminologyService:
    """Create a service with test value sets."""
    service = InMemoryTerminologyService()

    # Add observation status value set
    obs_status_vs = ValueSet(
        url="http://hl7.org/fhir/ValueSet/observation-status",
        name="ObservationStatus",
        compose=ValueSetCompose(
            include=[
                ValueSetComposeInclude(
                    system="http://hl7.org/fhir/observation-status",
                    concept=[
                        ValueSetComposeIncludeConcept(code="registered", display="Registered"),
                        ValueSetComposeIncludeConcept(code="preliminary", display="Preliminary"),
                        ValueSetComposeIncludeConcept(code="final", display="Final"),
                        ValueSetComposeIncludeConcept(code="amended", display="Amended"),
                    ],
                )
            ]
        ),
    )
    service.add_value_set(obs_status_vs)

    # Add expanded value set
    gender_vs = ValueSet(
        url="http://hl7.org/fhir/ValueSet/administrative-gender",
        name="AdministrativeGender",
        expansion=ValueSetExpansion(
            contains=[
                ValueSetExpansionContains(
                    system="http://hl7.org/fhir/administrative-gender",
                    code="male",
                    display="Male",
                ),
                ValueSetExpansionContains(
                    system="http://hl7.org/fhir/administrative-gender",
                    code="female",
                    display="Female",
                ),
                ValueSetExpansionContains(
                    system="http://hl7.org/fhir/administrative-gender",
                    code="other",
                    display="Other",
                ),
                ValueSetExpansionContains(
                    system="http://hl7.org/fhir/administrative-gender",
                    code="unknown",
                    display="Unknown",
                ),
            ]
        ),
    )
    service.add_value_set(gender_vs)

    return service


class TestValidateCode:
    """Test $validate-code operation."""

    def test_validate_code_in_compose(self, service):
        request = ValidateCodeRequest(
            url="http://hl7.org/fhir/ValueSet/observation-status",
            code="final",
            system="http://hl7.org/fhir/observation-status",
        )
        result = service.validate_code(request)
        assert result.result is True

    def test_validate_code_not_in_valueset(self, service):
        request = ValidateCodeRequest(
            url="http://hl7.org/fhir/ValueSet/observation-status",
            code="invalid-code",
            system="http://hl7.org/fhir/observation-status",
        )
        result = service.validate_code(request)
        assert result.result is False

    def test_validate_code_in_expansion(self, service):
        request = ValidateCodeRequest(
            url="http://hl7.org/fhir/ValueSet/administrative-gender",
            code="male",
            system="http://hl7.org/fhir/administrative-gender",
        )
        result = service.validate_code(request)
        assert result.result is True

    def test_validate_code_wrong_system(self, service):
        request = ValidateCodeRequest(
            url="http://hl7.org/fhir/ValueSet/observation-status",
            code="final",
            system="http://wrong-system.org",
        )
        result = service.validate_code(request)
        assert result.result is False

    def test_validate_code_without_system(self, service):
        # Should match if code exists in any system within the value set
        request = ValidateCodeRequest(
            url="http://hl7.org/fhir/ValueSet/observation-status",
            code="final",
        )
        result = service.validate_code(request)
        assert result.result is True

    def test_validate_valueset_not_found(self, service):
        request = ValidateCodeRequest(
            url="http://nonexistent/ValueSet",
            code="some-code",
        )
        result = service.validate_code(request)
        assert result.result is False
        assert result.message == "Value set not found"


class TestMemberOf:
    """Test memberOf operation."""

    def test_member_of_true(self, service):
        request = MemberOfRequest(
            code="final",
            system="http://hl7.org/fhir/observation-status",
            valueSetUrl="http://hl7.org/fhir/ValueSet/observation-status",
        )
        result = service.member_of(request)
        assert result.result is True

    def test_member_of_false(self, service):
        request = MemberOfRequest(
            code="invalid",
            system="http://hl7.org/fhir/observation-status",
            valueSetUrl="http://hl7.org/fhir/ValueSet/observation-status",
        )
        result = service.member_of(request)
        assert result.result is False

    def test_member_of_valueset_not_found(self, service):
        request = MemberOfRequest(
            code="final",
            system="http://hl7.org/fhir/observation-status",
            valueSetUrl="http://nonexistent/ValueSet",
        )
        result = service.member_of(request)
        assert result.result is False


class TestSubsumes:
    """Test $subsumes operation."""

    def test_subsumes_equivalent(self, service):
        request = SubsumesRequest(
            codeA="final",
            codeB="final",
            system="http://hl7.org/fhir/observation-status",
        )
        result = service.subsumes(request)
        assert result.outcome == "equivalent"

    def test_subsumes_not_subsumed(self, service):
        request = SubsumesRequest(
            codeA="final",
            codeB="preliminary",
            system="http://hl7.org/fhir/observation-status",
        )
        result = service.subsumes(request)
        assert result.outcome == "not-subsumed"


class TestValueSetRetrieval:
    """Test value set retrieval."""

    def test_get_value_set(self, service):
        vs = service.get_value_set("http://hl7.org/fhir/ValueSet/observation-status")
        assert vs is not None
        assert vs.name == "ObservationStatus"

    def test_get_value_set_not_found(self, service):
        vs = service.get_value_set("http://nonexistent/ValueSet")
        assert vs is None
