#!/bin/env python
# coding=utf-8
''' user view functions.
'''

from django.shortcuts import render_to_response
from mealing.views.decorator import render_template
from mealing.forms import LoginForm
from mealing.forms.base import DivErrorList

def login(request):
    """ login view.
    >>> from django.test.client import Client
    >>> c = Client()
    >>> resp = c.get("/login/")
    >>> print resp.status_code
    200
    >>> print resp.context["form"] != None
    True
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = LoginForm(error_class = DivErrorList)
        
    return render_template("login.html", {"form": form})