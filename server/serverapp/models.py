from django.db import models

class Documents(models.Model):
    doc_id = models.CharField(max_length=500, primary_key=True)
    collection_id = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)