from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views import View
from django.shortcuts import get_object_or_404
from api.models import User
from api.serializers import UpdateUserInfoRequestSerializer
import os

IMAGE_UPLOAD_DIR = "media/profile_images/"

class UserView(View):

    @staticmethod
    def get_user_info(request):
        try:
            user_id = request.GET.get('id')
            user = get_object_or_404(User, id=user_id)

            user_dict = user.__dict__
            user_dict.pop("password", None)  # Exclude hashed_password field
            
            return JsonResponse(user_dict, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    @staticmethod
    def update_user_info(request):
        try:
            if request.method != "POST":
                return JsonResponse({"error": "Invalid HTTP method"}, status=405)

            token = request.user  # Assuming you use Django's authentication middleware
            user = get_object_or_404(User, id=token.id)

            data = request.POST.dict()
            serializer = UpdateUserInfoRequestSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse(serializer.errors, status=400)

            user_req = serializer.validated_data

            # Ensure at least one field to update is provided
            if not any(user_req.values()):
                return JsonResponse({"error": "Please provide at least one field to update"}, status=204)

            # Validate old password if updating password
            if 'password' in user_req or 'newpassword' in user_req:
                if not check_password(user_req.get('password'), user.password):
                    return JsonResponse({"error": "Your old password doesn't match"}, status=400)
                if 'newpassword' in user_req:
                    user.password = make_password(user_req.get('newpassword'))

            # Update email if provided
            if 'email' in user_req:
                if User.objects.filter(email=user_req.get('email')).exists():
                    return JsonResponse({"error": "This email is already in use"}, status=226)
                user.email = user_req.get('email')

            # Save the image if provided
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                image_filename = f"{user.id}_profile_image.jpg"
                image_path = os.path.join(IMAGE_UPLOAD_DIR, image_filename)
                default_storage.save(image_path, ContentFile(image_file.read()))
                user.image = image_path

            # Update name if provided
            if 'name' in user_req:
                user.name = user_req.get('name')

            user.save()

            user_dict = user.__dict__
            user_dict.pop("password", None)  # Exclude hashed_password field

            return JsonResponse({
                "message": "User information updated successfully",
                "user": user_dict
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
