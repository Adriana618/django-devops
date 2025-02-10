import pytest
from documents.models import Document
from documents.tasks import process_document_textract
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_process_document_textract(mocker):
    """
    Test that the task updates the Document status and extracted text.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    doc = Document.objects.create(
        owner=user, file_name="dummy.pdf", s3_key="dummy_key"
    )

    s3_mock = mocker.patch("documents.tasks.boto3.client")
    textract_mock = s3_mock.return_value

    textract_mock.detect_document_text.return_value = {
        "Blocks": [
            {"BlockType": "LINE", "Text": "Hello from Textract!"},
            {"BlockType": "LINE", "Text": "More lines here..."},
        ]
    }

    process_document_textract(doc.id)

    doc.refresh_from_db()
    assert doc.status == "DONE"
    assert "Hello from Textract!" in doc.extracted_text
