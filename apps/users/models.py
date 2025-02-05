from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Custom user manager to handle user creation
class CustomUserManager(BaseUserManager):
    """
    Custom manager to handle user creation logic.
    """
    def create_user(self, email, first_name, last_name, password=None, role=None):
        """
        Create and return a regular user with an email, first_name, last_name, and optional role.

        Args:
            email (str): The user's email address.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            password (str): The user's password.
            role (str): The role of the user. Defaults to 'customer'.
        
        Returns:
            user (CustomUser): The created user instance.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('Email address is mandatory!')
        
        # Normalize email to ensure it's in lowercase format
        email = self.normalize_email(email)

        # Create user instance and set password
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save user in the database
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Create and return a superuser with email, first_name, last_name, and password.

        Args:
            email (str): The superuser's email address.
            first_name (str): The superuser's first name.
            last_name (str): The superuser's last name.
            password (str): The superuser's password.

        Returns:
            user (CustomUser): The created superuser instance.
        """
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True  # Grant superuser admin privileges
        user.is_superuser = True  # Grant superuser privileges
        user.save(using=self._db)
        return user


# Custom User model to replace the default Django User model
class CustomUser(AbstractBaseUser):
    """
    Custom User model that extends AbstractBaseUser to support authentication using email 
    instead of the default username. It also includes custom fields like first_name, last_name, and role.
    """
    
    # Define choices for user roles
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('service_provider', 'Service Provider'),
        ('admin', 'Admin')
    )

    # Define model fields
    email = models.EmailField(unique=True)  # Unique email for user identification
    first_name = models.CharField(max_length=30)  # User's first name
    last_name = models.CharField(max_length=30)  # User's last name
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')  # User role
    is_active = models.BooleanField(default=True)  # Is the user active (can log in)
    is_staff = models.BooleanField(default=False)  # Can the user access the admin panel
    date_joined = models.DateTimeField(auto_now_add=True)  # Date when the user was created

    # Custom user manager
    objects = CustomUserManager()

    # Set the email field as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    
    # Fields that are required for creating a user, apart from email
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """
        Return the string representation of the user instance (email).
        """
        return self.email

    def get_full_name(self):
        """
        Return the user's full name by concatenating first name and last name.
        
        Returns:
            str: Full name of the user.
        """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """
        Return the user's first name (useful for admin interfaces).
        
        Returns:
            str: First name of the user.
        """
        return self.first_name
