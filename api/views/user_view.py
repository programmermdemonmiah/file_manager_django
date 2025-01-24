from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.models import User
from api.serializers import UpdateUserInfoRequestSerializer, UserSerializer
import os
from file_manager import PROFILE_IMAGE_UPLOAD_DIR

class UserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures the user is authenticated

    def get(self, request):
        """Get user information."""
        try:
            user = request.user  
            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)
            
            serializer = UserSerializer(user)
            print(serializer.data)
            return JsonResponse(serializer.data, status=200, safe=False)
        
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    def post(self, request):
        """Update user information."""
        try:
            user = request.user  # Assuming authentication middleware is used
            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            data = request.data  # Use DRF's request.data to handle both JSON and form-data
            serializer = UpdateUserInfoRequestSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse(serializer.errors, status=400)

            user_req = serializer.validated_data

            # Ensure at least one field to update is provided
            if not any(user_req.values()):
                return JsonResponse({"error": "Please provide at least one field to update"}, status=400)

            # Validate old password if updating password
            if 'password' in user_req or 'newpassword' in user_req:
                if not check_password(user_req.get('password'), user.password):
                    return JsonResponse({"error": "Your old password doesn't match"}, status=400)
                if 'newpassword' in user_req:
                    user.password = make_password(user_req.get('newpassword'))

            # Update email if provided
            if 'email' in user_req:
                if User.objects.filter(email=user_req.get('email')).exists():
                    return JsonResponse({"error": "This email is already in use"}, status=400)
                user.email = user_req.get('email')

            # Save the image if provided
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                image_filename = f"{user.id}_profile_image.jpg"
                image_path = os.path.join(PROFILE_IMAGE_UPLOAD_DIR, image_filename)
                default_storage.save(image_path, ContentFile(image_file.read()))
                user.image = image_path

            # Update name if provided
            if 'name' in user_req:
                user.name = user_req.get('name')

            user.save()

            # Use a serializer to serialize updated user data
            user_serializer = UpdateUserInfoRequestSerializer(user)
            return JsonResponse({
                "message": "User information updated successfully",
                "user": user_serializer.data
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
