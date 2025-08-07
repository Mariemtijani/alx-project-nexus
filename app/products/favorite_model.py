from django.db import models
from common.models import TimeStampedModel
from users.models import User
from .models import Product

class Favorite(TimeStampedModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'buyer'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('buyer', 'product')

    def __str__(self):
        return f"{self.buyer.name} - {self.product.title}"