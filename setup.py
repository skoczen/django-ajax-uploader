#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name = "ajaxuploader",
    version = "0.1",
    packages = find_packages(),
    package_data ={'ajaxuploader':   ['static/ajaxuploader/js/fileuploader.js', 'static/ajaxuploader/css/fileuploader.css']},
    zip_safe = False,
)
