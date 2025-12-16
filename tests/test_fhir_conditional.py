"""Tests for FHIR conditional operations."""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from fhirkit.server.api.app import create_app
from fhirkit.server.api.conditional import (
    check_conditional_read,
    etag_matches,
    is_modified_since,
    parse_etag,
    parse_if_modified_since,
    parse_if_none_match,
    parse_last_updated,
)
from fhirkit.server.config.settings import FHIRServerSettings
from fhirkit.server.storage.fhir_store import FHIRStore


@pytest.fixture
def store() -> FHIRStore:
    """Create a fresh FHIR store."""
    return FHIRStore()


@pytest.fixture
def client(store: FHIRStore) -> TestClient:
    """Create a test client."""
    settings = FHIRServerSettings(patients=0, enable_docs=False, enable_ui=False, api_base_path="")
    app = create_app(settings=settings, store=store)
    return TestClient(app)


class TestConditionalCreate:
    """Tests for conditional create (If-None-Exist header)."""

    def test_conditional_create_no_match(self, client):
        """Test conditional create with no existing match creates resource."""
        # Create with unique identifier
        response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "unique-123"}],
                "name": [{"family": "Test"}],
            },
            headers={"If-None-Exist": "identifier=test|unique-123"},
        )

        assert response.status_code == 201
        patient = response.json()
        assert patient["resourceType"] == "Patient"
        assert "id" in patient

    def test_conditional_create_single_match(self, client):
        """Test conditional create with single match returns existing (200)."""
        # First create a patient
        create_response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "cond-create-match"}],
                "name": [{"family": "Original"}],
            },
        )
        assert create_response.status_code == 201
        original = create_response.json()

        # Try conditional create with same identifier
        response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "cond-create-match"}],
                "name": [{"family": "New"}],
            },
            headers={"If-None-Exist": "identifier=test|cond-create-match"},
        )

        # Should return 200 with existing resource
        assert response.status_code == 200
        returned = response.json()
        assert returned["id"] == original["id"]
        assert returned["name"][0]["family"] == "Original"  # Not updated

    def test_conditional_create_multiple_matches(self, client):
        """Test conditional create with multiple matches returns 412."""
        # Create two patients with same family name
        client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "name": [{"family": "DuplicateFamily"}],
            },
        )
        client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "name": [{"family": "DuplicateFamily"}],
            },
        )

        # Try conditional create matching both
        response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "name": [{"family": "DuplicateFamily"}],
            },
            headers={"If-None-Exist": "family=DuplicateFamily"},
        )

        assert response.status_code == 412
        outcome = response.json()
        assert outcome["resourceType"] == "OperationOutcome"
        assert "match" in outcome["issue"][0]["diagnostics"].lower()

    def test_conditional_create_without_header(self, client):
        """Test regular create works without If-None-Exist header."""
        response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "name": [{"family": "Regular"}],
            },
        )

        assert response.status_code == 201


class TestConditionalUpdate:
    """Tests for conditional update (PUT with search params)."""

    def test_conditional_update_no_match_creates(self, client):
        """Test conditional update with no match creates new resource."""
        response = client.put(
            "/Patient?identifier=test|new-cond-update",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "new-cond-update"}],
                "name": [{"family": "NewPatient"}],
            },
        )

        assert response.status_code == 201
        patient = response.json()
        assert patient["name"][0]["family"] == "NewPatient"

    def test_conditional_update_single_match_updates(self, client):
        """Test conditional update with single match updates the resource."""
        # First create a patient
        create_response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "cond-update-test"}],
                "name": [{"family": "Original"}],
            },
        )
        assert create_response.status_code == 201
        original = create_response.json()

        # Conditional update by identifier
        response = client.put(
            "/Patient?identifier=test|cond-update-test",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "cond-update-test"}],
                "name": [{"family": "Updated"}],
            },
        )

        assert response.status_code == 200
        updated = response.json()
        assert updated["id"] == original["id"]
        assert updated["name"][0]["family"] == "Updated"

    def test_conditional_update_multiple_matches(self, client):
        """Test conditional update with multiple matches returns 412."""
        # Create two patients with same gender
        client.post(
            "/Patient",
            json={"resourceType": "Patient", "gender": "other", "name": [{"family": "A"}]},
        )
        client.post(
            "/Patient",
            json={"resourceType": "Patient", "gender": "other", "name": [{"family": "B"}]},
        )

        # Try conditional update matching both
        response = client.put(
            "/Patient?gender=other",
            json={
                "resourceType": "Patient",
                "gender": "other",
                "name": [{"family": "Updated"}],
            },
        )

        assert response.status_code == 412
        outcome = response.json()
        assert outcome["resourceType"] == "OperationOutcome"

    def test_conditional_update_no_params(self, client):
        """Test conditional update without search params returns 400."""
        response = client.put(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "Test"}]},
        )

        assert response.status_code == 400
        outcome = response.json()
        assert "requires search parameters" in outcome["issue"][0]["diagnostics"]

    def test_conditional_update_wrong_resource_type(self, client):
        """Test conditional update with wrong resourceType in body."""
        response = client.put(
            "/Patient?identifier=test|xyz",
            json={"resourceType": "Observation", "status": "final"},
        )

        assert response.status_code == 400


