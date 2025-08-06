from django.db import models
from common.models import TimeStampedModel
from associations.models import Association, Artisan
import uuid

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    OWNER_TYPE_CHOICES = [('artisan', 'Artisan'), ('association', 'Association')]
    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE_CHOICES)
    owner_id = models.UUIDField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

class ProductTranslation(models.Model):
    product = models.ForeignKey(Product, related_name='translations', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()
