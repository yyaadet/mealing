#!/bin/env python
# coding=utf-8
''' user view functions.
'''

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User as DjangoUser
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
    >>> resp = c.post("/login", {"username": "pengxt", "password": "pengxt"})
    >>> print resp.status_code
    301
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            is_remember = form.cleaned_data["is_remember"]
            if DjangoUser.objects.get(username = username) == None:
                form = LoginForm()
                form.errors["status"] = u"用户名不存在"
                return render_template("login.html", {"form": form})
            user = authenticate(username, password)
            if user == None:
                form = LoginForm()
                form.errors["status"] = u"密码错误"
                return render_template("login.html", {"form": form})
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()
        
    return render_template("login.html", {"form": form})