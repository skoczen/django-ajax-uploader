import os

from django.conf import settings
from sorl.thumbnail import get_thumbnail

from ajaxuploader.backends.local import LocalUploadBackend

class ThumbnailUploadBackend(LocalUploadBackend):
    DIMENSION = "100x100"

    def upload_complete(self, request, filename):
        thumbnail = get_thumbnail(self._path, self.DIMENSION)
        os.unlink(self._path)
        return {"path": settings.MEDIA_URL + thumbnail.name}
