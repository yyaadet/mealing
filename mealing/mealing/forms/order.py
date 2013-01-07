#!/bin/env python
# coding=utf-8
''' all forms about order.
'''

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import User as DjangoUser
from mealing.forms import base


def validate_receivers(value):
    """ validate receivers
    """
    if value.strip() == "":
        raise ValidationError(u"这个字段不能为空")
    # check user
    receiver_names = value.split(" ")
    for name in receiver_names:
        u = DjangoUser.objects.filter(username=name)
        if not u:
           raise ValidationError(u"%s 不是一个有效的用户名" % name)
       
       
class CommitOrderForm(base.BasisForm):
    """ user commit order form.
    >>> data = {"receivers": "aaa; bbbb;"}
    >>> f = CommitOrderForm(data)
    >>> print f.is_valid()
    False
    """
    text_style = {"class": "input-block-level", "placeholder": "", "row": 3, "id": "receivers_input"}
    receivers = forms.CharField(max_length = 1024, required = True, 
                                widget = forms.TextInput(attrs=text_style), 
                                validators = [validate_receivers],
                                help_text = u"多个领餐人以空格分隔，例如：\"pengxt tanj hucj\"")
