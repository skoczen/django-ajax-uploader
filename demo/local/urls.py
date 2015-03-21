from django.conf.urls import patterns, include, url
from django.conf import settings
from local import views

urlpatterns = patterns('',
    url(r'upload$', views.local, name="local"),
    url(r'ajax-upload$', views.local_uploader, name="my_ajax_upload"),
)
