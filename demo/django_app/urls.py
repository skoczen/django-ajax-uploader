from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    #url(r'^s3/', include('s3.urls')),
    #url(r'^s3direct/', include('local.urls')),
    url(r'^local/', include('local.urls')),


    url(r'^admin/', include(admin.site.urls)),
)
