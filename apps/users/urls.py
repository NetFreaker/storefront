from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),  # User registration
    path('login/', views.LoginView.as_view(), name='login'),     # Handles JWT authentication # We can handle default TokenObtainPairView, we also have custom loginview
    path('logout/', views.LogoutView.as_view(), name='logout'),  # User logout (blacklist token)
    path('profile/', views.ProfileView.as_view(), name='profile_update'), # Retrieve and Update
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),  # Handled by SimpleJWT
]