import pytest
import io
from unittest.mock import patch


def test_upload_resume_invalid_file_type(client):
    # Create a fake non-PDF file
    files = {
        "file": ("test.txt", io.BytesIO(b"not a pdf"), "text/plain")
    }
    data = {"name": "John Doe"}

    response = client.post("/api/v1/resumes/upload", files=files, data=data)
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_list_resumes_empty(client):
    response = client.get("/api/v1/resumes/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_resume_not_found(client):
    response = client.get("/api/v1/resumes/999")
    assert response.status_code == 404