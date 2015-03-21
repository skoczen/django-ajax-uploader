from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from s3 import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'upload$', views.s3, name="s3_upload"),
    #url(r'^s3-upload$', views.s3_uploader, name="my_s3_upload"),
)
