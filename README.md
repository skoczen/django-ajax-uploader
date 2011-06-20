`django-ajax-uploader` provides a useful class you can use to easily implement ajax uploads.

It uses valum's great uploader: https://github.com/valums/file-uploader , and draws heavy inspiration and some code from https://github.com/alexkuhl/file-uploader

In short, it implements a callable class, `AjaxFileUploader` that you can use to handle uploads.  By default, `AjaxFileUploader` assumes you want to upload to Amazon's S3, but you can select any other backend if desired or write your own (see backends section below).  Pull requests welcome! 

Usage
=====
Step 1. Install django-ajax-uploader. 
-------------------------------------
Right now, you can either:

-	Download and install, or
-	`pip install -e git://github.com/GoodCloud/django-ajax-uploader.git#egg=ajaxuploader`  it from here. If there's demand, I'll look into pypi. 

Step 2. Include it in your app's views and urls.
------------------------------------------------
You'll need to make sure to meet the csrf requirements to still make valum's uploader work.  Code similar to the following should work:

views.py

	from ajaxuploader.views import AjaxFileUploader
	from django.middleware.csrf import get_token
	@render_to("import.html")
	def start(request):
	    csrf_token = get_token( request )
	    return locals()

	import_uploader = AjaxFileUploader()


urls.py 

	url( r'ajax-upload$',                     views.import_uploader,             name="my_ajax_upload" ),

Step 3. Set up your template.
-----------------------------
This sample is included in the templates directory, but at the minimum, you need:

	<!doctype html> 
	<head>
		<script src="{{STATIC_URL}}django-ajax-uploader/fileuploader.js" ></script>
		<link href="{{STATIC_URL}}django-ajax-uploader/fileuploader.css" media="screen" rel="stylesheet" type="text/css" />
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
Backend Selection
-----------------

Backends are available in `ajaxuploader.backends`. To select the backend you want to use simply specify the `backend` parameter when instantiating `AjaxFileUploader`. For instance, if you want to the use `LocalUploadBackend` in order to store the uploaded files locally:

views.py

    from ajaxuploader.backends.local import LocalUploadBackend

    ...
    import_uploader = AjaxFileUploader(backend=LocalUploadBackend)

Each backend has its own configuration. As an example, the `LocalUploadBackend` has the constant `UPLOAD_DIR` which specifies where the files should be stored, based on `MEDIA_ROOT`. By default, the `UPLOAD_DIR` is set to `uploads`, which means the files will be stored at `MEDIA_ROOT/UPLOAD_DIR`. If you want to use an alternative place for storing the files, you need to set a new value for this constant:

    from ajaxuploader.backends.local import LocalUploadBackend

	...
	LocalUploadBackend.UPLOAD_DIR = "tmp"
    import_uploader = AjaxFileUploader(backend=LocalUploadBackend)

Similarly, the `ThumbnailUploadBackend` has the constant `DIMENSION`, which determines the dimension of the thumbnail image that will be created. The string format for this constant is the same as for `sorl-thumbnail`.

Backends Available
------------------

The following backends are available:

* `local.LocalUploadBackend`: Store the file locally. You can specify the directory where files will be saved through the `UPLOAD_DIR` constant. This backend will also include in the response sent to the client a `path` variable with the path in the server where the file can be accessed.
* `s3.S3UploadBackend`: Store the file in Amazon S3.
* `thumbnail.ThumbnailUploadBackend`: Depends on `sorl-thumbnail`. Used for images upload that needs re-dimensioning/cropping. Like `LocalUploadBackend`, it includes in the response a `path` variable pointing to the image in the server. The image dimension can be set through `ThumbnailUploadBackend.DIMENSION`, by default it is set to "100x100".

Customization
-------------

In order to write your custom backend, you need to inherit from `backends.base.AbstractUploadBackend` and implement the `upload_chunk` method, which will receive the string representing a chunk of data that was just read from the client. The following methods are optional and should be implement if you want to take advantage of their purpose:

* `setup`: given the original filename, do any pre-processing needed before uploading the file (for example, for S3 backend, this method is used to establish a connection with S3 server).
* `update_filename`: given the `request` object and the original name of the file being updated, returns a new filename which will be used to refer to the file being saved, also this filename will be returned to the client.
* `upload_complete`: receives the `request` object and the updated filename (as described on `update_filename`) and do any processing needed after upload is complete (like croping the image or disconnecting from the server). If a dict is returned, it is used to update the response returned to the client.


Caveats
=======
One note on changing `BUFFER_SIZE` - some users have reported problems using smaller buffer sizes.  I also saw random failed uploads with very small sizes like 32k.  10MB has been completely reliable for me, and in what I've read here and there, so do some testing if you want to try a different value.  Note that this doesn't have a big impact on the overall upload speed.


Credits
=======
This code is such a trivial layer on top of [valum's uploader](http://valums.com/ajax-upload/), [boto](https://github.com/boto/boto), and [alex's ideas](http://kuhlit.blogspot.com/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) it's silly.  However, I didn't find any implementations that *just worked*, so hopefully it's useful to someone else.  I also drew from these sources:

* http://www.topfstedt.de/weblog/?p=558
* http://www.elastician.com/2010/12/s3-multipart-upload-in-boto.html
* https://github.com/valums/file-uploader
* https://github.com/alexkuhl/file-uploader

Many thanks to all for writing such helpful and readable code!
