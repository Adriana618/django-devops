import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_upload_document_success(mocker):
    """
    Test that an authenticated user can upload a PDF
    successfully (mocking S3 upload).
    """
    mock_upload = mocker.patch("documents.services.upload_file_to_s3")
    mock_upload.return_value = "some_s3_key"

    User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()

    token_response = client.post(
        "/api/token/",
        {"username": "testuser", "password": "testpass"},
        format="json",
    )
    assert token_response.status_code == 200

    access_token = token_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    url = reverse("document-upload")
    with open("documents/tests/resources/dummy.pdf", "rb") as f:
        response = client.post(url, {"file": f}, format="multipart")

    assert response.status_code == 201
    assert "document_id" in response.data

    mock_upload.assert_called_once()


@pytest.mark.django_db
def test_upload_document_unauthenticated():
    """
    Test that an unauthenticated user cannot upload a document.
    """
    client = APIClient()
    url = reverse("document-upload")

    with open("documents/tests/resources/dummy.pdf", "rb") as f:
        response = client.post(url, {"file": f}, format="multipart")

    assert response.status_code == 401  # Unauthorized
