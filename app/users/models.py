from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from common.models import TimeStampedModel
from typing import Optional

class UserManager(BaseUserManager):
    """Custom user manager for handling user creation."""
    
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> 'User':
        """Create and return a regular user with email and password."""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, TimeStampedModel):
    """Custom user model for the artisan platform.
    
    Supports multiple user roles: platform_admin, association_admin, artisan, buyer.
    Uses email as the unique identifier instead of username.
    """
    USERNAME_FIELD = 'email'
    
    ROLE_CHOICES = [
        ('platform_admin', 'Platform Admin'),
        ('association_admin', 'Association Admin'),
        ('artisan', 'Artisan'),
        ('buyer', 'Buyer'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_picture = models.URLField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def has_perm(self, perm: str, obj=None) -> bool:
        """Check if user has specific permission."""
        return self.is_superuser

    def has_module_perms(self, app_label: str) -> bool:
        """Check if user has permissions for app module."""
        return self.is_superuser

    def get_username(self) -> str:
        """Return email as username."""
        return self.email

    def __str__(self):
        return self.name
