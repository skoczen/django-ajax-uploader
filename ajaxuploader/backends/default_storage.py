import datetime
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from ajaxuploader.backends.base import AbstractUploadBackend


class DefaultStorageUploadBackend(AbstractUploadBackend):
    """
    Uses Django's default storage backend to store the uploaded files
    see https://docs.djangoproject.com/en/dev/topics/files/#file-storage
    """

    UPLOAD_DIR = getattr(settings, "UPLOAD_DIR", "uploads")

    def _get_upload_dir(self):
        if callable(self.UPLOAD_DIR):
            return self.UPLOAD_DIR()
        return datetime.datetime.now().strftime(self.UPLOAD_DIR)

    def setup(self, filename, *args, **kwargs):
        # join UPLOAD_DIR with filename.
        new_path = os.path.join(self._get_upload_dir(), filename)

        # save empty file in default storage with path = new_path
        self.path = default_storage.save(new_path, ContentFile(''))

        # create BufferedWriter for new file
        self._dest = default_storage.open(self.path, mode='wb')

    def upload_chunk(self, chunk, *args, **kwargs):
        self._dest.write(chunk)

    def upload_complete(self, request, filename, *args, **kwargs):
        self._dest.close()
        return {"path": self.path}
