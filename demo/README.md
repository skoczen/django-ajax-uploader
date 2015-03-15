Django Ajax Uploader Demo
=============

Here are some "real-world" implementations of this project to give a clear starting point for adding ajax file uploads to your django projects.  This demo includes two different routes for starting these demos in several commands using [Docker](http://docker.io/) or [Vagrant](http://vagrantup.com) / [Packer](http://packer.io).

As it's clever to have your config in environment variables, this demo requires you to set them.  They are;
    AWS_UPLOAD_CLIENT_SECRET_KEY (your aws_secret_key)
    AWS_UPLOAD_CLIENT_KEY (your aws_access_key)
    AWS_EXPECTED_BUCKET (name of your bucket)
    AWS_EXPECTED_SIZE (Size of your bucket for validation)


**With Fig/Docker (easiest)**

    # Populate env variables in the Dockerfile then...
    fig up
    # in another terminal...
    fig run --rm web syncdb
    fig run --rm web collectstatic
    # to watch the logs...
    docker logs --follow
    # Django is now running on localhost:8080

Navigate to localhost:8080/start and go nuts!

**With Vagrant / [django-dev-box](http://github.com/derek-adair/django-dev-box) (requires virtualbox / NFS ready system)**
    git clone git@github.com:derek-adair/django-dev-box.git && cd django-dev-box
    #optionally bake your env vars into the vagrant box, see [env_vars.exampple.sh](https://github.com/derek-adair/django-dev-box/blob/master/core/files/env_vars.example.sh)
    ./create_box
    vagrant init derek-adair/django-dev-box
    vagrant up && vagrant ssh
    # If you didn't set your env vars in packer, you need to export them in your provisioned VM at this point.
    ./manage.py syncdb
    ./manage.py runserver 0.0.0.0:8080
    # Django is now running on localhost:8080 - note that my vagrant box is configured to auto-forward this port if its already taken

**Vanilla Install**

Requires python 2.7 / pip / Postgres.  If you dont have postgres installed in your environment this can easily be run with an sqlite database

Set environment variables

    export AWS_UPLOAD_CLIENT_SECRET_KEY {{ YOUR_SECRET }}
    export AWS_UPLOAD_CLIENT_KEY {{ YOUR_ID }} 
    export AWS_EXPECTED_BUCKET {{ YOUR_BUCKET }} 
    export AWS_EXPECTED_SIZE 15000000

*Install dependencies*

    pip install -r requirements.txt

*Set up your database*

    ./manage.py syncdb

*Consolodate static files*

    ./manage.py collectstatic

*Run yo server!*

    ./manage.py runserver 0.0.0.0:8080
