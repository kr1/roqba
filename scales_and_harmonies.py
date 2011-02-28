
DIATONIC = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
HARMONIC = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
MELODIC = [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]
PENTATONIC = [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0 ]
PENTA_MINOR = [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]),
                    set([3, 5, 0]), set([2, 5, 0])]

# TODO: create dynamically
BASE_HARMONIES = {2:[set([6]), set([6, 2]), set([6, 0]), set([0, 2]), set([0, 4])],
                  3:[set([0]), set([6]), set([6, 2]), set([6, 0]), set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])],
                  4:[set([0, 2]), set([6]), set([6, 2]), set([6, 0]), set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])]
                  }
HARMONIES = STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]
HARMONIC_INTERVALS = [0, 2, 3, 4, 5, 6]

DISHARMS = [1]