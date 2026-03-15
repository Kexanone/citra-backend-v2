from pathlib import Path

from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """
    Same as FileSystemStorage, but overrides files
    with the same name instead of renaming them
    """

    def get_available_name(self, name, max_length):
        if self.exists(name):
            old_file = Path(self.path(name))
            old_file.unlink()

        return super().get_available_name(name, max_length)
