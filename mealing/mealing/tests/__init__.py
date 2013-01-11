#!/bin/env python
# coding=utf-8
'''test definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


import unittest
import doctest
from django.test import TestCase
from django.test._doctest import DocTestSuite

     
LIST_OF_DOCTESTS = [
    # models
    "mealing.models.restaurant",
    "mealing.models.order",
    "mealing.models.user",
    "mealing.models.config",
    "mealing.models",
    # views
    "mealing.views.decorator",
    "mealing.views.home",
    "mealing.views.user",
    "mealing.views.restaurant",
    "mealing.views.menu",
    "mealing.views.order",
    # forms
    "mealing.forms.user",
    "mealing.forms.base",
    "mealing.forms.order",
    # templatetags
    "mealing.templatetags.common",
    # utils
    "mealing.utils.email",
    "mealing.utils.date",
]

LIST_OF_UNITTESTS = [
    "mealing.tests.order",
]

def suite():
    suite = unittest.TestSuite()
    for t in LIST_OF_DOCTESTS:
        suite.addTest(DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    for t in LIST_OF_UNITTESTS:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    return suite
        
        
