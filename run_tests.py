# from https://github.com/django-extensions/django-extensions/blob/master/run_tests.py

from django.conf import settings
from django.core.management import call_command

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'ajaxuploader',
        ),
        # Django replaces this, but it still wants it. *shrugs*
        DATABASE_ENGINE = 'django.db.backends.sqlite3',
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MEDIA_ROOT = '/tmp/ajaxuploader_test_media/',
        MEDIA_PATH = '/media/',
        ROOT_URLCONF = 'ajaxuploader.urls',
        DEBUG = True,
        TEMPLATE_DEBUG = True
    )
    
    # Fire off the tests
    call_command('test', 'ajaxuploader')
    

if __name__ == '__main__':
    main()
