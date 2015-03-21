from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

from local import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    #url(r'^s3/', include('s3.urls')),
    #url(r'^s3direct/', include('local.urls')),
    url(r'^local/', include('local.urls')),

    url(r'ajax-upload$', views.local_uploader, name="my_ajax_upload"),

    url(r'^admin/', include(admin.site.urls)),
)
