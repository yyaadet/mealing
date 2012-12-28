#!/bin/env python
# coding=utf-8
''' all decorator functions.
'''

from django.conf import settings
from django.shortcuts import render_to_response

def render_template(template, kwargs = {}):
    """ render template
    >>> render_template("index.html")
    """
    new_kwargs = {"settings": settings}
    if kwargs.has_key("settings"):
        kwargs.pop("settings")
        
    new_kwargs.update(kwargs)
    
    return render_to_response(template, new_kwargs)
    