class TestConditionalDelete:
    """Tests for conditional delete (DELETE with search params)."""

    def test_conditional_delete_deletes_matches(self, client):
        """Test conditional delete removes all matching resources."""
        # Create some patients to delete
        for i in range(3):
            client.post(
                "/Observation",
                json={
                    "resourceType": "Observation",
                    "status": "cancelled",
                    "code": {"text": f"test-delete-{i}"},
                },
            )

        # Search to verify they exist
        search_before = client.get("/Observation?status=cancelled")
        count_before = search_before.json().get("total", 0)
        assert count_before >= 3

        # Conditional delete
        response = client.delete("/Observation?status=cancelled")

        assert response.status_code == 204

        # Verify they're deleted
        search_after = client.get("/Observation?status=cancelled")
        count_after = search_after.json().get("total", 0)
        assert count_after == 0

    def test_conditional_delete_no_match(self, client):
        """Test conditional delete with no matches returns 204."""
        response = client.delete("/Patient?identifier=nonexistent|12345")

        # FHIR spec: return 204 even if nothing deleted
        assert response.status_code == 204

    def test_conditional_delete_no_params(self, client):
        """Test conditional delete without search params returns 400."""
        response = client.delete("/Patient")

        assert response.status_code == 400
        outcome = response.json()
        assert "requires search parameters" in outcome["issue"][0]["diagnostics"]

    def test_conditional_delete_unsupported_type(self, client):
        """Test conditional delete with unsupported type returns 400."""
        response = client.delete("/UnsupportedType?code=test")

        assert response.status_code == 400
        outcome = response.json()
        assert "not supported" in outcome["issue"][0]["diagnostics"]

    def test_conditional_delete_single_resource(self, client):
        """Test conditional delete removes exactly one matched resource."""
        # Create a patient with unique identifier
        create_response = client.post(
            "/Patient",
            json={
                "resourceType": "Patient",
                "identifier": [{"system": "test", "value": "single-delete-test"}],
                "name": [{"family": "ToDelete"}],
            },
        )
        patient_id = create_response.json()["id"]

        # Delete by identifier
        response = client.delete("/Patient?identifier=test|single-delete-test")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/Patient/{patient_id}")
        assert get_response.status_code == 404


class TestConditionalReadUtilities:
    """Tests for conditional read utility functions."""

    def test_parse_etag_weak(self):
        """Test parsing weak ETag."""
        assert parse_etag('W/"2"') == "2"
        assert parse_etag('W/"123"') == "123"

    def test_parse_etag_strong(self):
        """Test parsing strong ETag."""
        assert parse_etag('"2"') == "2"
        assert parse_etag('"abc"') == "abc"

    def test_parse_etag_with_spaces(self):
        """Test parsing ETag with whitespace."""
        assert parse_etag('  W/"2"  ') == "2"

    def test_parse_if_none_match_single(self):
        """Test parsing single ETag."""
        assert parse_if_none_match('W/"2"') == ["2"]

    def test_parse_if_none_match_multiple(self):
        """Test parsing multiple ETags."""
        result = parse_if_none_match('W/"1", W/"2", W/"3"')
        assert result == ["1", "2", "3"]

    def test_parse_if_none_match_wildcard(self):
        """Test parsing wildcard."""
        assert parse_if_none_match("*") == ["*"]

    def test_parse_if_modified_since_valid(self):
        """Test parsing valid HTTP date."""
        result = parse_if_modified_since("Tue, 15 Nov 2024 12:30:45 GMT")
        assert result is not None
        assert result.year == 2024
        assert result.month == 11
        assert result.day == 15

    def test_parse_if_modified_since_invalid(self):
        """Test parsing invalid date returns None."""
        assert parse_if_modified_since("invalid-date") is None
        assert parse_if_modified_since("") is None

    def test_etag_matches_exact(self):
        """Test ETag exact match."""
        assert etag_matches("2", ["2"]) is True
        assert etag_matches("2", ["1", "2", "3"]) is True

    def test_etag_matches_no_match(self):
        """Test ETag no match."""
        assert etag_matches("2", ["1", "3"]) is False

    def test_etag_matches_wildcard(self):
        """Test ETag wildcard match."""
        assert etag_matches("2", ["*"]) is True
        assert etag_matches("anything", ["*"]) is True

    def test_parse_last_updated_iso(self):
        """Test parsing ISO 8601 datetime."""
        result = parse_last_updated("2024-11-15T12:30:45+00:00")
        assert result is not None
        assert result.year == 2024

    def test_parse_last_updated_z_suffix(self):
        """Test parsing datetime with Z suffix."""
        result = parse_last_updated("2024-11-15T12:30:45Z")
        assert result is not None
        assert result.tzinfo is not None

    def test_is_modified_since_true(self):
        """Test resource modified after date."""
        # Resource updated today
        now = datetime.now(timezone.utc)
        last_updated = now.isoformat()
        # Check against yesterday
        yesterday = now - timedelta(days=1)
        assert is_modified_since(last_updated, yesterday) is True

    def test_is_modified_since_false(self):
        """Test resource not modified after date."""
        # Resource updated yesterday
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        last_updated = yesterday.isoformat()
        # Check against today
        today = datetime.now(timezone.utc)
        assert is_modified_since(last_updated, today) is False

    def test_check_conditional_read_etag_match(self):
        """Test check_conditional_read with matching ETag."""
        resource = {"meta": {"versionId": "2", "lastUpdated": "2024-01-01T00:00:00Z"}}
        assert check_conditional_read(resource, 'W/"2"', None) is True

    def test_check_conditional_read_etag_no_match(self):
        """Test check_conditional_read with non-matching ETag."""
        resource = {"meta": {"versionId": "2", "lastUpdated": "2024-01-01T00:00:00Z"}}
        assert check_conditional_read(resource, 'W/"1"', None) is False

    def test_check_conditional_read_not_modified(self):
        """Test check_conditional_read with If-Modified-Since."""
        # Resource from yesterday
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        resource = {"meta": {"versionId": "1", "lastUpdated": yesterday.isoformat()}}
        # Check with today's date - should return True (not modified)
        today = datetime.now(timezone.utc)
        if_modified_since = today.strftime("%a, %d %b %Y %H:%M:%S GMT")
        assert check_conditional_read(resource, None, if_modified_since) is True


