from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

# Serializer for user registration (Signup)
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # Ensure password is not exposed in API responses
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
    
    def validate_email(self, value):
        """Ensure email is unique."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    # Create user with hashed password
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# Serializer for user login (returns JWT tokens)
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh_token': str(refresh),        # Refresh token (used to get new access token)
                'access_token': str(refresh.access_token), # Access token (used for authentication)
                'role': user.role,              # User role (customer/provider/admin)
                'email': user.email
            }
        raise serializers.ValidationError("Invalid email or password")
