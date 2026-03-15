from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.forms import ModelForm
from PIL import Image

from .models import Account


class ChangeAvatarForm(ModelForm):
    """
    Form for changing the account's avatar
    """

    class Meta:
        model = Account
        fields = ['avatar']
        labels = {'avatar': ''}

    def clean_avatar(self):
        """
        Enforce maximum image size and convert to png
        """
        avatar = self.cleaned_data['avatar']
        if not avatar:
            return False

        with Image.open(avatar) as image:
            width, height = image.size

            if (
                width > settings.MAX_AVATAR_IMAGE_SIZE
                or height > settings.MAX_AVATAR_IMAGE_SIZE
            ):
                image.thumbnail(
                    (
                        settings.MAX_AVATAR_IMAGE_SIZE,
                        settings.MAX_AVATAR_IMAGE_SIZE,
                    ),
                    Image.LANCZOS,
                )

            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            buffer = BytesIO()
            image.save(buffer, format='png')
            buffer.seek(0)

        name = Path(avatar.name).with_suffix('.png')
        return ContentFile(buffer.read(), name=name)


class DeleteUserForm(ModelForm):
    class Meta:
        model = User
        exclude = []
