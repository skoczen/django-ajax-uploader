#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name = "ajaxuploader",
    description = "AJAX file uploader for django",
    author = "Steven Skoczen",
    author_email = "steven@agoodcloud.com",
    url = "https://github.com/GoodCloud/django-ajax-uploader",
    version = "0.2.4",
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
)
