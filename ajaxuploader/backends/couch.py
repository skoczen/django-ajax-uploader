"""CouchDB Backend Module for django-ajaxuploader

"""

from uuid import uuid4
from tempfile import TemporaryFile

from couchdb import Server
from django.conf import settings

from ajaxuploader.backends.base import AbstractUploadBackend

class CouchDBUploadBackend(AbstractUploadBackend):
    """Stores the file in a CouchDB Backend

    Requirements: couchdb

    Settings:
    AJAXUPLOAD_COUCHDB_HOST:  Specify the host of your MongoDB server.
     Defaults to http://localhost:5984 if not specified.

    Arguments:
    db (required): Specify the database within CouchDB you wish to use

    Context returned:
    None
    
    """
    def __init__(self, *args, **kwargs):
        self.database = kwargs.pop('db')
        self.connection = None
        self._dest = None
        
        super(CouchDBUploadBackend, self).__init__(*args, **kwargs)

    def setup(self, filename, *args, **kwargs):
        self.connection = Server(getattr(settings,
                                         'AJAXUPLOAD_COUCHDB_HOST',
                                         'http://localhost:5984')
        )[self.database]
        self._dest = TemporaryFile()

    def upload_chunk(self, chunk, *args, **kwargs):
        self._dest.write(chunk)

    def upload_complete(self, request, filename, *args, **kwargs):
        self._dest.seek(0)
        doc_id = uuid4().hex
        # create doc by self defined uuid. We need the _rev for attachment
        doc = self.connection[doc_id] = {'_id':doc_id,
                                         # append anything you like maybe from
                                         # request
                                         }
        # mimetype is guessed by extension.
        # We don't put the whole document back in the put_attachment request
        self.connection.put_attachment({'_id':doc['_id'], '_rev':doc['_rev']},
                                        self._dest,
                                        filename=filename)
        self._dest.close()
