import os

from sorl.thumbnail import get_thumbnail

from ajaxuploader.backends.local import LocalUploadBackend

class ThumbnailUploadBackend(LocalUploadBackend):
    def __init__(self, dimension):
        self._dimension = dimension
    
    def upload_complete(self, request, filename):
        thumbnail = get_thumbnail(self._filename, self._dimension)
        os.unlink(self._filename)
        return {"path": thumbnail.name}
