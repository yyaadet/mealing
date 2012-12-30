#!/bin/env python
# coding=utf-8
''' base form define.
'''

from django.forms.util import ErrorList
from django import forms

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    
    def as_divs(self):
        if not self:
            return u""
        return u'<div class="alert">%s</div>' % ''.join([u'<div class="alert-error">%s</div>' % e for e in self])
    
    def as_ul(self):
        return self.as_divs()