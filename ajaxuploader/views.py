from StringIO import StringIO
from multiprocessing import Pool
from django.http import HttpResponse, HttpResponseBadRequest, Http404
import boto
import json
from django.conf import settings
class AjaxFileUploader(object):
    NUM_PARALLEL_PROCESSES = 4
    BUFFER_SIZE = 10485760  # 10MB

    def __call__(self,request):
        return self._ajax_upload(request)

    def _update_filename(self, request, filename):
        return filename

    def _upload_complete(self, request, filename):
        """Overriden to performs any actions needed post-upload, and
            returns a dict to be added to the render / json context"""
        return {}

    def _upload_chunk(self, pool, mp, chunk, counter):
        buffer = StringIO()
        buffer.write(chunk)
        pool.apply_async(mp.upload_part_from_file(buffer, counter))
        buffer.close()

    def _save_upload(self, uploaded, filename, raw_data ):
        try:
            bucket = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY).lookup(settings.AWS_BUCKET_NAME)
            mp = bucket.initiate_multipart_upload(filename)
            pool = Pool(processes=self.NUM_PARALLEL_PROCESSES)
            counter = 0        

            if raw_data:
                # File was uploaded via ajax, and is streaming in.
                chunk = uploaded.read(self.BUFFER_SIZE)
                while len(chunk) > 0:
                    counter += 1
                    self._upload_chunk(pool, mp, chunk, counter)
                    chunk = uploaded.read(self.BUFFER_SIZE)
            else:
                # File was uploaded via a POST, and is here.
                for chunk in uploaded.chunks():
                    counter += 1
                    self._upload_chunk(pool, mp, chunk, counter)

            # Tie up loose ends, and finish the upload
            pool.close()
            pool.join()
            mp.complete_upload()
            return True

        except:
            # things went badly.
            return False


    def _ajax_upload(self, request):
        if request.method == "POST":        
            if request.is_ajax():
                # the file is stored raw in the request
                upload = request
                is_raw = True
                # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
                try:
                    filename = request.GET[ 'qqfile' ]
                except KeyError: 
                    return HttpResponseBadRequest( "AJAX request not valid" )
            # not an ajax upload, so it was the "basic" iframe version with submission via form
            else:
                is_raw = False
                if len( request.FILES ) == 1:
                    # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
                    # ID based on a random number, so it cannot be guessed here in the code.
                    # Rather than editing Ajax Upload to pass the ID in the querystring,
                    # observe that each upload is a separate request,
                    # so FILES should only have one entry.
                    # Thus, we can just grab the first (and only) value in the dict.
                    upload = request.FILES.values()[ 0 ]
                else:
                    raise Http404( "Bad Upload" )
                filename = upload.name
            
            # custom filename handler
            filename = self._update_filename(request, filename)

            # save the file
            success = self._save_upload( upload, filename, is_raw )
     
            # callback
            extra_context = self._upload_complete(request, filename)

            # let Ajax Upload know whether we saved it or not
            ret_json = { 'success': success, }
            ret_json.update(extra_context)
            return HttpResponse( json.dumps( ret_json ) )
