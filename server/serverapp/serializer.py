from rest_framework import serializers
from .models import Sessions

class UsersSerializer(serializers.ModelSerializer):
    class meta:
        model = Sessions
        fields = '__all__'

class DocumentsSerializer(serializers.ModelSerializer):
    class meta:
        model = Sessions
        fields = '__all__'