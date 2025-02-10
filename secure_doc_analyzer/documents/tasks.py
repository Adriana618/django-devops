import io
import boto3
from celery import shared_task
from django.conf import settings
from .models import Document
import logging

@shared_task
def process_document_textract(document_id):
    """
    This task downloads the file from S3, processes it with AWS Textract, 
    and updates the Document model with extracted text.
    """
    try:
        doc = Document.objects.get(id=document_id)
        doc.status = 'PROCESSING'
        doc.save()

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        file_buffer = io.BytesIO()
        result = s3_client.download_fileobj(settings.AWS_S3_BUCKET, doc.s3_key, file_buffer)
        file_buffer.seek(0)

        textract_client = boto3.client(
            'textract',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        response = textract_client.detect_document_text(
            Document={'Bytes': file_buffer.read()}
        )

        lines = []
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                lines.append(block['Text'])

        extracted_text = "\n".join(lines)
        doc.extracted_text = extracted_text
        doc.status = 'DONE'
        doc.save()

    except Document.DoesNotExist:
        pass
    except Exception as e:
        doc.status = 'ERROR'
        doc.save()
        logging.error(e)
