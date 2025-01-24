from rest_framework import serializers
from api.models import Folder

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'user', 'parent_folder', 'created_at', 'updated_at']


