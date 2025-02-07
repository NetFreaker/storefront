from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from apps.services.models import Category
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class AdminLoginView(LoginView):
    """Admin Login Page"""
    template_name = "admin_panel/login.html"

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')  # Redirect after login
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensures only superusers can access"""
    def test_func(self):
        return self.request.user.is_superuser

@method_decorator(login_required, name="dispatch")
class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "admin_panel/dashboard.html"

    def test_func(self):
        """Allow only staff and superusers"""
        return self.request.user.is_staff or self.request.user.is_superuser

class AdminProfileView(AdminRequiredMixin, UpdateView):
    """Admin Profile Update"""
    # form_class = ProfileUpdateForm
    template_name = "admin_panel/profile.html"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('admin_dashboard')

class AdminCategoryListView(AdminRequiredMixin, ListView):
    """Admin Panel - List Categories"""
    model = Category
    template_name = "admin_panel/categories.html"
    context_object_name = "categories"

class AdminCategoryCreateView(AdminRequiredMixin, CreateView):
    """Admin Panel - Create Category"""
    model = Category
    form_class = CategoryForm
    template_name = "admin_panel/category_form.html"

    def form_valid(self, form):
        form.save()
        return redirect('admin_categories')

class AdminLogoutView(AdminRequiredMixin, TemplateView):
    """Logout Admin"""
    def get(self, request):
        logout(request)
        return redirect('admin_login')  # Redirect to admin login page
