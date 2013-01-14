#!/bin/env python
# coding=utf-8
"""Bayesian average
>>> bay1 = Bayesian(100, 300, 2.5)
>>> bay2 = Bayesian(50, 300, 2.5)
>>> print bay1.score > bay2.score
True
"""


__author__ = 'yyaadet <yyaadet2002@gmail.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from base import Base
import math


class Bayesian(Base):
    def __init__(self, vote_number, vote_point, entire_avg_point, extend_vote_number = 300):
        """  Bayesian average
        Args:
            vote_number: the number of vote
            vote_point: total point of vote
            entire_avg_point: entire average point by all people
            extend_vote_number: user can set by self. you should use average vote of every item.
        """
        self.vote_number = vote_number
        self.vote_point = vote_point
        self.entire_avg_point = entire_avg_point
        self.extend_vote_number = extend_vote_number
        
    @property
    def score(self):
        if self.vote_number <= 0:
            self.vote_number += 1
        score = 1.0*(self.vote_number * self.entire_avg_point + self.vote_point) / (self.vote_number + self.extend_vote_number)
        return score