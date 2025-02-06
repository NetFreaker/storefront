from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView

class AdminLoginView(LoginView):
    """Admin login view."""
    template_name = 'admin_panel/login.html'
    redirect_authenticated_user = True  # Redirect to dashboard if already logged in

    def get(self, *args, **kwargs):
        print(f"Template directories: {settings.TEMPLATES[0]['DIRS']}")
        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')  # Redirect to dashboard after login

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get total counts of Users, Services, and Categories
        context['total_users'] = User.objects.count()
        context['total_services'] = Service.objects.count()
        context['total_categories'] = Category.objects.count()
        
        return context
    
def admin_logout(request):
    """Logs out the admin and redirects to the login page."""
    logout(request)
    return redirect('admin_login')

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to admin users only."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        return render(self.request, 'admin_panel/403.html', status=403)

class CreateCategoryView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Admin view to create categories."""
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/create_category.html'
    success_url = reverse_lazy('admin_dashboard')  # Redirect to dashboard after success

    def form_valid(self, form):
        """Override to handle custom validation."""
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating the admin profile."""
    model = User
    form_class = ProfileForm
    template_name = 'admin_panel/update_profile.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_object(self):
        return self.request.user  # Ensure the user is editing their own profile
    
    def test_func(self):
        return self.request.user.is_staff  # Ensure only admin users can edit