from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.forms import ModelForm
from PIL import Image

from .models import Profile

MAX_IMAGE_SIZE = 64


class ChangeAvatarForm(ModelForm):
    """
    Form for changing the profile's avatar
    """

    class Meta:
        model = Profile
        fields = ['avatar']

    def clean_avatar(self):
        """
        Enforces maximum image size and converts to png
        """
        avatar = self.cleaned_data['avatar']
        if not avatar:
            return False

        with Image.open(avatar) as image:
            width, height = image.size

            if width > MAX_IMAGE_SIZE or height > MAX_IMAGE_SIZE:
                image.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.LANCZOS)

            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            buffer = BytesIO()
            image.save(buffer, format='png')
            buffer.seek(0)

        name = Path(avatar.name).with_suffix('.png')
        return ContentFile(buffer.read(), name=name)
