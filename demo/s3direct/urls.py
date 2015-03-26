from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from s3direct import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'up$', views.s3direct, name="s3direct"),
    url(r'ajax-upload/$', views.s3_uploader, name="my_s3_upload"),
)
