from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('profile/', views.UpdateProfileView.as_view(), name='update_profile'),
]