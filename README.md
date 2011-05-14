`django-ajax-uploader` provides a useful class you can use to easily implement ajax uploads.

It uses valum's great uploader: http://valums.com/ajax-upload/,and draws heavy inspiration and some code from https://github.com/alexkuhl/file-uploader

In short, it implements a callable class, `AjaxFileUploader` that you can subclass use to handle uploads.  By default, `AjaxFileUploader` assumes you want to upload to Amazon's S3, but can be subclassed to change this behavior if desired.  Pull requests welcome! 

Usage
=====
Step 1. Install django-ajax-uploader. 
-------------------------------------
Right now, you can either:
* Download and install, or
* `pip install -e git://github.com/GoodCloud/django-ajax-uploader.git#egg=ajaxuploader`  it from here. If there's demand, I'll look into pypi. 

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

Step 4. Subclass and override if needed.
----------------------------------------
That's all you need to get rolling. However, it's likely you actually want to do something with those files the user just uploaded. For that, you can subclass AjaxFileUploader, and override functions and constants.  AjaxFileUploader has a fair bit of configurability.  The example below shows all of the most common functions and constants redefined.

	class MyAjaxFileUploader(AjaxFileUploader):
		NUM_PARALLEL_PROCESSES = 48   		# Your servers are way better than mine
	    BUFFER_SIZE = 10485760  # 100MB		# In the future, 10 MB is nothing. 

	    def _update_filename(self, request, filename):
	    	# This example timestamps the filename, so we know they're always unique.
	        import time
	        return "import/%s.%s" % (int(time.time()), filename,)

	    def _upload_complete(self, request, filename):
	        print "Save the fact that %s's upload was completed to the database, and do important things!"  % filename

	my_uploader = MyAjaxFileUploader()


Advanced Usage / Not uploading to S3
====================================
At the moment, ajax-upload is built for s3.  However, you can easily redefine the `_save_upload` method, and save the stream/file wherever you'd like.  Pull requests are welcome for further abstraction.


Caveats
=======
One note on changing `BUFFER_SIZE` - some users have reported problems using smaller buffer sizes.  I also saw random failed uploads with very small sizes like 32k.  10MB has been completely reliable for me, and in what I've read here and there, so do some testing if you want to try a different value.  Note that this doesn't have a big impact on the overall upload speed.


Credits
=======
This code is such a trivial layer on top of [valum's uploader](http://valums.com/ajax-upload/), [boto](https://github.com/boto/boto), and [alex's ideas](http://kuhlit.blogspot.com/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) it's silly.  However, I didn't find any implementations that *just worked*, so hopefully it's useful to someone else.  I also drew from these sources:

* http://www.topfstedt.de/weblog/?p=558
* http://www.elastician.com/2010/12/s3-multipart-upload-in-boto.html

Many thanks to all for writing such helpful and readable code!
