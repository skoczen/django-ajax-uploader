Django Fine Uploader DEMO
=============

Demonstration of how to use the django-ajax-uploader module

**With Fig/Docker**

    fig up
    
    #in another terminal
    fig run web syncdb
    fig run web collectstatic

Navigate to localhost:8080/start and go nuts!

**Without Fig**
If you dont have postgres installed in your environment this can easily be run with an sqlite database

Set environment variables
    export AWS_UPLOAD_CLIENT_SECRET_KEY {{ YOUR_SECRET }}
    export AWS_UPLOAD_CLIENT_KEY {{ YOUR_ID }} 
    export AWS_EXPECTED_BUCKET {{ YOUR_BUCKET }} 
    export AWS_EXPECTED_SIZE 15000000

Install dependencies
    pip install -r requirements.txt

Set up your database
    ./manage.py syncdb

Consolodate static files
    ./manage.py collectstatic

Run yo server!
    ./manage.py runserver 0.0.0.0:8080
