from django.conf import settings
from django.shortcuts import render
from django.middleware.csrf import get_token

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.s3 import S3UploadBackend

def s3direct(request):
    context = {
        'AWS_EXPECTED_BUCKET': settings.AWS_BUCKET_NAME,
        'AWS_UPLOAD_CLIENT_KEY': settings.AWS_ACCESS_KEY_ID,
        'csrf_token': get_token(request),
    }


    return render(request, 's3direct/upload.html', context)

s3_uploader = AjaxFileUploader(backend=S3UploadBackend)
