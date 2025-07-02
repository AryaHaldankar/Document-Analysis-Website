from django.db import models

class Users(models.Model):
    user_id = models.CharField(max_length=500, primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Documents(models.Model):
    user_id = models.ForeignKey(Users, on_delete = models.CASCADE)
    doc_id = models.CharField(max_length=500, primary_key=True)
    collection_id = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)