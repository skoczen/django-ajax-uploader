import os
from io import FileIO, BufferedWriter


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from ajaxuploader.backends.base import AbstractUploadBackend


class LocalUploadBackend(AbstractUploadBackend):
    UPLOAD_DIR = 'uploads'

    def setup(self, filename):
        # join UPLOAD_DIR with filename 
        new_path = os.path.join(self.UPLOAD_DIR, filename)

        # save empty file in default storage with path = new_path
        self._path = default_storage.save(new_path, ContentFile(''))

        # get absolute path to new file
        self._abs_path = default_storage.path(self._path)

        # create BufferedWriter for new file
        self._dest = BufferedWriter(FileIO(self._abs_path, "w"))

    def upload_chunk(self, chunk):
        self._dest.write(chunk)

    def upload_complete(self, request, filename):
        self._dest.close()
        return {"path": self._path}
