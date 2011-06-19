from io import FileIO, BufferedWriter
import os
from StringIO import StringIO

from django.conf import settings

from ajaxuploader.backends.base import AbstractUploadBackend

class LocalUploadBackend(AbstractUploadBackend):
    UPLOAD_DIR = "uploads"

    def setup(self, filename):
        self._filename = os.path.join(
            os.path.join(settings.MEDIA_ROOT, self.UPLOAD_DIR), filename)

        try:
            os.makedirs(os.path.realpath(os.path.dirname(self._filename)))
        except:
            pass

        self._dest = BufferedWriter(FileIO(self._filename, "wb"))

    def upload_chunk(self, chunk):
        self._dest.write(chunk)
