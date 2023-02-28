`django-ajax-uploader` provides a useful class you can use to easily implement ajax uploads.

It uses valum's great uploader: https://github.com/valums/file-uploader, and draws heavy inspiration and some code from https://github.com/alexkuhl/file-uploader.

You can also use [fineuploader](http://fineuploader.com/), the commercial/open source project that sprung out of valum's original work. It's great, and highly recommended. 

In short, it implements a callable class, `AjaxFileUploader` that you can use to handle uploads. By default, `AjaxFileUploader` assumes you want to upload to local storage, but you can select any other backend if desired or write your own (see backends section below). Pull requests welcome!

Updates
=======

Version 0.3.x is released, and contains:

* Support for direct to s3 backends
* Official deprecation of the included fileuploader.js.  Please use [fineuploader](http://fineuploader.com/) going forward.

Installation and Usage
======================

You have two basic ways to set up django-ajax-uploader.

- If you want to handle the files yourself, follow the [Standard Instructions](https://github.com/goodcloud/django-ajax-uploader/#usage-standard-non-direct-to-s3-backends).
- If you want to upload directly to s3, follow the [S3 Instructions](https://github.com/goodcloud/django-ajax-uploader/#usage-direct-to-s3-uploads).



Usage (standard, non-direct to s3 backends)
===========================================

Step 1. Install django-ajax-uploader. 
-------------------------------------
It's in pypi now, so simply:

- `pip install ajaxuploader`

You may also need to install backend-specific dependences. 

 - For the S3 backend or direct S3 uploads, you will need [boto](https://github.com/boto/boto).  ( `pip install boto` )
 - For the MongoDB GridFS backend, you will need [pymongo 3.13.0](https://github.com/AloneRoad/pymongo) ( `pip install pymongo==3.13.0` )

Step 2. (Django 1.3+)
-------------------------
Add 'ajaxuploader' to your installed apps in settings.py:

```
INSTALLED_APPS = (
    ...
    "ajaxuploader",
)
```

Then:

```
$ python manage.py collectstatic
```

Step 3. Include it in your app's views and urls.
------------------------------------------------
You'll need to make sure to meet the csrf requirements to still make valum's uploader work.  Code similar to the following should work:

views.py

```python
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader


def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()
``` 

urls.py 

```
url(r'start$', views.start, name="start"),
url(r'ajax-upload$', views.import_uploader, name="my_ajax_upload"),
```

Step 4. Set up your template.
-----------------------------
This sample is included in the templates directory, but at the minimum, you need:

```html
<!doctype html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js" ></script>
        <script src="{{ STATIC_URL }}ajaxuploader/js/fileuploader.js" ></script>
        <link href="{{ STATIC_URL }}ajaxuploader/css/fileuploader.css" media="screen" rel="stylesheet" type="text/css" />
        <script>
            $(function(){
            var uploader = new qq.FileUploader({
                action: "{% url my_ajax_upload %}",
                element: $('#file-uploader')[0],
                multiple: true,
                onComplete: function(id, fileName, responseJSON) {
                    if(responseJSON.success) {
                        alert("success!");
                    } else {
                        alert("upload failed!");
                    }
                },
                onAllComplete: function(uploads) {
                    // uploads is an array of maps
                    // the maps look like this: {file: FileObject, response: JSONServerResponse}
                    alert("All complete!");
                },
                params: {
                    'csrf_token': '{{ csrf_token }}',
                    'csrf_name': 'csrfmiddlewaretoken',
                    'csrf_xname': 'X-CSRFToken',
                },
            });
            });
        </script>
    </head>
<body>
    <div id="file-uploader">       
        <noscript>          
            <p>Please enable JavaScript to use file uploader.</p>
        </noscript>         
    </div>
</body>
</html>
```


 If you want to use the latest version of [Fine Uploader](http://fineuploader.com/), as valum's `file-uploader` is now called, instead of the one bundled with `django-ajax-uploader`, you can do so by replacing the params arguments in the above template with the following customHeaders:
 
 ```javascript
                 ...
                 customHeaders: {
                     'X-CSRFToken': '{{ csrf_token }}',
                 },
                 ...
 ```
 

Usage (Direct to S3 uploads)
===========================================

Step 1. Install django-ajax-uploader and dependencies. 
------------------------------------------------------

- `pip install ajaxuploader boto`


Step 2. Set up any necessary keys at AWS
----------------------------------------

Fineuploader has a great [tutorial here](http://blog.fineuploader.com/2013/08/16/fine-uploader-s3-upload-directly-to-amazon-s3-from-your-browser/).


Step 3. Include it in your app's settings and urls
--------------------------------------------------

Add 'ajaxuploader' to your installed apps in settings.py

```
INSTALLED_APPS = (
    ...
    "ajaxuploader",
)
```

Also in settings, add the following: 

```python
AWS_UPLOAD_BUCKET_NAME = "bucket-to-upload-to"
AWS_UPLOAD_CLIENT_KEY = "public-aws-upload-key"
AWS_UPLOAD_CLIENT_SECRET_KEY = "secret-aws-upload-key"
```

In your urls.py, add:
```python
url(r'^ajax-uploader/', include('ajaxuploader.urls', namespace='ajaxuploader', app_name='ajaxuploader')),
```

Then:

```
$ python manage.py collectstatic
```


Step 4. Set up your template.
-----------------------------

You can pretty much just use the same examples as are on fineuploader's site.  Make sure to pass in `AWS_UPLOAD_CLIENT_KEY` and `AWS_UPLOAD_BUCKET_NAME` to the template, and something like this should work:

```html
<div id="fine_uploader"></div>

<script>
var uploader = new qq.s3.FineUploader({
    element: document.getElementById('fine_uploader'),
    request: {
        endpoint: '{{ AWS_UPLOAD_BUCKET_NAME }}.s3.amazonaws.com',
        accessKey: AWS_CLIENT_ACCESS_KEY
    },
    signature: {
        endpoint: '{% url "ajaxuploader:s3_signature" %}'
    },
    uploadSuccess: {
        endpoint: '{% url "ajaxuploader:s3_success" %}'
    },
    iframeSupport: {
        localBlankPagePath: '/success.html'
    },
    deleteFile: {
        enabled: true,
        endpoint: '{% url "ajaxuploader:s3_delete" %}'
    },
});
</script>
```


Backends
========

`django-ajax-uploader` can put the uploaded files into a number of places, and perform actions on the files uploaded. Currently, 
there are backends available for local storage (default), Amazon S3, MongoDB (GridFS), CouchDB, and a locally stored image 
thumbnail backend. Creating a custom backend is fairly straightforward, and pull requests are welcome.

Built-in Backends
------------------

`django-ajax-uploader` has the following backends:

### local.LocalUploadBackend ###

Stores the file locally, by default to `{MEDIA_ROOT}/uploads`.

Requirements:

* None

Settings:

* `UPLOAD_DIR` : The directory to store the uploaded file in, within `MEDIA_ROOT`. Defaults to "uploads".
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.  See the caveat at the bottom before changing it.

Context returned:

* `path`: The full media path to the uploaded file.


### mongodb.MongoDBUploadBackend ###

Stores the file in MongoDB via GridFS

Requirements

* [pymongo](https://github.com/AloneRoad/pymongo)

Settings:

* `AJAXUPLOAD_MONGODB_HOST`: Specify either a single host:port or a list of host:port. Defaults to `"localhost:27017"`
* `AJAXUPLOAD_MONGODB_PORT` (for backwards compatibility): Specify the port of your MongoDB server. Defaults to 27017 if not specified.
* `AJAXUPLOAD_MONGODB_REPLICASET` (optional): Specify the name of your replicaset as a string. Defaults to an empty string.

```python

# Replicaset
AJAXUPLOAD_MONGODB_HOST = ["127.0.0.1:27017", "127.0.0.1:27018"]
AJAXUPLOAD_MONGODB_REPLICASET = "myset"

# Standard
AJASUPLOAD_MONGODB_HOST = "127.0.0.1:27017"
```

Arguments

* db (required): Specify the database within MongoDB you wish to use
* collection (optional): Specify the collection within the db you wish to use. This is optional and will default to `fs` if not specified


Context returned:

* None


### couch.CouchDBUploadBackend ###

Stores the file in a CouchDB backend

Requirements

* [couchdb](http://code.google.com/p/couchdb-python/)

Settings:

* `AJAXUPLOAD_COUCHDB_HOST`: Specify the host of your CouchDB server. Defaults to `http://localhost:5984` if not specified.

Arguments

* db (required): Specify the database within CouchDB you wish to use


Context returned:

* None


### s3.S3UploadBackend ###

Stores the file in Amazon's S3.

Requirements:

* [boto](https://github.com/boto/boto)

Settings:

* `NUM_PARALLEL_PROCESSES` : Uploads to Amazon are parallelized to increase speed. If you have more cores and a big pipe, increase this setting for better performance. Defaults to 4.
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.

Context returned:

* None


### thumbnail.ThumbnailUploadBackend ###

Stores a thumbnail of the locally, optionally discarding the upload.  Subclasses `LocalUploadBackend`.

Requirements:

* [sorl-thumbnail](https://github.com/sorl/sorl-thumbnail)

Settings:

* `DIMENSIONS` : A string of the dimensions (WxH) to resize the uploaded image to. Defaults to "100x100"
* `KEEP_ORIGINAL`: Whether to keep the originally uploaded file. Defaults to False.
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.

Context returned:

* `path`: The full media path to the uploaded file.

### easythumbnails.EasyThumbnailUploadBackend ###

Stores a thumbnail of the locally, optionally discarding the upload. Uses 'Easy Thumbnails' rather than sorl-thumbnail,
which requires a key-value store. Subclasses `LocalUploadBackend`.

Requirements:

* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails/)

Settings:

* `DIMENSIONS` : A tuple of the dimensions (WxH) to resize the uploaded image to. Defaults to "100x100"
* `KEEP_ORIGINAL`: Whether to keep the originally uploaded file. Defaults to False.
* `CROP`: Whether to create a 'cropped' version of the thumbnail. Defaults to True. 
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.

Context returned:

* `path`: The full media path to the uploaded file.


### default_storage.DefaultStorageUploadBackend ###

This backend uses Django's default storage backend (defined by the  DEFAULT_FILE_STORAGE setting) to save the uploaded files.

Requirements:

* None

Settings:

* `UPLOAD_DIR` : The directory to store the uploaded file in, within `MEDIA_ROOT`. Defaults to "uploads".
* `BUFFER_SIZE`: The size in bytes of each chunk to write. Defaults to 10 MB; i.e. 10485760 bytes.  See the caveat at the bottom before changing it.

Context returned:

* `path`: The full media path to the uploaded file.

Example Usage:

```python

#views.py
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend

import_uploader = AjaxFileUploader(UPLOAD_DIR='my_upload', backend=EasyThumbnailUploadBackend, DIMENSIONS=(250, 250)) 
```


Backend Usage
------------------------

The default backend is `local.LocalUploadBackend`. To use another backend, specify it when instantiating `AjaxFileUploader`.

For instance, to use `MongoDBUploadBackend`:

views.py

```python
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.mongodb import MongoDBUploadBackend

...
import_uploader = AjaxFileUploader(backend=MongoDBUploadBackend, db='uploads')
```

To set custom parameters, simply pass them along with instantiation.  For example, for larger thumbnails, preserving the originals:
views.py

    from ajaxuploader.backends.thumbnail import ThumbnailUploadBackend

    ...
    import_uploader = AjaxFileUploader(backend=ThumbnailUploadBackend, DIMENSIONS="500x500", KEEP_ORIGINAL=True)


Custom Backends
-------------

To write a custom backend, simply inherit from `backends.base.AbstractUploadBackend` and implement the `upload_chunk` method.  All possible methods to override are described below.

* `upload_chunk` - takes a string, and writes it to the specified location.
* `setup`: takes the original filename, does all pre-processing needed before uploading the file (for example, for the S3 backend, this method is used to establish a connection with the S3 server).
* `update_filename`: takes the `request` object and the original name of the file being updated, can return a new filename which will be used to refer to the file being saved. If undefined, the uploaded filename is used.  If not overriden by `upload_complete`, this value will be returned in the response.
* `upload_complete`: receives the `request` object and the filename post `update_filename` and does any cleanup or manipulation after the upload is complete.  (Examples:  cropping the image, disconnecting from the server).  If a dict is returned, it is used to update the response returned to the client.


Signals
=======

The signal `ajaxuploader.signals.file_uploaded` will be fired after a file has been sucessfully uploaded.

Listener methods receives two arguments: the backend that stored the file, and the upload's request.

```python
    from django.db import models
    from django.dispatch import receiver

    from ajaxuploader.views import AjaxFileUploader
    from ajaxuploader.signals import file_uploaded


    class MyModel(models.Model):
        user = models.ForeignKey('auth.User')
        document = models.FileField(upload_to='attachments/%Y/%m/%d')


    @receiver(file_uploaded, sender=AjaxFileUploader)
    def create_on_upload(sender, backend, request, **kwargs):
        MyModel.objects.create(user=request.user, document=backend.path)
```


Caveats
=======
`BUFFER_SIZE` - some users have reported problems using smaller buffer sizes.  I also saw random failed uploads with very small sizes like 32k.  10MB has been completely reliable for me, and in what I've read here and there, so do some testing if you want to try a different value.  Note that this doesn't have a big impact on the overall upload speed.


Credits and Updates
===================

Many thanks to all for writing such helpful and readable code!

0.3.8

* `backends.path` property added by [gilsondev](https://github.com/gilsondev)
* python3 exception fix by [eryckson](https://github.com/eryckson)

0.3.7

* Fixes to `UPLOAD_DIR` handling and docs by [dogstick](https://github.com/dogstick)

0.3.6

* More robust handling of fineuploader vs valum's by [mbaechtold](https://github.com/mbaechtold)

0.3.5

* JSON import bug fixed by [lazerscience](https://github.com/lazerscience)
* EasyThumbnail backend rename by [michel54 and a rather annoyed crowd](https://github.com/GoodCloud/django-ajax-* uploader/pull/35)
* Saner s3 checking by [aalebedev](https://github.com/aalebedev)
* MongoDB improvements on upload by [dannybrowne86](https://github.com/dannybrowne86)
* Respecting django's UPLOAD_DIR by [dotcom900825](https://github.com/dotcom900825)
* Callable upload_dir with date string formatting by [fcurella](https://github.com/fcurella)
* Documentation improvements by [worldofchris](https://github.com/worldofchris)
* Directory traversal security fix by [hschmitt](https://github.com/hschmitt)
* Ability to clear all drop areas by [minddust](https://github.com/minddust)
* file_uplaoded signal fires by [fcurella](https://github.com/fcurella)
* More bugfixes by [fcurella](https://github.com/fcurella)


Long before I switched to this update format:

Original implementation and ongoing maintenance by [skoczen](https://github.com/skoczen), courtesy of [GoodCloud](https://www.agoodcloud.com).
Most of the backend abstraction was written by [chromano](https://github.com/chromano) and [shockflash](https://github.com/shockflash).  
MongoDB support and saner defaults by [chrisjones-brack3t](https://github.com/chrisjones-brack3t).  
Threadsafe improvements and bugfixes by [dwaiter](https://github.com/dwaiter).  
CouchDB support by [paepke](https://github.com/paepke).
Default Storage backend by [fhahn](https://github.com/fhahn).  
EasyThumbnail backend by [Miserlou](https://github.com/Miserlou).  
File number limit in upload by [qnub](https://github.com/qnub).  
JSON parsing improvements by [onyxfish](https://github.com/onyxfish).  
JSON content type added by [majdal](https://github.com/majdal).  
Improvements to Local backend by [OnlyInAmerica](https://github.com/OnlyInAmerica).  
Multiple upload improvements by [truetug](https://github.com/truetug).
Better subclassable backends by [minddust](https://github.com/minddust).
Addition of direct S3 support by [skoczen](https://github.com/skoczen), courtesy of [GreenKahuna](https://www.greenkahuna.com).

This code began as such a trivial layer on top of [valum's uploader](http://valums.com/ajax-upload/), [boto](https://github.com/boto/boto), and [alex's ideas](http://kuhlit.blogspot.com/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) it's silly.  However, I didn't find any implementations that *just worked*, so hopefully it's useful to someone else.  I also drew from these sources:

* http://www.topfstedt.de/weblog/?p=558
* http://www.elastician.com/2010/12/s3-multipart-upload-in-boto.html
* https://github.com/valums/file-uploader
* https://github.com/alexkuhl/file-uploader


Past Release History / API Changes
==================================

Version 0.3.5 is released, with the following backward incompababile changes:

* The EasyThumbnail backend now lives in `easythumbnails.py`, instead of `easy_thumbnails.py`. 


Version 0.2.1 is released, and contains:

* JSON parsing of `extra_context` now properly handles datetimes. (Thanks to onyxfish)


Version 0.2 is released, and contains:
    
* Optional `fileLimit` param for the uploader, to limit the number of allowed files. (Thanks to qnub)
* fhahn's `default_storage` backend.
 

Version 0.1.1 is released, and contains:

* Support for a CouchDB backend
* A backwards-incompatible change to the location of the ajaxuploader static files. I try to avoid backwards incompatibilities, but since /js and /css are the proper conventions and the lib is relatively young, it seemed better to get things right now, instead of waiting. The static files are now at:
  * `{{STATIC_URL}}ajaxuploader/js/fileuploader.js`
  * `{{STATIC_URL}}ajaxuploader/css/fileuploader.css`
