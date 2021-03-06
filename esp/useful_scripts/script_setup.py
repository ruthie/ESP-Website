#!/usr/bin/env python

import os, sys

useful_scripts = os.path.dirname(os.path.realpath(__file__))
project = os.path.dirname(useful_scripts)
sys.path.append(project)

# activate virtualenv
envroot = os.path.dirname(project)
activate_this = os.path.join(envroot, 'env', 'bin', 'activate_this.py')
try:
    execfile(activate_this, dict(__file__=activate_this))
except IOError, e:
    # Check if a virtualenv has been installed and activated from elsewhere.
    # If this has happened, then the VIRTUAL_ENV environment variable should be
    # defined, and we can ignore the IOError.
    # If the variable isn't defined, then we really should be using our own
    # virtualenv, so we re-raise the error.
    if os.environ.get('VIRTUAL_ENV') is None:
        raise e

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esp.settings")

from django.db.models.loading import get_models
from django.conf import settings as S

# http://sontek.net/blog/detail/tips-and-tricks-for-the-python-interpreter
for m in get_models():
    globals()[m.__name__] = m

from esp.utils.shell_utils import *
