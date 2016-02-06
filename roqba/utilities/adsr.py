from random import random


def get_random_adsr(min_adsr, max_adsr):
    return [random() * (max_adsr[index] - min_adsr[index]) + min_adsr[index]
            for index in range(len(max_adsr))]
