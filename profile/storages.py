from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pathlib import Path

class OverwriteStorage(FileSystemStorage):
    '''
    Same as FileSystemStorage, but overrides files
    with the same name instead of renaming them
    '''
    def get_available_name(self, name, max_length):
        if self.exists(name):
            old_file = Path(settings.MEDIA_ROOT) / name
            old_file.unlink()
        return super().get_available_name(name, max_length)
