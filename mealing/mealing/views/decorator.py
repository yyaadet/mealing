#!/bin/env python
# coding=utf-8
''' all decorator functions.

>>> resp = render_template("index.html")
>>> print resp.status_code
200
'''

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_template(template, kwargs = {}, request = None):
    """ render template
    """
    new_kwargs = {"settings": settings}
    if kwargs.has_key("settings"):
        kwargs.pop("settings")
    if request != None:
        kwargs["request"] = request
        
    new_kwargs.update(kwargs)
    if request:
        instance = RequestContext(request)
        return render_to_response(template, new_kwargs, context_instance = instance)
    return render_to_response(template, new_kwargs)