from io import FileIO, BufferedWriter
import os

from django.conf import settings

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
        self._dest = BufferedWriter(FileIO(self._path, "w"))

    def upload_chunk(self, chunk):
        self._dest.write(chunk)

    def upload_complete(self, request, filename):
        path = settings.MEDIA_URL + self.UPLOAD_DIR + "/" + filename
        self._dest.close() 
        return {"path": path}
