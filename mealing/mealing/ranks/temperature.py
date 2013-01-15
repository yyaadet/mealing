#!/bin/env python
# coding=utf-8
""" temperature rank algorithm. Example, Hacker News etc.

>>> temp = Temperature(0, 1)
>>> base_score = temp.score
>>> temp1 = Temperature(0, 4)
>>> print temp1.score < base_score
True
>>> temp2 = Temperature(10, 4)
>>> print temp2.score > base_score
True
"""

__author__ = 'yyaadet <yyaadet2002@gmail.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from base import Base


class Temperature(Base):
    """ News is suitable for it.
    """
    def __init__(self, vote_number, distance, gravityth_power = 1.8):
        """
        Args:
            vote_number: user vote number
            distance: how long object published
            gravityth_power: gravityth power. So bigger, so quickly to down.
        """
        self.gravityth_power = gravityth_power
        self.vote_number = vote_number
        self.distance = distance
        
    @property
    def score(self):
        if self.vote_number <= 1:
            self.vote_number += 2
        score = 1.0*(self.vote_number - 1) / pow(self.distance + 2, self.gravityth_power)
        return score