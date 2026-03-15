from pathlib import Path

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Account, generate_token


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """
    Create an account when a user is created
    """
    if created:
        Account.objects.create(user=instance)
        generate_token(instance)


@receiver(post_delete, sender=Account)
def delete_account_avatar(sender, instance, **kwargs):
    """
    Delete avatar when account gets deleted
    """
    if not instance.avatar:
        return

    avatar_path = Path(instance.avatar.path)
    avatar_path.unlink(missing_ok=True)
