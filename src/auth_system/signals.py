from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


@receiver(post_save, sender=User)
def handle_user_creation(sender, instance, created, **kwargs):
    """
    Handle user creation events
    """
    if created:
        # Additional logic can be added here when a new user is created
        pass