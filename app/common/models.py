from django.db import models
import uuid

class TimeStampedModel(models.Model):
    """Abstract base model with UUID primary key and timestamps.
    
    Provides common fields for all models: id, created_at, updated_at.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
