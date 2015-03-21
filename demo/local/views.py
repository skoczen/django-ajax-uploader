from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader

def local(request):
    csrf_token = get_token(request)
    return render_to_response('local/upload.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

local_uploader = AjaxFileUploader()
