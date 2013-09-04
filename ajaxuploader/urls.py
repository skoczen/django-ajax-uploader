from django.conf.urls import patterns, url

from .views import handle_s3, success_redirect_endpoint

urlpatterns = patterns(
    '',
    url(r'^s3/signature', handle_s3, name="s3_signature"),
    url(r'^s3/delete', handle_s3, name='s3_delete'),
    url(r'^s3/success', success_redirect_endpoint, name="s3_success")
)
