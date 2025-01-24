from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.utils.timezone import now
from api.models import File, Folder
from api.serializers import FileSerializer


class FileCreateView(View):
    def post(self, request, *args, **kwargs):
        # Create a file
        name = request.data.get("name")
        size = request.data.get("size")
        path = request.data.get("path")
        folder_id = request.data.get("folder_id")
        user = request.user  # assuming user is logged in
        
        # Get folder object
        folder = Folder.objects.get(id=folder_id)
        
        file = File.objects.create(
            name=name, size=size, path=path, folder=folder, user=user
        )
        
        return JsonResponse({
            "message": "File created successfully!",
            "file": FileSerializer(file).data
        }, status=201)


class MoveFileView(View):
    def post(self, request, *args, **kwargs):
        # Move a file to another folder
        file_id = request.data.get("file_id")
        new_folder_id = request.data.get("new_folder_id")
        
        file = File.objects.get(id=file_id)
        new_folder = Folder.objects.get(id=new_folder_id)
        
        # Update file's folder
        file.folder = new_folder
        file.save()
        
        return JsonResponse({
            "message": "File moved successfully!",
            "file": FileSerializer(file).data
        }, status=200)
    
class FileInFolderView(View):
    def get(self, request, *args, **kwargs):
        # Get files inside a specific folder
        folder_id = request.GET.get("folder_id")
        folder = Folder.objects.get(id=folder_id)
        
        files_in_folder = File.objects.filter(folder=folder)
        
        return JsonResponse({
            "message": "Files fetched successfully!",
            "files": FileSerializer(files_in_folder, many=True).data
        }, status=200)