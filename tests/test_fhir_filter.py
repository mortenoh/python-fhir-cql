"""Tests for FHIR _filter parameter."""

import pytest
from fastapi.testclient import TestClient

from fhirkit.server.api.app import create_app
from fhirkit.server.api.filter_parser import (
    FilterCondition,
    FilterEvaluator,
    FilterExpression,
    FilterOp,
    FilterParser,
    LogicalOp,
    apply_filter,
)
from fhirkit.server.config.settings import FHIRServerSettings


@pytest.fixture
def client():
    """Create a test client with sample data."""
    settings = FHIRServerSettings(patients=0, enable_docs=False, enable_ui=False, api_base_path="")
    app = create_app(settings=settings)
    client = TestClient(app)

    # Create test patients
    client.post(
        "/Patient",
        json={
            "resourceType": "Patient",
            "id": "patient-1",
            "name": [{"family": "Smith", "given": ["John"]}],
            "gender": "male",
            "birthDate": "1980-01-15",
            "active": True,
        },
    )
    client.post(
        "/Patient",
        json={
            "resourceType": "Patient",
            "id": "patient-2",
            "name": [{"family": "Doe", "given": ["Jane"]}],
            "gender": "female",
            "birthDate": "1990-05-20",
            "active": True,
        },
    )
    client.post(
        "/Patient",
        json={
            "resourceType": "Patient",
            "id": "patient-3",
            "name": [{"family": "Johnson", "given": ["Bob"]}],
            "gender": "male",
            "birthDate": "1975-12-01",
            "active": False,
        },
    )

    return client


class TestFilterParser:
    """Tests for FilterParser."""

    def test_parse_simple_eq(self):
        """Test parsing simple equals expression."""
        parser = FilterParser('gender eq "male"')
        expr = parser.parse()
        assert expr.condition is not None
        assert expr.condition.path == "gender"
        assert expr.condition.op == FilterOp.EQ
        assert expr.condition.value == "male"

    def test_parse_unquoted_value(self):
        """Test parsing with unquoted value."""
        parser = FilterParser("gender eq male")
        expr = parser.parse()
        assert expr.condition.value == "male"

    def test_parse_date_value(self):
        """Test parsing date value."""
        parser = FilterParser("birthDate ge 1990-01-01")
        expr = parser.parse()
        assert expr.condition.path == "birthdate"
        assert expr.condition.op == FilterOp.GE
        assert expr.condition.value == "1990-01-01"

    def test_parse_and_expression(self):
        """Test parsing AND expression."""
        parser = FilterParser("gender eq male and active eq true")
        expr = parser.parse()
        assert expr.logical_op == LogicalOp.AND
        assert expr.left.condition.path == "gender"
        assert expr.right.condition.path == "active"

    def test_parse_or_expression(self):
        """Test parsing OR expression."""
        parser = FilterParser('gender eq male or gender eq "female"')
        expr = parser.parse()
        assert expr.logical_op == LogicalOp.OR

    def test_parse_not_expression(self):
        """Test parsing NOT expression."""
        parser = FilterParser("not active eq true")
        expr = parser.parse()
        assert expr.logical_op == LogicalOp.NOT
        assert expr.negated is True

    def test_parse_parentheses(self):
        """Test parsing with parentheses."""
        parser = FilterParser("(gender eq male) and (active eq true)")
        expr = parser.parse()
        assert expr.logical_op == LogicalOp.AND

    def test_parse_complex_expression(self):
        """Test parsing complex expression."""
        parser = FilterParser("(gender eq male or gender eq female) and birthDate ge 1990-01-01")
        expr = parser.parse()
        assert expr.logical_op == LogicalOp.AND
        assert expr.left.logical_op == LogicalOp.OR

    def test_parse_all_operators(self):
        """Test parsing all comparison operators."""
        ops = ["eq", "ne", "gt", "lt", "ge", "le", "co", "sw", "ew"]
        for op in ops:
            parser = FilterParser(f"name {op} value")
            expr = parser.parse()
            assert expr.condition.op.value == op


