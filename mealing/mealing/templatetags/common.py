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
                           {"name": u"今日订餐", "url": "/order/today/"},
                           {"name": u"排行榜", "url": "/rank/pop_menu/"},
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
    
def do_nav_list(parser, token):
    """ show navigate list at left of page.
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, nav = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0]) 
    if not (nav[0] == nav[-1] and nav[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return NavListNode(nav[1:-1])

class NavListNode(template.Node):
    """ render nav list template tag
    """
    def __init__(self, cur_nav): 
        """ init function
        
        Args:
            cur_tab: current page tab
        """
        self.nav_header = u"排行榜"
        self._cur_nav = cur_nav
        self._navs = [{"name": u"活跃用户", "url": "#"},
                      {"name": u"流行菜品", "url": "/rank/pop_menu/"},
                      {"name": u"新增菜品", "url": "/rank/newly_menu/"},
                      {"name": u"Wilson菜品", "url": "/rank/wilson_menu/"},
                      ]
        
    def render(self, context):
        """ so import function. render tag now.
        """
        t = template.loader.get_template("tags/nav_list.html")
        navs = []
        for nav in self._navs:
            if nav["name"] == self._cur_nav:
                nav["is_active"] = 1
            navs.append(nav)
        new_context = Context({'navs': navs, "nav_header": self.nav_header}, autoescape=context.autoescape)
        return t.render(new_context)
    
def do_restaurant_list(parser, token):
    """ restaurant nav list at left
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, restaurant, restaurants = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0]) 
    if restaurant[0] != restaurant[-1] and restaurant[0] in ('"', "'"):
        raise template.TemplateSyntaxError("%r tag's second argument should be in quotes" % tag_name)
    return RestaurantListNode(restaurant, restaurants)

class RestaurantListNode(template.Node):
    """ restaurant nav list node.
    """
    def __init__(self, restaurant, restaurants):
        """ init node.
        """
        self.restaurant = template.Variable(restaurant)
        self.restaurants = template.Variable(restaurants)
    
    def render(self, context):
        """ render pagination from template.
        """
        logging.debug("restaurant is %s" % self.restaurant.resolve(context))
        restaurants = self.restaurants.resolve(context)
        new_restaurants = [{"name": restaurant.name, 
                            "url": "/order/today/%d/" % restaurant.id, 
                            "id": restaurant.id} for restaurant in restaurants]
        
        t = template.loader.get_template("tags/restaurant_list.html")
        new_context = Context({"restaurant": self.restaurant.resolve(context), 
                               "restaurants": new_restaurants}, 
                              autoescape=context.autoescape)
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
register.tag("nav_list", do_nav_list)
register.tag("restaurant_list", do_restaurant_list)
register.tag("pagination", do_pagination)