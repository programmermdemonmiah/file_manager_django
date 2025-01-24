from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.utils.timezone import now
from api.models import File, Folder
from api.serializers import  FolderSerializer

class FolderCreateView(View):
    def post(self, request, *args, **kwargs):
        # Create a folder
        name = request.data.get("name")
        user = request.user  # assuming user is logged in
        
        # Optional parent folder to create subfolders
        parent_folder_id = request.data.get("parent_folder_id")
        parent_folder = None
        if parent_folder_id:
            parent_folder = Folder.objects.get(id=parent_folder_id)
        
        folder = Folder.objects.create(
            name=name, user=user, parent_folder=parent_folder
        )
        
        return JsonResponse({
            "message": "Folder created successfully!",
            "folder": FolderSerializer(folder).data
        }, status=201)




class MoveFolderView(View):
    def post(self, request, *args, **kwargs):
        # Move a folder (along with its subfolders and files) to another folder
        folder_id = request.data.get("folder_id")
        new_parent_folder_id = request.data.get("new_parent_folder_id")
        
        folder = Folder.objects.get(id=folder_id)
        new_parent_folder = Folder.objects.get(id=new_parent_folder_id)
        
        # Update folder's parent
        folder.parent_folder = new_parent_folder
        folder.save()

        # Also move all files inside this folder
        files_in_folder = File.objects.filter(folder=folder)
        for file in files_in_folder:
            file.folder = new_parent_folder  # Update file's folder if needed
            file.save()
        
        return JsonResponse({
            "message": "Folder moved successfully!",
            "folder": FolderSerializer(folder).data
        }, status=200)


class SubFolderCreateView(View):
    def post(self, request, *args, **kwargs):
        # Create a subfolder under a folder
        name = request.data.get("name")
        parent_folder_id = request.data.get("parent_folder_id")
        user = request.user  # assuming user is logged in
        
        parent_folder = Folder.objects.get(id=parent_folder_id)
        
        subfolder = Folder.objects.create(
            name=name, user=user, parent_folder=parent_folder
        )
        
        return JsonResponse({
            "message": "Subfolder created successfully!",
            "subfolder": FolderSerializer(subfolder).data
        }, status=201)



class FolderDetailView(View):
    def get(self, request, *args, **kwargs):
        # Get folder details and its subfolders
        folder_id = request.GET.get("folder_id")
        folder = Folder.objects.get(id=folder_id)
        
        subfolders = Folder.objects.filter(parent_folder=folder)
        
        return JsonResponse({
            "message": "Folder details fetched successfully!",
            "folder": FolderSerializer(folder).data,
            "subfolders": FolderSerializer(subfolders, many=True).data
        }, status=200)
