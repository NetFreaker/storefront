from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer

class CategoryCreateAPIView(generics.CreateAPIView):
    """API for creating categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryListAPIView(generics.ListAPIView):
    """API for listing all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