class TestConditionalReadEndpoint:
    """Tests for conditional read HTTP endpoint."""

    def test_read_with_matching_etag_returns_304(self, client):
        """Test read with matching If-None-Match returns 304."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "ConditionalRead"}]},
        )
        assert create_response.status_code == 201
        patient = create_response.json()
        patient_id = patient["id"]
        etag = create_response.headers.get("ETag")

        # Read with matching ETag
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-None-Match": etag},
        )

        assert response.status_code == 304
        assert response.content == b""  # No body
        assert "ETag" in response.headers

    def test_read_with_non_matching_etag_returns_200(self, client):
        """Test read with non-matching If-None-Match returns 200."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "ConditionalRead2"}]},
        )
        patient_id = create_response.json()["id"]

        # Read with non-matching ETag
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-None-Match": 'W/"999"'},
        )

        assert response.status_code == 200
        assert response.json()["resourceType"] == "Patient"

    def test_read_with_wildcard_etag_returns_304(self, client):
        """Test read with If-None-Match: * returns 304 if resource exists."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "WildcardTest"}]},
        )
        patient_id = create_response.json()["id"]

        # Read with wildcard
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-None-Match": "*"},
        )

        assert response.status_code == 304

    def test_read_with_old_if_modified_since_returns_200(self, client):
        """Test read with old If-Modified-Since returns 200."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "ModifiedTest"}]},
        )
        patient_id = create_response.json()["id"]

        # Read with old date (resource was modified after this)
        old_date = "Tue, 01 Jan 2020 00:00:00 GMT"
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-Modified-Since": old_date},
        )

        assert response.status_code == 200
        assert response.json()["resourceType"] == "Patient"

    def test_read_with_future_if_modified_since_returns_304(self, client):
        """Test read with future If-Modified-Since returns 304."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "FutureTest"}]},
        )
        patient_id = create_response.json()["id"]

        # Read with future date (resource not modified after this)
        future_date = "Tue, 01 Jan 2030 00:00:00 GMT"
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-Modified-Since": future_date},
        )

        assert response.status_code == 304

    def test_read_without_conditional_headers_returns_200(self, client):
        """Test normal read without conditional headers returns 200."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "NormalRead"}]},
        )
        patient_id = create_response.json()["id"]

        # Normal read
        response = client.get(f"/Patient/{patient_id}")

        assert response.status_code == 200
        assert "ETag" in response.headers

    def test_read_nonexistent_resource_returns_404(self, client):
        """Test read of nonexistent resource returns 404, not 304."""
        response = client.get(
            "/Patient/nonexistent-id",
            headers={"If-None-Match": "*"},
        )

        assert response.status_code == 404

    def test_read_multiple_etags_match(self, client):
        """Test read with multiple ETags where one matches."""
        # Create a patient
        create_response = client.post(
            "/Patient",
            json={"resourceType": "Patient", "name": [{"family": "MultiETag"}]},
        )
        patient_id = create_response.json()["id"]

        # Read with multiple ETags including the correct one
        response = client.get(
            f"/Patient/{patient_id}",
            headers={"If-None-Match": 'W/"99", W/"1", W/"100"'},
        )

        assert response.status_code == 304
