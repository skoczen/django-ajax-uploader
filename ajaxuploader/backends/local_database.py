from django.contrib.contenttypes.models import ContentType

from ajaxuploader.backends.local import LocalUploadBackend as _LocalUploadBackend
from ajaxuploader.models import UploadedFile

class LocalUploadBackend(_LocalUploadBackend):

    def set_object_id(self, object_id):
        self.__dict__['object_id'] = int(object_id)

    def upload_complete(self, request, filename):
        content_type = ContentType.objects.get_for_model(self.attach_to)
        extra_context = super(LocalUploadBackend, self).upload_complete(request, filename)

        qs = UploadedFile.objects.all()
        qs = qs.filter(content_type=content_type)
        qs = qs.filter(object_id=self.object_id)
        if qs.count()<3:
            uploaded_file_record = UploadedFile(path=extra_context['path'], filename=filename)
            uploaded_file_record.content_type = content_type
            uploaded_file_record.object_id = self.object_id
            uploaded_file_record.save()
        else:
            extra_context['error'] = 'exceeded the number of files allowed'
        return extra_context

    def upload(self, uploaded, filename, raw_data):
        qs = UploadedFile.objects.all()
        qs = qs.filter(content_type=ContentType.objects.get_for_model(self.attach_to))
        qs = qs.filter(object_id=self.object_id)
        if qs.count()<3:
            return super(LocalUploadBackend, self).upload(uploaded, filename, raw_data)
        else:
            return False