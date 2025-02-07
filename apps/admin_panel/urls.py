from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('categories/', views.AdminCategoryListView.as_view(), name='admin_categories'),
    path('categories/create/', views.AdminCategoryCreateView.as_view(), name='admin_create_category'),
    path('logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
]
