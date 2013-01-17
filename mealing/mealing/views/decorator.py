#!/bin/env python
# coding=utf-8
''' all decorator functions.

>>> resp = render_template("index.html")
>>> print resp.status_code
200
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.utils import simplejson
from django.utils.encoding import smart_str
import csv, codecs, cStringIO
import types


def render_template(template, kwargs = {}, request = None):
    """ render template
    """
    new_kwargs = {"settings": settings}
    if kwargs.has_key("settings"):
        kwargs.pop("settings")
    if request != None:
        kwargs["request"] = request
        
    new_kwargs.update(kwargs)
    if request:
        instance = RequestContext(request)
        return render_to_response(template, new_kwargs, context_instance = instance)
    return render_to_response(template, new_kwargs)


def render_json(view_func):
    """ render http response to json decorator
    """
    def wrap(request, *args, **kwargs):
        retval = view_func(request, *args, **kwargs)
        if isinstance(retval, HttpResponse):
            retval.mimetype = 'application/json'
            return retval
        else:
            json = simplejson.dumps(retval)
            return HttpResponse(json, mimetype='application/json')
    return wrap

def render_csv(view_func, encoding = "gbk"):
    """ render http response to csv
    """
    def wrap(request, *args, **kwargs):
        # data_list is list of list, for example [["a", "b"], ["a1", "a2"]]
        attachment_name, data_list = view_func(request, *args, **kwargs)
        response = HttpResponse(mimetype = "text/csv")
        response['Content-Disposition'] = u"attachment; filename=\"%s\"" % attachment_name
        writer = csv.writer(response)
        for data in data_list:
            row = []
            for cell in data:
                if not isinstance(cell, types.UnicodeType):
                    row.append(smart_str(u"%s" % cell, encoding = encoding))
                else:
                    row.append(smart_str(cell, encoding = encoding))
            writer.writerow(row)
        return response
    return wrap