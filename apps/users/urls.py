from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),  # User registration
    path('login/', views.LoginView.as_view(), name='login'),     # User login (JWT)
    path('logout/', views.LogoutView.as_view(), name='logout'),  # User logout (blacklist token)
]