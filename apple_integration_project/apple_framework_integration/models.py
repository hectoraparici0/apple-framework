"""Models for the app."""
from django.db import models
# /mnt/data/apple_integration_project/apple_framework_integration/models.py
from django.db import models

class CVE(models.Model):
    cve_id = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    exploit_path = models.CharField(max_length=255, blank=True, null=True)
    dependencies = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cve_id
