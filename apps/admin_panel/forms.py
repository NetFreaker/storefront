from django import forms
from .models import Category
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    """Form for updating admin profile."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """Validate email format."""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

class CategoryForm(forms.ModelForm):
    """Form for creating/updating categories."""
    class Meta:
        model = Category
        fields = ['name', 'description']

    def clean_name(self):
        """Ensure the category name is unique."""
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name
