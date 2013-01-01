#!/bin/env python
# coding=utf-8
""" home page functions.

>>> from django.test.client import Client
>>> c = Client()
>>> resp = c.get("/")
>>> print resp.status_code
200
>>> print (resp.context["settings"] != None)
True
"""

from django.shortcuts import render_to_response
from mealing.views.decorator import render_template

def index(request):
    """ site index
    """
    return render_template("index.html", request = request)