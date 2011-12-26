import os
import hashlib
from shutil import rmtree

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class AjaxUploadTest(TestCase):
    urls = 'ajaxuploader.tests.urls'

    def setUp(self):
        super(AjaxUploadTest, self).setUp()
        
        self.test_dir = os.path.dirname(__file__)
        test_file = open(os.path.join(self.test_dir, '../fixtures/pony.png'),
                         'rb')

        self.test_file_1 = test_file

        # generate sha1 hash of the file
        self.test_file_1_hash = hashlib.sha1(self.test_file_1.read())\
                                       .hexdigest()

        # reset position to beginning of the file
        self.test_file_1.seek(0)
        
        
    def tearDown(self):
        # remove created uploads/tests directory
        rmtree(os.path.join(settings.MEDIA_ROOT, 'uploads/tests'))
        
    def test_upload_raw_post_local_backend(self):
        """
        tests uploading a file to DefaultStorageUploadBackend
        """

        # there is a bug in Django 1.3.1 with raw_post_data in the django test client
        # it's fixed in trunk
        # https://code.djangoproject.com/changeset/16479

        uploaded_file_name = 'tests/foo.png'

        file_data = self.test_file_1.read()
        # post raw self.test_file_1 data to AjaxFileUploader as Ajax request
        response = self.client.post(reverse('ajax-upload-default-storage')+'?qqfile=%s' % \
                                    uploaded_file_name, file_data,
                                    content_type='application/octet-stream',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads',
                                          uploaded_file_name)
        uploaded_file = open(uploaded_file_path, 'rb')

        # uploaded file must exist in MEDIA_DIR
        self.assertTrue(os.path.exists(uploaded_file_path))

        # sha1 hash of original file and uploaded file must match
        self.assertEquals(hashlib.sha1(uploaded_file.read()).hexdigest(),
                          self.test_file_1_hash)
