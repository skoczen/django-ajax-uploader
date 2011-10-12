from django.contrib.contenttypes.models import ContentType

from ajaxuploader.backends.local import LocalUploadBackend as _LocalUploadBackend
from ajaxuploader.models import UploadedFile

class LocalUploadBackend(_LocalUploadBackend):

    def set_object_id(self, object_id):
        self.__dict__['object_id'] = object_id

    def upload_complete(self, request, filename):
        extra_context = super(LocalUploadBackend, self).upload_complete(request, filename)
        uploaded_file_record = UploadedFile(path=extra_context['path'])
        uploaded_file_record.content_type = ContentType.objects.get_for_model(self.attach_to)
        uploaded_file_record.object_id = int(self.object_id)
        uploaded_file_record.save()
        return extra_context