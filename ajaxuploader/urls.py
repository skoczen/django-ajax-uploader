from django.conf.urls.defaults import *

from ajaxuploader.views import AjaxFileUploader


urlpatterns = patterns('',
    url(r'^upload$', AjaxFileUploader(), name="ajax-upload"),                
)
