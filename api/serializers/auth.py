from rest_framework import serializers
from api.models import User

class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True, error_messages={"required": "Username is required."})
    email = serializers.EmailField(required=True, error_messages={"required": "Email is required."})
    password = serializers.CharField(write_only=True, min_length=6, required=True, error_messages={
        "required": "Password is required.",
        "min_length": "Password must be at least 6 characters long."
    })
    name = serializers.CharField(max_length=150, required=True, error_messages={"required": "Name is required."})

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True, error_messages={"required": "Username is required."})
    password = serializers.CharField(write_only=True, min_length=6, required=True, error_messages={
        "required": "Password is required.",
        "min_length": "Password must be at least 6 characters long."
    })
