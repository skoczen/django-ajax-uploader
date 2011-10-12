from ajaxuploader.backends.local import LocalUploadBackend as _LocalUploadBackend
from ajaxuploader.models import UploadedFile

class LocalUploadBackend(_LocalUploadBackend):
	def upload_complete(self, request, filename):
		extra_context = super(LocalUploadBackend, self).upload_complete(request, filename)
		uploaded_file_record = UploadedFile(path=extra_context['path'])
		uploaded_file_record.save()
		return extra_context