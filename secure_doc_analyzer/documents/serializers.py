from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'owner',
            'file_name',
            'status',
            'extracted_text',
            'created_at'
        ]
        read_only_fields = ['owner', 'extracted_text']