from django.conf.urls import patterns, include, url
from django.conf import settings
from s3direct import views

urlpatterns = patterns('',
    url(r'ajax-uploader/', include('ajaxuploader.urls', namespace='ajaxuploader', app_name='ajaxuploader')),
    url(r'upload/$', views.s3direct, name="s3direct_client"),
)
