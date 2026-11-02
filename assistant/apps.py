from django.apps import AppConfig
class AssistantConfig(AppConfig):
 default_auto_field='django.db.models.BigAutoField'; name='assistant'
 def ready(self):
  from django.contrib.auth.models import User
  from django.db.models.signals import post_save
  from .models import AuditLog
  # Role is stored in the lightweight user profile created by seed_demo.
