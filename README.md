`django-ajax-uploader` provides a useful class you can use to easily implement ajax uploads.

It uses valum's great uploader: https://github.com/valums/file-uploader, and draws heavy inspiration and some code from 
https://github.com/alexkuhl/file-uploader

In short, it implements a callable class, `AjaxFileUploader` that you can use to handle uploads. By default, `AjaxFileUploader` assumes you want to upload to local storage, but you can select any other backend if desired or write your own (see backends section below). Pull requests welcome!

Updates
=======

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
 

Usage
=====
Step 1. Install django-ajax-uploader. 
-------------------------------------
It's in pypi now, so simply:

- `pip install ajaxuploader`

You may also need to install backend-specific dependences. 

 - For the S3 backend, you will need [boto](https://github.com/boto/boto).  ( `pip install boto` )
 - For the MongoDB GridFS backend, you will need [pymongo](https://github.com/AloneRoad/pymongo) ( `pip install pymongo` )

Step 2. (Django 1.3 only)
-------------------------
For Django 1.3 you will need to have the app in your installed apps tuple for collect static to pick up the files.

First Add 'ajaxuploader' to you installed apps in settings.py

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

### easy_thumbnails.EasyThumbnailUploadBackend ###

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
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.  See the caveat at the bottom before changing it.

Context returned:

* `path`: The full media path to the uploaded file.


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


Caveats
=======
`BUFFER_SIZE` - some users have reported problems using smaller buffer sizes.  I also saw random failed uploads with very small sizes like 32k.  10MB has been completely reliable for me, and in what I've read here and there, so do some testing if you want to try a different value.  Note that this doesn't have a big impact on the overall upload speed.


Credits
=======
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



This code began as such a trivial layer on top of [valum's uploader](http://valums.com/ajax-upload/), [boto](https://github.com/boto/boto), and [alex's ideas](http://kuhlit.blogspot.com/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) it's silly.  However, I didn't find any implementations that *just worked*, so hopefully it's useful to someone else.  I also drew from these sources:

* http://www.topfstedt.de/weblog/?p=558
* http://www.elastician.com/2010/12/s3-multipart-upload-in-boto.html
* https://github.com/valums/file-uploader
* https://github.com/alexkuhl/file-uploader

Many thanks to all for writing such helpful and readable code!
