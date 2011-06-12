class AbstractUploadBackend(object):
    BUFFER_SIZE = 10485760  # 10MB

    def setup(self, filename):
        """TODO"""

    def update_filename(self, request, filename):
        """Returns a new name for the file being uploaded."""

    def upload_chunk(self, chunk):
        """TODO"""

    def upload_complete(self, request, filename):
        """Overriden to performs any actions needed post-upload, and returns
        a dict to be added to the render / json context"""

    def upload(self, uploaded, filename, raw_data):
        try:
            if raw_data:
                # File was uploaded via ajax, and is streaming in.
                chunk = uploaded.read(self.BUFFER_SIZE)
                while len(chunk) > 0:
                    self.upload_chunk(chunk)
                    chunk = uploaded.read(self.BUFFER_SIZE)
            else:
                # File was uploaded via a POST, and is here.
                for chunk in uploaded.chunks():
                    self.upload_chunk(chunk)
            return True
        except:
            # things went badly.
            return False
