# Create your models here.
from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DONE', 'Done'),
        ('ERROR', 'Error'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    extracted_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.file_name} | Owner: {self.owner.username}"

auditlog.register(Document)