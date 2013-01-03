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
    # forms
    "mealing.forms.user",
    "mealing.forms.base",
    # templatetags
    "mealing.templatetags.common",
]

LIST_OF_UNITTESTS = [
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
        
        
