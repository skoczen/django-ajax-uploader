from io import FileIO, BufferedWriter
import os

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files.move import file_move_safe

from ajaxuploader.backends.base import AbstractUploadBackend

class LocalUploadBackend(AbstractUploadBackend):
    UPLOAD_DIR = "uploads"

    def setup(self, filename):
        self._path = os.path.join(
            settings.MEDIA_ROOT, self.UPLOAD_DIR, filename)
        try:
            os.makedirs(os.path.realpath(os.path.dirname(self._path)))
        except:
            pass
        self._dest = NamedTemporaryFile(suffix='.upload', dir=settings.FILE_UPLOAD_TEMP_DIR)

    def upload_chunk(self, chunk):
        self._dest.write(chunk)

    def upload_complete(self, request, filename):
        file_move_safe(self._dest.name, self._path, allow_overwrite=True)
        return {"path": self._path}
