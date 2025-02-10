"""
Celery app configuration file for secure_doc_analyzer project.
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure_doc_analyzer.settings")

app = Celery("secure_doc_analyzer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
