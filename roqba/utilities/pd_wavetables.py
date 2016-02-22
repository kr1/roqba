'''creates the messages for puredata array's sinesum command:

sinesum expects a list of numbers representing the amplitudes of
consecutive partial sinewaves
'''
import random
import math


def random_wavetable(partials=15, which='all'):
    '''all partials have randomly selected amplitudes'''
    det = lambda x: random.random()
    fun = __assemble(which, det)
    parts = map(fun, xrange(partials))
    return " ".join(parts)


def random_harmonic_wavetable(partials=15, which='all'):
    '''all partials have randomly selected amplitudes

    the maximum value of each amplitude is its value in the
    harmonic series (as returned by <harmonic_wavetable>).
    '''
    det = lambda x: random.random() / (x + 1)
    fun = __assemble(which, det)
    parts = map(fun, xrange(partials))
    return " ".join(parts)


def harmonic_wavetable(partials=15, which='all'):
    '''the value of each amplitude of partial N is given by 1 / N'''
    det = lambda x: 1.0 / (x + 1)
    fun = __assemble(which, det)
    parts = map(fun, xrange(partials))
    parts[0] = "1"
    return " ".join(parts)


def __assemble(which, determinant):
    '''helper function to assemble abstract odd/even capable lambdas'''
    if which == 'all':
        fun = lambda x: str(determinant(x))
    if which == 'odd':
        fun = lambda x: (x % 2 == 1) and str(determinant(x)) or "0"
    if which == 'even':
        fun = lambda x: (x % 2 == 0) and str(determinant(x)) or "0"
    return fun


def _apply_wavetable(string, size=4096):
    '''creates and returns a normalized list of length <size>

    applying the weights in the incoming definition'''
    numbers = _as_floats(string)
    wavetable = []
    pi_step = 2 * math.pi / size
    for index in xrange(size):
        wavetable.append(sum([value * math.sin(pi_step * index * (harmo_index + 1))
                              for harmo_index, value in enumerate(numbers)]))
    max_ = max(abs(min(wavetable)), max(wavetable))
    return [num/max_ for num in wavetable]


def _as_floats(string):
    '''utility function to get the wavetable def as a list of floats'''
    return [float(num) for num in string.split(" ")]
