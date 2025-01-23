from rest_framework import serializers

class UpdateUserInfoRequestSerializer(serializers.Serializer):
    # Define the fields that can be updated
    name = serializers.CharField(required=False, max_length=100)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True, min_length=6)
    newpassword = serializers.CharField(required=False, write_only=True, min_length=6)
    image = serializers.ImageField(required=False)

    def validate(self, data):
        # Add custom validation if necessary
        if 'password' in data and not 'newpassword' in data:
            raise serializers.ValidationError("You must provide a new password if updating the password.")
        return data
