from django.urls import path
from .views import CategoryCreateAPIView, CategoryListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateAPIView.as_view(), name='category_create'),
]
