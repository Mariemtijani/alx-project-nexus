# core/admin.py or a custom admin setup file
from django.contrib.admin.models import LogEntry
from django.conf import settings

LogEntry._meta.get_field('user').remote_field.model = settings.AUTH_USER_MODEL
