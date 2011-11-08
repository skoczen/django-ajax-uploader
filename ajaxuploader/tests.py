import os
from shutil import rmtree

from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse



class AjaxUploadTest(TestCase):
    urls = 'ajaxuploader.urls'

    def setUp(self):
        super(AjaxUploadTest, self).setUp()
        if hasattr(settings, 'USER_UPLOADS'):
            self.old_upload_dir = settings.USER_UPLOADS
        else:
            self.old_upload_dir = None

        settings.USER_UPLOADS = 'tests/uploads/'
        
        self.test_dir = os.path.dirname(__file__)
        test_file = open(os.path.join(self.test_dir, 'fixtures/pony.png'), 'rb')
        self.test_file_1 = test_file
        User.objects.create_user(username='user1',
                                          password='!', email='foo@bar.com')

        
    def tearDown(self):
        #rmtree(os.path.join(settings.MEDIA_ROOT, settings.USER_UPLOADS))
        settings.USER_UPLOADS = self.old_upload_dir

    def test_upload_view(self):
        """
        test the ajax upload view
        """
        # there is a bug in Django 1.3 with raw_post_data in the django test client
        # https://code.djangoproject.com/ticket/15679
        # fixed in 1.3.1 

        response = self.client.post(reverse('ajax-upload')+'?qqfile=foobar.png', self.test_file_1.read(), content_type='application/octet-stream', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

