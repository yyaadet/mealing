#!/bin/env python
# coding=utf-8
''' all forms about user. for example, login, reset_password, register etc...
'''

from django import forms


class LoginForm(forms.Form):
    """ user login form.
    >>> from mealing.forms.base import DivErrorList
    >>> data = {"username": ""}
    >>> f = LoginForm(data, error_class = DivErrorList)
    >>> print f.is_valid()
    False
    >>> err = f["username"].errors.__unicode__()
    >>> print err.find("div") > -1
    True
    """
    username = forms.CharField(max_length = 30, required = True)
    password = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    is_remember = forms.BooleanField()