class TestFilterEvaluator:
    """Tests for FilterEvaluator."""

    def test_eq_match(self):
        """Test equals matching."""
        resource = {"gender": "male"}
        expr = FilterExpression(condition=FilterCondition("gender", FilterOp.EQ, "male"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_eq_no_match(self):
        """Test equals not matching."""
        resource = {"gender": "female"}
        expr = FilterExpression(condition=FilterCondition("gender", FilterOp.EQ, "male"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is False

    def test_ne_match(self):
        """Test not equals matching."""
        resource = {"gender": "female"}
        expr = FilterExpression(condition=FilterCondition("gender", FilterOp.NE, "male"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_co_match(self):
        """Test contains matching."""
        resource = {"name": [{"family": "Smith"}]}
        expr = FilterExpression(condition=FilterCondition("name.family", FilterOp.CO, "mit"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_sw_match(self):
        """Test starts with matching."""
        resource = {"name": [{"family": "Smith"}]}
        expr = FilterExpression(condition=FilterCondition("name.family", FilterOp.SW, "sm"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_ew_match(self):
        """Test ends with matching."""
        resource = {"name": [{"family": "Smith"}]}
        expr = FilterExpression(condition=FilterCondition("name.family", FilterOp.EW, "th"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_gt_numeric(self):
        """Test greater than numeric."""
        resource = {"valueInteger": 100}
        expr = FilterExpression(condition=FilterCondition("valueInteger", FilterOp.GT, "50"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_le_date(self):
        """Test less than or equal date."""
        resource = {"birthDate": "1990-01-01"}
        expr = FilterExpression(condition=FilterCondition("birthDate", FilterOp.LE, "2000-01-01"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_and_expression(self):
        """Test AND expression evaluation."""
        resource = {"gender": "male", "active": True}
        left = FilterExpression(condition=FilterCondition("gender", FilterOp.EQ, "male"))
        right = FilterExpression(condition=FilterCondition("active", FilterOp.EQ, "true"))
        expr = FilterExpression(logical_op=LogicalOp.AND, left=left, right=right)
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_or_expression(self):
        """Test OR expression evaluation."""
        resource = {"gender": "female"}
        left = FilterExpression(condition=FilterCondition("gender", FilterOp.EQ, "male"))
        right = FilterExpression(condition=FilterCondition("gender", FilterOp.EQ, "female"))
        expr = FilterExpression(logical_op=LogicalOp.OR, left=left, right=right)
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_not_expression(self):
        """Test NOT expression evaluation."""
        resource = {"active": False}
        inner = FilterExpression(condition=FilterCondition("active", FilterOp.EQ, "true"))
        expr = FilterExpression(logical_op=LogicalOp.NOT, left=inner, negated=True)
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True

    def test_codeable_concept(self):
        """Test matching CodeableConcept."""
        resource = {"code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic BP"}]}}
        expr = FilterExpression(condition=FilterCondition("code", FilterOp.EQ, "8480-6"))
        evaluator = FilterEvaluator({})
        assert evaluator.evaluate(resource, expr) is True


class TestApplyFilter:
    """Tests for apply_filter function."""

    def test_apply_filter_eq(self):
        """Test applying equals filter."""
        resources = [
            {"id": "1", "gender": "male"},
            {"id": "2", "gender": "female"},
            {"id": "3", "gender": "male"},
        ]
        result = apply_filter(resources, "gender eq male", {})
        assert len(result) == 2
        assert all(r["gender"] == "male" for r in result)

    def test_apply_filter_and(self):
        """Test applying AND filter."""
        resources = [
            {"id": "1", "gender": "male", "active": True},
            {"id": "2", "gender": "female", "active": True},
            {"id": "3", "gender": "male", "active": False},
        ]
        result = apply_filter(resources, "gender eq male and active eq true", {})
        assert len(result) == 1
        assert result[0]["id"] == "1"

    def test_apply_filter_or(self):
        """Test applying OR filter."""
        resources = [
            {"id": "1", "gender": "male"},
            {"id": "2", "gender": "female"},
            {"id": "3", "gender": "other"},
        ]
        result = apply_filter(resources, "gender eq male or gender eq female", {})
        assert len(result) == 2

    def test_apply_filter_empty_expression(self):
        """Test applying empty filter returns all."""
        resources = [{"id": "1"}, {"id": "2"}]
        result = apply_filter(resources, "", {})
        assert len(result) == 2


class TestFilterEndpoint:
    """Integration tests for _filter parameter in search endpoint."""

    def test_filter_eq(self, client):
        """Test _filter with equals."""
        response = client.get("/Patient", params={"_filter": "gender eq male"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 2
        for entry in bundle["entry"]:
            assert entry["resource"]["gender"] == "male"

    def test_filter_ne(self, client):
        """Test _filter with not equals."""
        response = client.get("/Patient", params={"_filter": "gender ne male"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["gender"] == "female"

    def test_filter_and(self, client):
        """Test _filter with AND."""
        response = client.get("/Patient", params={"_filter": "gender eq male and active eq true"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["id"] == "patient-1"

    def test_filter_or(self, client):
        """Test _filter with OR."""
        response = client.get("/Patient", params={"_filter": "gender eq male or gender eq female"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 3

    def test_filter_birthdate_ge(self, client):
        """Test _filter with date greater than or equal."""
        response = client.get("/Patient", params={"_filter": "birthDate ge 1985-01-01"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1  # Only Jane Doe born 1990

    def test_filter_contains(self, client):
        """Test _filter with contains."""
        response = client.get("/Patient", params={"_filter": "family co son"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["id"] == "patient-3"

    def test_filter_starts_with(self, client):
        """Test _filter with starts with."""
        response = client.get("/Patient", params={"_filter": "family sw Sm"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["name"][0]["family"] == "Smith"

    def test_filter_complex(self, client):
        """Test _filter with complex expression."""
        response = client.get(
            "/Patient",
            params={"_filter": "(gender eq male) and (birthDate ge 1980-01-01)"},
        )
        assert response.status_code == 200
        bundle = response.json()
        # Should match patient-1 (John Smith, male, born 1980)
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["id"] == "patient-1"

    def test_filter_not(self, client):
        """Test _filter with NOT."""
        response = client.get("/Patient", params={"_filter": "not active eq false"})
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 2  # patient-1 and patient-2 are active

    def test_filter_invalid_syntax(self, client):
        """Test _filter with invalid syntax returns error."""
        response = client.get("/Patient", params={"_filter": "invalid syntax"})
        assert response.status_code == 400
        outcome = response.json()
        assert outcome["resourceType"] == "OperationOutcome"
        assert "Invalid _filter" in outcome["issue"][0]["diagnostics"]

    def test_filter_combined_with_search(self, client):
        """Test _filter combined with regular search params."""
        response = client.get(
            "/Patient",
            params={"gender": "male", "_filter": "active eq true"},
        )
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["total"] == 1
        assert bundle["entry"][0]["resource"]["id"] == "patient-1"
