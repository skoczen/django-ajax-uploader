class AbstractUploadBackend(object):
    BUFFER_SIZE = 10485760  # 10MB

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def setup(self, filename, *args, **kwargs):
        """Responsible for doing any pre-processing needed before the upload
        starts."""

    def update_filename(self, request, filename, *args, **kwargs):
        """Returns a new name for the file being uploaded."""

    def upload_chunk(self, chunk, *args, **kwargs):
        """Called when a string was read from the client, responsible for 
        writing that string to the destination file."""
        raise NotImplementedError

    def upload_complete(self, request, filename, *args, **kwargs):
        """Overriden to performs any actions needed post-upload, and returns
        a dict to be added to the render / json context"""

    def upload(self, uploaded, filename, raw_data, *args, **kwargs):
        try:
            if raw_data:
                # File was uploaded via ajax, and is streaming in.
                chunk = uploaded.read(self.BUFFER_SIZE)
                while len(chunk) > 0:
                    self.upload_chunk(chunk, *args, **kwargs)
                    chunk = uploaded.read(self.BUFFER_SIZE)
            else:
                # File was uploaded via a POST, and is here.
                for chunk in uploaded.chunks():
                    self.upload_chunk(chunk, *args, **kwargs)
            return True
        except:
            # things went badly.
            return False
