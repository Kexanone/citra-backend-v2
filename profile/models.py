from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .storages import OverwriteStorage
from pathlib import Path

def get_avatar_upload_path(instance, filename):
    return Path('avatars') / f'{instance.user.id}.png'

class Profile(models.Model):
    '''
    Stores additional data for a user
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_upload_path, blank=True, null=True, storage=OverwriteStorage)

    def __str__(self):
        return self.user.username
    
    @property
    def avatar_url(self):
        '''
        Get URL for avatar
        '''
        return f'/{__package__}/{self.avatar.name}'
