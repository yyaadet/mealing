#!/bin/env python
# coding=utf-8
"""The Wilson interval is an improvement (the actual coverage probability is closer to the nominal value) 
over the normal approximation interval and was first developed by Edwin Bidwell Wilson (1927).[2]

This interval has good properties even for a small number of trials and/or an extreme probability. 
The center of the Wilson interval can be shown to be a weighted average of  and , 
with  receiving greater weight as the sample size increases. For the 95% interval, 
the Wilson interval is nearly identical to the normal approximation interval using  instead of .
The Wilson interval can be derived from Pearson's chi-squared test with two categories. The resulting interval can then be solved for  to produce the Wilson interval.
The test in the middle of the inequality is a score test, so the Wilson interval is sometimes called the Wilson score interval.

>>> wilson1 = Wilson(20, 100)
>>> wilson2 = Wilson(2, 10)
>>> print wilson1.score > wilson2.score
True
"""


__author__ = 'yyaadet <yyaadet2002@gmail.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from base import Base
import math


class Wilson(Base):
    def __init__(self, good_number, total_sample, z = 1.96):
        """  default confidence is 95%. z equal 1.96
        """
        self.good_number = good_number
        self.total_sample= total_sample
        self.z = z
        
    @property
    def score(self):
        if self.total_sample <= 0:
            return 0
        phat = 1.0*self.good_number/self.total_sample
        z = self.z
        n = self.total_sample
        score = (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n)) / (1+z*z/n)
        return score