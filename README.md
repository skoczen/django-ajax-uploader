`django-ajax-uploader` provides a useful class you can use to easily implement ajax uploads.

It uses valum's great uploader: https://github.com/valums/file-uploader , and draws heavy inspiration and some code from https://github.com/alexkuhl/file-uploader

In short, it implements a callable class, `AjaxFileUploader` that you can use to handle uploads.  By default, `AjaxFileUploader` assumes you want to upload to Amazon's S3, but you can select any other backend if desired or write your own (see backends section below).  Pull requests welcome! 

Usage
=====
Step 1. Install django-ajax-uploader. 
-------------------------------------
Right now, you can either:

- Download and install, or
- `pip install -e git://github.com/GoodCloud/django-ajax-uploader.git#egg=ajaxuploader` it from here. If there's 
demand, I'll look into pypi.
- If you plan on using the Amazon S3 backend you will also need to install [boto](https://github.com/boto/boto)

	$ pip install boto


Step 2. (Django 1.3 only)
-------------------------
For Django 1.3 you will need to have the app in your installed apps tuple for collect static to pick up the files.

1. Add 'ajaxuploader' to you installed apps in settings.py

	INSTALLED_APPS = (
    	...
    	"ajaxuploader",
	)

2. Then:

	$ python manage.py collectstatic

Step 3. Include it in your app's views and urls.
------------------------------------------------
You'll need to make sure to meet the csrf requirements to still make valum's uploader work.  Code similar to the following should work:

views.py

	from django.shortcuts import render
	from ajaxuploader.views import AjaxFileUploader
	from django.middleware.csrf import get_token

	def start(request):
	    csrf_token = get_token(request)
		return render(request, 'import.html',
			{'csrf_token': csrf_token})

	import_uploader = AjaxFileUploader()
	

urls.py 

	url( r'ajax-upload$', views.import_uploader, name="my_ajax_upload"),

Step 4. Set up your template.
-----------------------------
This sample is included in the templates directory, but at the minimum, you need:

	<!doctype html> 
	<head>
		<script src="{{ STATIC_URL }}django-ajax-uploader/fileuploader.js" ></script>
		<link href="{{ STATIC_URL }}django-ajax-uploader/fileuploader.css" media="screen" rel="stylesheet" type="text/css" />
		<script>
			var uploader = new qq.FileUploader( {
			    action: "{% url my_ajax_upload %}",
			    element: $('#file-uploader')[0],
			    multiple: true,
			    onComplete: function( id, fileName, responseJSON ) {
			      if( responseJSON.success )
			        alert( "success!" ) ;
			      else
			        alert( "upload failed!" ) ;
			    },
			    onAllComplete: function( uploads ) {
			      // uploads is an array of maps
			      // the maps look like this: { file: FileObject, response: JSONServerResponse }
			      alert( "All complete!" ) ;
			    },
			    params: {
			      'csrf_token': '{{ csrf_token }}',
			      'csrf_name': 'csrfmiddlewaretoken',
			      'csrf_xname': 'X-CSRFToken',
			    },
			  }) ;
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


Backends
========

`django-ajax-uploader` can put the uploaded files into a number of places, and perform actions on the files uploaded. Currently, there are backends available for local storage (default) and Amazon S3, as well as a locally stored image thumbnail backend. Creating a custom backend is fairly straightforward, and pull requests are welcome.

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


### s3.S3UploadBackend ###

Stores the file in Amazon's S3.

Requirements:

* [boto](https://github.com/boto/boto)

Settings:

* `NUM_PARALLEL_PROCESSES` : Uploads to Amazon are parallelized to increase speed. If you have more cores and a big pipe, increase this setting for better performance. Defaults to 4.
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.

Context returned:

* None


### s3.S3UploadBackend ###

Stores a thumbnail of the locally, optionally discarding the upload.  Subclasses `LocalUploadBackend`.

Requirements:

* [sorl-thumbnail](https://github.com/sorl/sorl-thumbnail)

Settings:

* `DIMENSIONS` : A string of the dimensions (WxH) to resize the uploaded image to. Defaults to "100x100"
* `KEEP_ORIGINAL`: Whether to keep the originally uploaded file. Defaults to False.
* `BUFFER_SIZE`: The size of each chunk to write. Defaults to 10 MB.

Context returned:

* `path`: The full media path to the uploaded file.


Backend Usage
------------------------

The default backend is `local.LocalUploadBackend`. To use another backend, specify it when instantiating `AjaxFileUploader`.

For instance, to use `LocalUploadBackend`:

views.py

    from ajaxuploader.backends.local import LocalUploadBackend

    ...
    import_uploader = AjaxFileUploader(backend=LocalUploadBackend)


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
Most of the backend abstraction was written by [chromano](https://github.com/chromano) and [shockflash](https://github.com/shockflash). 


This code began as such a trivial layer on top of [valum's uploader](http://valums.com/ajax-upload/), [boto](https://github.com/boto/boto), and [alex's ideas](http://kuhlit.blogspot.com/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) it's silly.  However, I didn't find any implementations that *just worked*, so hopefully it's useful to someone else.  I also drew from these sources:

* http://www.topfstedt.de/weblog/?p=558
* http://www.elastician.com/2010/12/s3-multipart-upload-in-boto.html
* https://github.com/valums/file-uploader
* https://github.com/alexkuhl/file-uploader

Many thanks to all for writing such helpful and readable code!
