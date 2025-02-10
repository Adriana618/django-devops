from django.shortcuts import render

# Create your views here.
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Document
from .serializers import DocumentSerializer
from .services import upload_file_to_s3
from .tasks import process_document_textract
import logging
logger = logging.getLogger(__name__)

class DocumentUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    valid_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}
    max_size = 10 * 1024 * 1024
    allowed_mimetypes = {'application/pdf', 'image/jpeg', 'image/png', 'image/tiff'}
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        ext = os.path.splitext(file_obj.name)[1].lower()
        if not file_obj:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        if ext not in self.valid_extensions:
            return Response({"detail": "Unsupported file extension."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if file_obj.size > self.max_size:
            return Response({"detail": "File size exceeds 10MB limit."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if file_obj.content_type not in self.allowed_mimetypes:
            return Response({"detail": "Unsupported mimetype."}, status=400)

        generated_name = f"{uuid.uuid4()}_{file_obj.name}"

        s3_key = upload_file_to_s3(file_obj, generated_name)

        logger.info(f"User {request.user} uploaded file: {file_obj.name}")

        doc = Document.objects.create(
            owner=request.user,
            file_name=file_obj.name,
            s3_key=s3_key,
            status='PENDING' 
        )
        
        # TODO: En el siguiente paso llamaremos a la tarea asíncrona Celery/SQS para procesar
        process_document_textract.delay(doc.id)

        return Response({"detail": "File uploaded successfully", "document_id": doc.id}, 
                        status=status.HTTP_201_CREATED)


class DocumentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
