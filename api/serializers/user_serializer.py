from rest_framework import serializers

from api.models import User

class UpdateUserInfoRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True, min_length=6)
    newpassword = serializers.CharField(required=False, write_only=True, min_length=6)
    image = serializers.ImageField(required=False)

    def validate(self, data):
        if 'password' in data and 'newpassword' not in data:
            raise serializers.ValidationError("You must provide a new password if updating the password.")
        return data


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ['password'] 

#     def to_representation(self, instance):
#         print("Serialized data:", instance)  # Debugging the instance data
#         return super().to_representation(instance)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        print("Serialized data:", User)  
        fields = ['id', 'username', 'email', 'name', 'image', 'fcm_token', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        print("Serialized data:", instance)  # Debugging the instance data
        return super().to_representation(instance)