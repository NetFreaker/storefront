from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from .serializers import UserSignupSerializer, LoginSerializer
from .models import CustomUser

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

# API for user logout (Blacklists Refresh token)
class LogoutView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # TODO: Lets discuss whether user should be loggedin or not required

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
