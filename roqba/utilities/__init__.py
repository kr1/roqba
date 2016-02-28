'''contains utility modules and classes

e.g. sine-controllers, a custom-dict class, etc. '''
from math import log
from random import random


def random_between(min_, max_, center=0.5):
    if center == 0.5:
        return (random() * (max_ - min_)) + min_
    else:
        return (random() ** log(center, 0.5) * (max_ - min_)) + min_


def project_scale(current, in_start, in_end, target_start, target_end):
    in_distance = in_end - in_start
    in_pos = (current - in_start) / in_distance
    out_distance = target_end - target_start
    #return target_start + (in_pos * out_distance)
    return target_start + ((current - in_start) / (in_end - in_start)) * (target_end - target_start)
