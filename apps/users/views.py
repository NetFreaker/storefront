from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.models import update_last_login
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from apps.users.authentication import JWTAuthenticationFromCookie
from .serializers import UserSignupSerializer, LoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer

class CSRFTokenView(APIView):
    """API to get CSRF token for frontend"""

    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow all users (even unauthenticated)

    def get(self, request):
        return Response({"csrf_token": get_token(request)})

# API for user signup (registration)
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
        role = self.request.data.get('role', 'customer')  # Default role = customer
        serializer.save(role=role)

# API for user login (returns JWT tokens)

class LoginView(APIView):
    """Login API that sets JWT in cookies"""

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Update last login
        update_last_login(None, user)

        # Prepare response
        response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)

        # Set HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.SECURE_COOKIE,  # Use True in production
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.SECURE_COOKIE,
            samesite="Lax",
        )

        # Set CSRF Token in response
        response.data["csrf_token"] = get_token(request)
        return response
    
# @method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for this specific view
# class CustomTokenRefreshView(TokenRefreshView):
#     """Custom Token Refresh view to return both refresh and access tokens."""

#     def post(self, request, *args, **kwargs):
#         # Retrieve the refresh token from the request data
#         refresh_token = request.data.get('refresh_token')

#         if not refresh_token:
#             return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Create a new refresh token using the given refresh token
#             refresh = RefreshToken(refresh_token)

#             # Generate a new access token from the refresh token
#             access_token = refresh.access_token

#             # Return both the new refresh token and access token in the response
#             return Response({
#                 'access_token': str(access_token),
#                 'refresh_token': str(refresh)  # Provide new refresh token
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
class CookieTokenRefreshView(TokenRefreshView):
    """Refresh access token using HTTP-only cookie"""

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token missing"}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({"message": "Token refreshed"})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=settings.DEBUG is False,
                samesite="Lax",
            )
            return response

        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=401)
        
# API for user logout (Blacklists Refresh token)
class LogoutView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]  # TODO: Lets discuss whether user should be loggedin or not required

    def post(self, request):
        try:
            # refresh_token = request.data.get("refresh_token")  # Get token from request body
            # if not refresh_token:
            #     return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # token = RefreshToken(refresh_token)  # Convert to token object 
            # token.blacklist()  # Blacklist the refresh token so it can't be used again
            response = Response({"message": "Logged out successfully"})  # JSON response
            response.delete_cookie("access_token")  # Remove access token
            response.delete_cookie("refresh_token")  # Remove refresh token
            return response  # Return response to client
        except Exception as e:
            print(e)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
 
# API for user profile (Retrieve and Update)
class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve & Update User Profile API"""
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthenticationFromCookie]

    def get_serializer_class(self):
        # Use different serializer based on the request method
        if self.request.method == 'GET':
            return UserProfileSerializer
        elif self.request.method == 'PUT':
            return UserProfileUpdateSerializer

    def get_object(self):
        # Return the logged-in user instance
        return self.request.user