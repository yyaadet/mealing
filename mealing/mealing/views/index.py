#!/bin/env python
# coding=utf-8
''' index page functions.
'''

from django.shortcuts import render_to_response
from mealing.views.decorator import render_template

def index(request):
    """ site index
    >>> from django.test.client import Client
    >>> c = Client()
    >>> resp = c.get("/")
    >>> print resp.status_code
    200
    >>> print (resp.context["settings"] != None)
    True
    """
    return render_template("index.html")