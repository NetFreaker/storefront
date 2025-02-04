from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from .serializers import UserSignupSerializer, LoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer

# API for user signup (registration)
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
        role = self.request.data.get('role', 'customer')  # Default role = customer
        serializer.save(role=role)

# API for user login (returns JWT tokens)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for this specific view
class CustomTokenRefreshView(TokenRefreshView):
    """Custom Token Refresh view to return both refresh and access tokens."""

    def post(self, request, *args, **kwargs):
        # Retrieve the refresh token from the request data
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new refresh token using the given refresh token
            refresh = RefreshToken(refresh_token)

            # Generate a new access token from the refresh token
            access_token = refresh.access_token

            # Return both the new refresh token and access token in the response
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh)  # Provide new refresh token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
# API for user logout (Blacklists Refresh token)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # TODO: Lets discuss whether user should be loggedin or not required

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")  # Get token from request body
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)  # Convert to token object 
            token.blacklist()  # Blacklist the refresh token so it can't be used again
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
 
# API for user profile (Retrieve and Update)
class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve & Update User Profile API"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use different serializer based on the request method
        if self.request.method == 'GET':
            return UserProfileSerializer
        elif self.request.method == 'PUT':
            return UserProfileUpdateSerializer

    def get_object(self):
        # Return the logged-in user instance
        return self.request.user