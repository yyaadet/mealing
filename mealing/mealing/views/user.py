#!/bin/env python
# coding=utf-8
''' user view functions.

# test login
>>> from django.test.client import Client
>>> from django.contrib.auth.models import User as DjangoUser
>>> c = Client()
>>> resp = c.get("/login/")
>>> print resp.status_code
200
>>> print resp.context["form"] != None
True
>>> resp = c.post("/login/", {"username": "1111", "password": "222"})
>>> print (resp.context["form"].custom_error != "")
True
>>> u = DjangoUser.objects.create_user("loginu", "u1@funshion.com", "1111")
>>> resp = c.post("/login/", {"username": "loginu", "password": "1111"})
>>> print resp.status_code 
302
>>> c.login(username = "loginu", password = "1111")
True
>>> resp = c.post("/login/")
>>> print resp.status_code
302

# test logout
>>> resp = c.get("/logout/")
>>> print resp.status_code
302
'''

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.models import User as DjangoUser
from django import forms
from mealing.views.decorator import render_template
from mealing.views import index
from mealing.forms import LoginForm
from mealing.forms.base import DivErrorList
import logging


logger = logging.getLogger(__name__)

@csrf_protect
def login(request):
    """ login view.
    """
    logger.info("request method is %s" % request.method)
    if request.user.is_authenticated():
        logger.info("you have logined")
        return redirect("/")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            is_remember = form.cleaned_data["is_remember"]
            user = authenticate(username = username, password = password)
            if user == None:
                form.set_custom_error(u"用户不存在或是密码错误")
                logger.info("user's password is error: %s" % form.non_field_errors())
                return render_template("login.html", {"form": form}, request)
            djangologin(request, user)
            return redirect("/")
        else:
            logger.info("form is not valid")
    else:
        form = LoginForm()
        
    return render_template("login.html", {"form": form}, request)

def logout(request):
    """ logout view
    """
    djlogout(request)
    return redirect("/")