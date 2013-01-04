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

# test register()
>>> c.logout()
>>> resp = c.get("/register/")
>>> print resp.status_code
200
>>> resp = c.post("/register/", {"username": "t11111", "password": "1111", "email": "pengxt@funshion.com"})
>>> print resp.status_code
302
>>> c.logout()
>>> resp = c.post("/register/", {"username": "t11111", "password": "1111", "email": "pengxt@funshion.com"})
>>> print resp.status_code
200
>>> print resp.context["form"].custom_error != ""
True

# test change_password()
>>> c.login(username = "loginu", password = "1111")
True
>>> resp = c.post("/change_password/", {"old_password": "2222", "new_password": "111", "new_password1": "333"})
>>> print resp.context["form"].custom_error != ""
True
>>> resp = c.post("/change_password/", {"old_password": "1111", "new_password": "111", "new_password1": "333"})
>>> print resp.context["form"].custom_error != ""
True
>>> resp = c.post("/change_password/", {"old_password": "1111", "new_password": "3333", "new_password1": "3333"})
>>> c.logout()
>>> print c.login(username = "loginu", password = "3333")
True
'''

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django import forms
from mealing.views.decorator import render_template
from mealing.views import index
from mealing.forms import LoginForm, RegisterForm, ChangePasswordForm
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

def register(request):
    """ user register view
    """
    if request.user.is_authenticated():
        return redirect("/")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            if DjangoUser.objects.filter(username = username).count() > 0:
                form.set_custom_error(u"用户名或已被他人注册")
                return render_template("register.html", {"form": form}, request)
            try:
                user = DjangoUser.objects.create_user(username, email, password)
            except Exception, e:
                logging.warn("failed to register: %s" % e)
                form.set_custom_error(u"系统发生故障")
                return render_template("register.html", {"form": form}, request)
            user = authenticate(username = username, password = password)
            djangologin(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
        
    return render_template("register.html", {"form": form}, request)

@login_required
def change_password(request):
    """ change user password
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            new_password1 = form.cleaned_data["new_password1"]
            if request.user.check_password(old_password):
                form.set_custom_error(u"密码不对")
                return render_template("change_password.html", {"form": form}, request)
            if new_password != new_password1:
                form.set_custom_error(u"两次输入密码不一致")
                return render_template("change_password.html", {"form": form}, request)
            request.user.set_password(new_password)
            request.user.save()
    else:
        form= ChangePasswordForm()
    return render_template("change_password.html", {"form": form}, request)