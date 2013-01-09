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


def do_nav(parser, token):
    """ show navigate at header of page.
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, tab = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0]) 
    if not (tab[0] == tab[-1] and tab[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return NavNode(tab[1:-1])

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
                           {"name": u"餐厅", "url": "/restaurant/all/"},
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
        new_context = Context({'tabs': tabs}, autoescape=context.autoescape)
        return t.render(new_context)
    
def do_pagination(parser, token):
    """ pagination at bottom
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, pager, prefix = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0]) 
    if prefix[0] != prefix[-1] and prefix[0] in ('"', "'"):
        raise template.TemplateSyntaxError("%r tag's second argument should be in quotes" % tag_name)
    return PaginationNode(pager, prefix)

class PaginationNode(template.Node):
    """ pagination node.
    """
    def __init__(self, pager, prefix):
        """ init pagination node.
        Args:
            pager: Paginator.page() object
            prefix: url prefix
        """
        self._pager = template.Variable(pager)
        self._prefix = template.Variable(prefix)
    
    def render(self, context):
        """ render pagination from template.
        """
        t = template.loader.get_template("tags/pagination.html")
        new_context = Context({"pager": self._pager.resolve(context), "prefix": self._prefix.resolve(context)}, 
                              autoescape=context.autoescape)
        return t.render(new_context)

register.tag("nav", do_nav)
register.tag("pagination", do_pagination)