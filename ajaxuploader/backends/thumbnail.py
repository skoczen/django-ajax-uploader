import os

from django.conf import settings
from sorl.thumbnail import get_thumbnail

from ajaxuploader.backends.local import LocalUploadBackend

class ThumbnailUploadBackend(LocalUploadBackend):
    DIMENSIONS = "100x100"
    KEEP_ORIGINAL = False

    def upload_complete(self, request, filename, *args, **kwargs):
        thumbnail = get_thumbnail(self._path, self.DIMENSIONS)
        if not self.KEEP_ORIGINAL:
            os.unlink(self._path)
        return {"path": settings.MEDIA_URL + thumbnail.name}
