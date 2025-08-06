from django.db import models
from common.models import TimeStampedModel

class User(TimeStampedModel):
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

    def __str__(self):
        return self.name
