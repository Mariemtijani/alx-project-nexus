from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import TimeStampedModel
from associations.models import Association, Artisan
from users.models import User
import uuid

class Category(models.Model):
    """Product category model for organizing products."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    """Product model with polymorphic ownership.
    
    Products can be owned by either artisans or associations.
    Supports multilingual content through ProductTranslation.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    OWNER_TYPE_CHOICES = [('artisan', 'Artisan'), ('association', 'Association')]
    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE_CHOICES)
    owner_id = models.UUIDField()  # Polymorphic reference to artisan or association
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

class ProductTranslation(models.Model):
    """Multilingual translations for products."""
    product = models.ForeignKey(Product, related_name='translations', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()

class ProductImage(models.Model):
    """Product image storage model."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

# Import models from separate files so Django can detect them
from .favorite_model import Favorite
from .review_model import Review

# class Favorite(TimeStampedModel):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('buyer', 'product')

#     def __str__(self):
#         return f"{self.buyer.name} - {self.product.title}"

# class Review(TimeStampedModel):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField(null=True, blank=True)

#     class Meta:
#         unique_together = ('buyer', 'product')

#     def __str__(self):
#         return f"{self.buyer.name} - {self.product.title} ({self.rating}/5)"
