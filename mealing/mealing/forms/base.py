#!/bin/env python
# coding=utf-8
''' base form define.
'''

from django.forms.util import ErrorList
from django import forms
from django.utils.safestring import mark_safe

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    
    def as_divs(self):
        if not self:
            return u""
        return u'<div class="alert">%s</div>' % ''.join([u'<div class="alert-error">%s</div>' % e for e in self])
    
    def as_ul(self):
        return self.as_divs()
    
class BasisForm(forms.Form):
    """ basis form class.
    """
    _custom_error = ""
    _success_tips = ""
    
    @property
    def custom_error(self):
        if self._custom_error == "":
            return ""
        return mark_safe(u"<div class=\"alert\">%s</div>" % self._custom_error)
    
    def set_custom_error(self, msg):
        self._custom_error = msg
        
    @property
    def success_tips(self):
        if self._success_tips == "":
            return ""
        return mark_safe(u"<div class=\"alert alert-success\">%s</div>" % self._success_tips)