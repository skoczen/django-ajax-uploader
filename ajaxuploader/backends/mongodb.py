import mimetypes

from django.conf import settings

from pymongo import Connection
import gridfs

from ajaxuploader.backends.base import AbstractUploadBackend


class MongoDBUploadBackend(AbstractUploadBackend):
    """
    Stores uploaded file in Mongo's GridFS.

    Requirements: pymongo
    """
    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')

        try:
            self.collection = kwargs.pop('collection')
        except KeyError:
            self.collection = None

        super(MongoDBUploadBackend, self).__init__(*args, **kwargs)

    def setup(self, filename, encoding='UTF-8', *args, **kwargs):
        """
        Setup MongoDB connection to specified db. Collection is optional
        and will default to fs if not specified.

        Create new gridFS file which returns a GridIn instance to write
        data to.
        """
        host = getattr(settings, "AJAXUPLOAD_MONGODB_HOST", "localhost:27017")
        port = getattr(settings, "AJAXUPLOAD_MONGODB_PORT", 27017)
        replicaset = getattr(settings, "AJAXUPLOAD_MONGODB_REPLICASET", "")

        if isinstance(host, list):
            host = ", ".join(host)
        else:
            if not ":" in host:
                """
                Backwards compatibility for old version.
                """
                host = u"%s:%d" % (host, port)
        self.connection = Connection(host, replicaset=replicaset)[self.db]

        if self.collection:
            self.grid = gridfs.GridFS(self.connection,
                collection=self.collection)
        else:
            self.grid = gridfs.GridFS(self.connection)

        self._path = filename
        content_type, encoding = mimetypes.guess_type(filename)
        self.f = self.grid.new_file(**{'filename': self._path,
            'encoding': 'UTF-8', 'content_type': content_type})

    def upload_chunk(self, chunk, *args, **kwargs):
        self.f.write(chunk)

    def upload_complete(self, request, filename, *args, **kwargs):
        self.f.close()
