from django.db import models
from common.models import TimeStampedModel
from users.models import User

class Association(TimeStampedModel):
    """Model representing artisan associations.
    
    Each association has an admin user and can have multiple artisans.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo_url = models.URLField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='managed_association')

    def __str__(self):
        return self.name
    
class Artisan(models.Model):
    """Model representing individual artisans.
    
    Artisans can be independent or belong to an association.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'artisan'})
    association = models.ForeignKey(Association, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.name
