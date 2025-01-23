from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from api.serializers import RegisterRequestSerializer, LoginRequestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Helper to generate JWT tokens
def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    }

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the email or username already exists
            if User.objects.filter(email=serializer.validated_data['email']).exists() or \
                    User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response(
                    {"error": "Email or username already registered."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Create the user
            user = User.objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=make_password(serializer.validated_data['password']),
                first_name=serializer.validated_data['name'],
            )
            user.save()
            tokens = generate_tokens_for_user(user)
            return Response({
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token'],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name,
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = " and ".join(serializer.errors.keys()) + " are required."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            # Combine all field errors into a single error message
            error_message = " and ".join(serializer.errors.keys()) + " are required."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Authenticate the user
            user = User.objects.filter(username=serializer.validated_data['username']).first()
            if not user or not check_password(serializer.validated_data['password'], user.password):
                raise AuthenticationFailed("Invalid credentials.")

            tokens = generate_tokens_for_user(user)
            return Response({
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token'],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name,
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
