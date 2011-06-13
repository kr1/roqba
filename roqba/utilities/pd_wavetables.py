'''creates the messages for puredata's array's sinesum command:

sinesum expects a list of numbers representing the amplitudes of
consecutive partial sinewaves
'''
import random


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
