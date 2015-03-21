from django.middleware.csrf import get_token
from django.shortcuts import render

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.s3 import S3UploadBackend

def s3(request):
    context = {
        'csrf_token': get_token(request),
    }

    return render(request, 's3/upload.html', context)

s3_uploader = AjaxFileUploader(backend=S3UploadBackend)
