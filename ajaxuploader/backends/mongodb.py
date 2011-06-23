from django.conf import settings

from pymongo import Connection
import gridfs

from ajaxuploader.backends.base import AbstractUploadBackend

class MongoDBUploadBackend(AbstractUploadBackend):

    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')
        self.collection = kwargs.pop('collection')
        self.connection = Connection(
            host=getattr(settings, 'AJAXUPLOAD_MONGODB_HOST', 'localhost'),
            port=getattr(settings, 'AJAXUPLOAD_MONGODB_PORT', 27017)
        )[self.db]
        self.grid = gridfs.GridFS(self.connection, collection=self.collection)
        super(MongoDBUploadBackend, self).__init__(*args, **kwargs)

    def setup(self, filename):
        self._path = filename
        self.f = self.grid.new_file(**{'filename': self._path})

    def upload_chunk(self, chunk):
        self.f.write(chunk)

    def upload_complete(self, request, filename):
        self.f.close()
