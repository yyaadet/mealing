#!/bin/env python
# coding=utf-8
''' all decorator functions.
'''

from django.conf import settings
from django.shortcuts import render_to_response

def render_template(*args, **kwargs):
    """ render template
    >>> render_template("index.html")
    """
    if (not kwargs.has_key("settings")):
        kwargs["settings"] = settings
        
    return render_to_response(args, kwargs)
    