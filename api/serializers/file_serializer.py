from rest_framework import serializers
from api.models import  File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'size', 'path', 'folder', 'user', 'created_at']
