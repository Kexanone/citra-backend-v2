from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account, generate_token
from pathlib import Path

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    '''
    Create an account when a user is created
    '''
    if created:
        Account.objects.create(user=instance)
        generate_token(instance)

@receiver(post_delete, sender=Account)
def delete_account_avatar(sender, instance, **kwargs):
    '''
    Delete avatar when account gets deleted
    '''
    if not instance.avatar:
        return

    avatar_path = Path(instance.avatar.path)
    avatar_path.unlink(missing_ok=True)
