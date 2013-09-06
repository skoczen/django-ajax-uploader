# Via Fine-uploader's server examples.
# MIT License https://github.com/Widen/fine-uploader-server/blob/master/license.txt
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import base64, hmac, hashlib, json

try:
    import boto
    from boto.s3.connection import Key, S3Connection
    boto.set_stream_logger('boto')
    S3 = S3Connection(settings.AWS_UPLOAD_CLIENT_KEY, settings.AWS_UPLOAD_CLIENT_SECRET_KEY)
except ImportError, e:
    print("Could not import boto, the Amazon SDK for Python.")
    print("Deleting files will not work.")
    print("Install boto with")
    print("$ pip install boto")


def home(request):
    """ The 'home' page. Returns an HTML page with Fine Uploader code
    ready to upload to S3.
    """
    return render(request, "index.html")


@csrf_exempt
def success_redirect_endpoint(request):
    """ This is where the upload will snd a POST request after the
    file has been stored in S3.
    """
    return make_response(200)


@csrf_exempt
def handle_s3(request):
    """ View which handles all POST and DELETE requests sent by Fine Uploader
    S3. You will need to adjust these paths/conditions based on your setup.
    """
    if request.method == "POST":
        return handle_POST(request)
    elif request.method == "DELETE":
        return handle_DELETE(request)
    else:
        return HttpResponse(status=405)


def handle_POST(request):
    """ Handle S3 uploader POST requests here. For files <=5MiB this is a simple
    request to sign the policy document. For files >5MiB this is a request
    to sign the headers to start a multipart encoded request.
    """
    if request.POST.get('success', None):
        return make_response(200)
    else:
        request_payload = json.loads(request.body)
        headers = request_payload.get('headers', None)
        if headers:
            # The presence of the 'headers' property in the request payload
            # means this is a request to sign a REST/multipart request
            # and NOT a policy document
            response_data = sign_headers(headers)
        else:
            response_data = sign_policy_document(request_payload)
        response_payload = json.dumps(response_data)
        return make_response(200, response_payload)


def handle_DELETE(request):
    """ Handle file deletion requests. For this, we use the Amazon Python SDK,
    boto.
    """
    if boto:
        bucket_name = request.REQUEST.get('bucket')
        key_name = request.REQUEST.get('key')
        aws_bucket = S3.get_bucket(bucket_name, validate=False)
        aws_key = Key(aws_bucket, key_name)
        aws_key.delete()
        return make_response(200)
    else:
        return make_response(500)


def make_response(status=200, content=None):
    """ Construct an HTTP response. Fine Uploader expects 'application/json'.
    """
    response = HttpResponse()
    response.status_code = status
    response['Content-Type'] = "application/json"
    response.content = content
    return response


def is_valid_policy(policy_document):
    """ Verify the policy document has not been tampered with client-side
    before sending it off.
    """
    #bucket = settings.AWS_UPLOAD_BUCKET_NAME
    #parsed_max_size = settings.AWS_MAX_SIZE
    bucket = ''
    parsed_max_size = 0

    for condition in policy_document['conditions']:
        if isinstance(condition, list) and condition[0] == 'content-length-range':
            parsed_max_size = condition[2]
        else:
            if condition.get('bucket', None):
                bucket = condition['bucket']

    return bucket == settings.AWS_UPLOAD_BUCKET_NAME and parsed_max_size == settings.AWS_MAX_SIZE


def sign_policy_document(policy_document):
    """ Sign and return the policy doucument for a simple upload.
    http://aws.amazon.com/articles/1434/#signyours3postform
    """
    policy = base64.b64encode(json.dumps(policy_document))
    signature = base64.b64encode(hmac.new(settings.AWS_UPLOAD_CLIENT_SECRET_KEY, policy, hashlib.sha1).digest())
    return {
        'policy': policy,
        'signature': signature
    }


def sign_headers(headers):
    """ Sign and return the headers for a chunked upload. """
    return {
        'signature': base64.b64encode(hmac.new(settings.AWS_UPLOAD_CLIENT_SECRET_KEY, headers, hashlib.sha1).digest())
    }
