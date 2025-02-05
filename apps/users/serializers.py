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
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user's profile (GET)"""
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']  # Fields to retrieve

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user's profile (PUT)"""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']  # Only allow updating first_name and last_name
    
    def update(self, instance, validated_data):
        # Only update the fields provided in the request
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
