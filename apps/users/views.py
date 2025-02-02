# apps/users/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Set default role to 'customer' during signup
        role = self.request.data.get('role', 'customer')
        serializer.save(role=role)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
