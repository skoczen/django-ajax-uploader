import mimetypes

from django.conf import settings

from pymongo import Connection
import gridfs

from ajaxuploader.backends.base import AbstractUploadBackend

class MongoDBUploadBackend(AbstractUploadBackend):

    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')

        try:
            self.collection = kwargs.pop('collection')
        except KeyError:
            self.collection = None

        super(MongoDBUploadBackend, self).__init__(*args, **kwargs)

    def setup(self, filename, encoding='UTF-8'):
        """
        Setup MongoDB connection to specified db. Collection is optional
        and will default to fs if not specified.

        Create new gridFS file which returns a GridIn instance to write
        data to.
        """
        self.connection = Connection(
            host=getattr(settings, 'AJAXUPLOAD_MONGODB_HOST', 'localhost'),
            port=getattr(settings, 'AJAXUPLOAD_MONGODB_PORT', 27017)
        )[self.db]

        if self.collection:
            self.grid = gridfs.GridFS(self.connection,
                collection=self.collection)
        else:
            self.grid = gridfs.GridFS(self.connection)

        self._path = filename
        content_type, encoding = mimetypes.guess_type(filename)
        self.f = self.grid.new_file(**{'filename': self._path,
            'encoding': 'UTF-8', 'content_type': content_type})

    def upload_chunk(self, chunk):
        self.f.write(chunk)

    def upload_complete(self, request, filename):
        self.f.close()
