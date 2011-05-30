'''contains utility modules and classes

e.g. sine-controllers, a custom-dict class, etc. '''
from math import log
from random import random


def random_between(min_, max_, center=0.5):
    if center == 0.5:
        return (random() * (max_ - min_)) + min_
    else:
        return (random() ** log(center, 0.5) * (max_ - min_)) + min_
