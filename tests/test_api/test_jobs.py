import pytest
from unittest.mock import patch


def test_create_job(client, sample_job_data):
    # Mock the embedding service to avoid API calls
    with patch("src.resume_matcher.services.job_service.get_embedding") as mock_embed:
        mock_embed.return_value = [0.1] * 1536

        response = client.post("/api/v1/jobs/", json=sample_job_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_job_data["title"]
        assert data["company"] == sample_job_data["company"]
        assert "id" in data


def test_create_job_validation_error(client):
    # Missing required fields
    response = client.post("/api/v1/jobs/", json={"title": "Test"})
    assert response.status_code == 422


def test_list_jobs_empty(client):
    response = client.get("/api/v1/jobs/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_jobs(client, sample_job_data):
    with patch("src.resume_matcher.services.job_service.get_embedding") as mock_embed:
        mock_embed.return_value = [0.1] * 1536

        # Create a job
        client.post("/api/v1/jobs/", json=sample_job_data)

        # List jobs
        response = client.get("/api/v1/jobs/")
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_get_job_not_found(client):
    response = client.get("/api/v1/jobs/999")
    assert response.status_code == 404


def test_delete_job(client, sample_job_data):
    with patch("src.resume_matcher.services.job_service.get_embedding") as mock_embed:
        mock_embed.return_value = [0.1] * 1536

        # Create a job
        create_response = client.post("/api/v1/jobs/", json=sample_job_data)
        job_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 404