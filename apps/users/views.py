from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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
    
class CustomTokenRefreshView(RefreshToken):
    """Custom Token Refresh view to return both refresh and access tokens."""
    
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    @csrf_exempt  # Disable CSRF for this specific view
    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated before proceeding
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Call the original TokenRefreshView to validate and refresh the token
        response = super().post(request, *args, **kwargs)
        
        # Retrieve the refresh token from the request data
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                # Create a new refresh token using the given refresh token
                refresh = RefreshToken(refresh_token)

                # Generate a new access token from the refresh token
                access_token = refresh.access_token

                # Return both the new refresh token and access token in the response
                return Response({
                    'access_token': str(access_token),
                    'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If no refresh token is provided, use the default response
        return response

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