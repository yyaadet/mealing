#!/bin/env python
# coding=utf-8
''' myself template tags
'''

from django import template
from django.template import Context
import logging


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

register = template.Library()

@register.tag(name = "nav")
def do_nav(parser, token):
    """ show navigate at header of page.
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0]) 
    if (not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'"))) and \
            (not (format_string[1] == format_string[-1] and format_string[0] == 'u')):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return NavNode(format_string[1:-1])

class NavNode(template.Node):
    """ render nav template tag
    """
    def __init__(self, cur_tab): 
        """ init function
        
        Args:
            cur_tab: current page tab
        """
        self._cur_tab = cur_tab
        self._tabs = [{"name": u"主页", "url": "/"},
                           {"name": u"排行榜", "url": "#"},
                           {"name": u"今日订餐", "url": "#"},
                      ]
        
    def render(self, context):
        """ so import function. render tag now.
        """
        t = template.loader.get_template("tags/nav.html")
        tabs = []
        for tab in self._tabs:
            if tab["name"] == self._cur_tab:
                tab["is_active"] = 1
            tabs.append(tab)
        logging.debug("tabs: %s\ncurrent tab: %s" % (tabs, self._cur_tab))
        new_context = Context({'tabs': tabs}, autoescape=context.autoescape)
        return t.render(new_context)