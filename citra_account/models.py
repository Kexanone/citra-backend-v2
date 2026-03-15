import binascii
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pathlib import Path
from secrets import token_urlsafe

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import models

from .storages import OverwriteStorage

avatar_storage = OverwriteStorage(
    location=settings.MEDIA_ROOT / 'avatars', base_url='/account/avatars/'
)


def get_avatar_upload_path(instance, filename):
    return f'{instance.user.username}.png'


class Account(models.Model):
    """
    Stores additional data for a user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=get_avatar_upload_path,
        blank=True,
        null=True,
        storage=avatar_storage,
    )
    token = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username

    @property
    def avatar_url(self):
        """
        Get URL for avatar
        """
        return f'/account/avatars/{self.avatar.name}'

    def save(self, *args, **kwargs):
        """
        Delete avatar file when avatar gets deleted from DB
        """
        if not self.avatar:
            self.delete_old_avatar_file()

        return super().save(*args, **kwargs)

    def delete_old_avatar_file(self):
        """
        Delete avatar file based on the path in the DB
        """
        try:
            old_self = Account.objects.get(pk=self.id)
        except Account.DoesNotExist:
            return

        if not old_self.avatar:
            return

        avatar_path = Path(old_self.avatar.path)
        avatar_path.unlink(missing_ok=True)


def generate_token(user):
    """
    Generates a new API token for user
    """
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        return

    token = token_urlsafe(32)
    account.token = make_password(token)
    account.save()
    prefixed_token = f'{user.username}:{token}'.encode('utf-8')
    prefixed_token = urlsafe_b64encode(prefixed_token)
    # Remove padding
    prefixed_token = prefixed_token.rstrip(b'=')
    return prefixed_token.decode('utf-8')


def get_user_from_token(prefixed_token):
    """
    Returns user from API token or None on failure
    """
    prefixed_token = prefixed_token.encode('utf-8')
    # Add max possible patting
    prefixed_token += b'=='

    try:
        prefixed_token = urlsafe_b64decode(prefixed_token).decode('utf-8')
    except (binascii.Error, UnicodeDecodeError):
        return

    try:
        (username, token) = prefixed_token.split(':', maxsplit=1)
    except ValueError:
        return

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return

    if check_password(token, user.account.token):
        return user

    return
