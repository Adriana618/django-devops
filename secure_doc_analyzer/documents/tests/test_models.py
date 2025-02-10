import pytest
from documents.models import Document
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_document_creation():
    """
    This test checks if a Document instance can be created successfully.
    """
    user = User.objects.create_user(username="testuser", password="pass123")

    doc = Document.objects.create(
        owner=user, file_name="example.pdf", s3_key="some_s3_key"
    )

    assert doc.owner == user
    assert doc.file_name == "example.pdf"
    assert doc.s3_key == "some_s3_key"
    assert doc.status == "PENDING"
    assert doc.extracted_text is None
