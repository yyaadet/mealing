#!/bin/env python
# coding=utf-8
''' all forms about user. for example, login, reset_password, register etc...
'''

from django import forms
from mealing.models import Department
from mealing.forms import base


class LoginForm(base.BasisForm):
    """ user login form.
    >>> from mealing.forms.base import DivErrorList
    >>> data = {"username": ""}
    >>> f = LoginForm(data, error_class = DivErrorList)
    >>> print f.is_valid()
    False
    >>> err = f["username"].errors.__unicode__()
    >>> print err.find("div") > -1
    True
    >>> f1 = LoginForm(data)
    >>> print f1.as_table().find("text-error") > -1
    True
    """
    error_css_class = "text-error"
    required_css_class= "text-error"
    username = forms.CharField(max_length = 30, required = True)
    password = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    is_remember = forms.BooleanField(required = False)
    
class RegisterForm(base.BasisForm):
    """user register form
    >>> form = RegisterForm()
    >>> print form.is_valid()
    False
    """
    username = forms.CharField(max_length = 30)
    password = forms.CharField(max_length = 30, widget = forms.PasswordInput)
    email = forms.EmailField(max_length = 60)
    real_name = forms.CharField(max_length = 30)
    department = forms.ModelChoiceField(queryset = Department.objects.all(), empty_label = u"请选择部门")
    
class ChangePasswordForm(base.BasisForm):
    """ user change password form
    """
    old_password = forms.CharField(max_length = 30, widget = forms.PasswordInput)
    new_password = forms.CharField(max_length = 30, widget = forms.PasswordInput)
    new_password1 = forms.CharField(max_length = 30, widget = forms.PasswordInput)