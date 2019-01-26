"""this module privides constant note-length (rhythm) groupings
pauses should be implemented as a gate on the trigger and
are not implemented in the groupings

reconsider specifying pauses with negative values(to-do:
check implications on other modules)
"""
import logging
from random import choice

logger = logging.getLogger('setup')

DEFAULT_METER_LENGTH = (8, (4, 4))

groupings = {
    (8, (4, 4)): {
        "first": [
            # smallest units
            # 8: 8x1
            [[1, 1, 1, 1, 1, 1, 1, 1]] * 3,
            # 7: 6x1 & 1x2
            [[2, 1, 1, 1, 1, 1, 1]] * 6,
            [[1, 2, 1, 1, 1, 1, 1]] * 4,
            [[1, 1, 2, 1, 1, 1, 1]] * 6,
            [[1, 1, 1, 2, 1, 1, 1]] * 4,
            [[1, 1, 1, 1, 2, 1, 1]] * 6,
            [[1, 1, 1, 1, 1, 2, 1]] * 4,
            [[1, 1, 1, 1, 1, 1, 2]] * 6,
            # 6: 5x1 & 1x3
            [[3, 1, 1, 1, 1, 1]] * 2,
            [[1, 3, 1, 1, 1, 1]] * 2,
            [[1, 1, 3, 1, 1, 1]] * 2,
            [[1, 1, 1, 3, 1, 1]] * 2,
            [[1, 1, 1, 1, 3, 1]] * 2,
            [[1, 1, 1, 1, 1, 3]] * 2,
            # 5: 1x4 & 1x4
            [[4, 1, 1, 1, 1]] * 2,
            [[1, 4, 1, 1, 1]] * 2,
            [[1, 1, 4, 1, 1]] * 2,
            [[1, 1, 1, 4, 1]] * 2,
            [[1, 1, 1, 1, 4]] * 2,
            # 4: 1x5 3x1
            [[5, 1, 1, 1]] * 2,
            [[1, 5, 1, 1]] * 2,
            [[1, 1, 5, 1]] * 2,
            [[1, 1, 1, 5]] * 2,
            # 3: 1x6 & 2x1
            [[6, 1, 1]] * 2,
            [[1, 6, 1]] * 2,
            [[1, 1, 6]] * 2,
            # 2: 1x7 & 1x1
            [[7, 1]] * 2,
            [[1, 7]] * 2,
            # 1: 1x8
            [[8]] * 1],
        "second": [
            # second smallest units:
            # 5 3x2 & 2x1
            [[1, 1, 2, 2, 2]] * 8,
            [[2, 1, 1, 2, 2]] * 8,
            [[2, 2, 1, 1, 2]] * 8,
            [[2, 2, 2, 1, 1]] * 8,
            # 4: 4x2
            [[2, 2, 2, 2]] * 10,
            # 3: 1x4 & 2x2
            [[4, 2, 2]] * 8,
            [[2, 4, 2]] * 8,
            [[2, 2, 4]] * 8,
            # 2 1x6 & 1x2
            [[6, 2]] * 6,
            [[2, 6]] * 6],
        "terns": [
            # second smallest units:
            #  2x3 & 2x1
            [[3, 3, 1, 1]] * 8,
            [[3, 1, 1, 3]] * 3,
            [[1, 1, 3, 3]] * 8,
            #  2x3 & 2x1
            [[2, 3, 3]] * 8,
            [[3, 2, 3]] * 3,
            [[3, 3, 2]] * 8,
            # 2 x (2, 1) & 2x1
            [[2, 2, 1, 2, 1]] * 8,
            [[2, 1, 2, 2, 1]] * 5,
            [[2, 1, 2, 1, 2]] * 8],
        "heavy": [
            # 5 3x2 & 2x1
            [[2, 1, 1, 2, 2]] * 3,
            [[2, 2, 1, 1, 2]] * 3,
            [[2, 2, 2, 1, 1]] * 3,

            # 6 2x2 & 4x1
            [[2, 1, 1, 2, 1, 1]] * 3,
            [[1, 1, 2, 1, 1, 2]] * 3,
            # 4: 4x2
            [[2, 2, 2, 2]] * 5,
            # 3: 1x4 & 2x2
            [[4, 2, 2]] * 8,
            [[2, 4, 2]] * 8,
            [[2, 2, 4]] * 8,
            # 5 1x4 & 1x2 & 2x1
            [[4, 2, 1, 1]] * 3,
            [[2, 1, 1, 4]] * 3,
            [[1, 1, 4, 2]] * 3,
            [[4, 1, 1, 2]] * 3,
            [[1, 1, 2, 4]] * 3,
            [[4, 1, 1, 2]] * 3,
            # 2 1x6 & 1x2
            [[6, 2]] * 6,
            [[2, 6]] * 6]},
    (8, (2, 2, 2, 2)): {
        "heavy": [
            [[2, 2, 2, 2]] * 17,
            [[4, 2, 2]] * 7,
            [[2, 4, 2]] * 7,
            [[2, 2, 4]] * 7,
        ],
        "first": [
            [[1, 1, 1, 1, 1, 1, 1, 1]] * 3,
            [[2, 1, 1, 1, 1, 1, 1]] * 10,
            [[2, 1, 1, 2, 1, 1]] * 10],
        "second": [
            [[2, 2, 1, 1, 1, 1]] * 10,
            [[2, 1, 1, 2, 2]] * 10],
        "terns": [
            [[2, 1, 2, 1, 1, 1]] * 10,
            [[2, 1, 1, 1, 2, 1]] * 10,
            [[1, 1, 1, 2, 1, 2]] * 10]
    },
    (8, (3, 3, 2)): {
        "heavy": [
            [[3, 3, 2]] * 20,
            [[3, 3, 1, 1]] * 5,
            [[2, 1, 2, 1, 2]] * 5,
            [[2, 1, 2, 1, 1, 1]] * 5,
            [[1, 1, 1, 2, 1, 1, 1]] * 5
        ]
    },
    (5, (2, 3)): {
        "heavy": [
            [[5]] * 7,
            [[2, 3]] * 20,
            [[2, 2, 1]] * 5,

            [[1, 1, 3]] * 5,
            [[1, 1, 2, 1]] * 5,
            [[1, 1, 1, 1, 1]] * 5,
            [[2, 1, 1, 1]] * 5
        ]
    },
    (5, (3, 2)): {
        "heavy": [
            [[5]] * 7,
            [[3, 2]] * 20,
            [[2, 1, 2]] * 5,

            [[1, 1, 1, 2]] * 5,
            [[1, 1, 1, 1, 1]] * 5,
            [[2, 1, 1, 1]] * 5]
    },
    (6, (3, 3)): {
        "heavy": [
            [[6]] * 3,
            [[3, 3]] * 15,
            [[3, 2, 1]] * 3,
            [[2, 1, 2, 1]] * 6,
            [[3, 1, 1, 1]] * 3,
            [[1, 1, 1, 3]] * 3,
            [[2, 2, 2]] * 4]
    },
    (6, (2, 2, 2)): {
        "heavy": [
            [[6]] * 3,
            [[2, 2, 2]] * 15,
            [[3, 1, 2]] * 6,
            [[1, 1, 2, 2]] * 3,
            [[2, 1, 1, 2]] * 3,
            [[2, 2, 1, 1]] * 3,
            [[2, 2, 1, 1]] * 3,
            [[1, 1, 1, 1, 2]] * 4,
            [[2, 1, 1, 1, 1]] * 4,
            [[1, 1, 2, 1, 1]] * 4]
    },
    (7, (3, 2, 2)): {
        "heavy": [
            [[5, 2]] * 7,
            [[3, 2, 2]] * 20,
            [[2, 1, 2, 2]] * 7,

            [[1, 1, 1, 2, 2]] * 5,
            [[1, 1, 1, 1, 1, 1, 1]] * 5,
            [[2, 1, 1, 1, 1, 1]] * 7,
            [[1, 1, 1, 1, 1, 2]] * 5,
            [[2, 1, 2, 1, 1]] * 7]
    },
    (9, (3, 3, 3)): {
        "heavy": [
            [[6, 3]] * 7,
            [[3, 6]] * 7,
            [[3, 3, 3]] * 30,
            [[2, 1, 2, 1, 2, 1]] * 7,
            [[1, 1, 1, 1, 1, 1, 1, 1, 1]] * 5,
            [[2, 1, 1, 1, 1, 1, 1, 1]] * 5,
            [[2, 1, 2, 1, 1, 1, 1]] * 7,
            [[3, 3, 1, 1, 1]] * 5,
            [[3, 2, 1, 1, 2]] * 7]
    },
    (11, (3, 3, 3, 2)): {
        "heavy": [
            [[6, 3, 2]] * 7,
            [[3, 6, 2]] * 7,
            [[3, 3, 3, 2]] * 30,
            [[2, 1, 2, 1, 2, 1, 2]] * 7,

            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] * 5,
            [[2, 1, 1, 1, 1, 1, 1, 1, 2]] * 5,
            [[2, 1, 2, 1, 1, 1, 1, 2]] * 7,
            [[3, 3, 1, 1, 1, 1, 1]] * 5,
            [[3, 2, 1, 1, 2, 2]] * 7]
    },
    (12, (3, 3, 2, 2, 2)): {
        "heavy": [
            [[3, 3, 2, 2, 2]] * 17,
            [[3, 3, 6]] * 7,
            [[3, 3, 4, 2]] * 10,
            [[2, 1, 2, 1, 2, 2, 2]] * 7,
            [[1, 1, 1, 2, 1, 2, 1, 1, 2]] * 7,
            [[1, 2, 2, 1, 2, 2, 2]] * 7,
            [[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] * 5],
        "first": [
            [[2, 1, 2, 1, 2, 2, 1, 1]] * 10,
            [[1, 1, 1, 2, 1, 1, 1, 2, 1, 1]] * 10,
            [[2, 1, 2, 1, 1, 1, 2, 1, 1]] * 10],
        "second": [
            [[2, 1, 2, 1, 2, 2, 2]] * 10,
            [[3, 3, 2, 2, 2]] * 10],
        "terns": [
            [[1, 1, 2, 1, 1, 2, 1, 2, 1]] * 10,
            [[1, 2, 1, 2, 1, 2, 1, 2]] * 10,
            [[2, 1, 2, 1, 2, 1, 2, 1]] * 10]
    },
    (12, (2, 2, 2, 3, 3)): {
        "heavy": [
            [[2, 2, 2, 3, 3]] * 7,
            [[6, 3, 3]] * 7,
            [[4, 2, 3, 3]] * 30,
            [[2, 2, 2, 2, 1, 2, 1]] * 7,
            [[2, 2, 2, 1, 2, 2, 1]] * 7,
            [[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] * 5],
        "first": [
            [[1, 1, 2, 1, 1, 2, 1, 2, 1]] * 15,
            [[2, 1, 1, 1, 1, 2, 1, 2, 1]] * 5,
            [[1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1]] * 10],
        "terns": [
            [[1, 1, 2, 1, 1, 2, 1, 2, 1]] * 10,
            [[1, 2, 1, 2, 1, 2, 1, 2]] * 10,
            [[2, 1, 2, 1, 2, 1, 2, 1]] * 10]
    },
    (12, (1, 2, 2, 1, 2, 2, 2)): {
        "heavy": [
            [[1, 2, 2, 1, 2, 2, 2]] * 20,
            [[3, 3, 2, 2, 2]] * 7],
        "first": [
            [[1, 1, 1, 2, 1, 2, 1, 2, 1]] * 10,
            [[1, 1, 1, 1, 1, 1, 2, 2, 2]] * 10,
            [[1, 2, 2, 1, 1, 1, 1, 1, 2]] * 10],
        "terns": [
            [[2, 1, 2, 1, 2, 1, 2, 1]] * 10,
            [[1, 2, 1, 2, 1, 2, 1, 2]] * 10,
            [[3, 3, 1, 1, 1, 3]] * 10]
    },
    (15, (3, 3, 2, 3, 2, 2)): {
        "heavy": [
            [[3, 3, 2, 3, 2, 2]] * 20,
            [[3, 3, 1, 1, 3, 1, 1, 2]] * 5,
            [[2, 1, 2, 1, 2, 2, 1, 2, 2]] * 25,
        ],
        "first": [
            [[2, 1, 2, 1, 2, 2, 1, 2, 1, 1]] * 25,
         ],
        "second": [
            [[2, 1, 1, 1, 1, 2, 2, 1, 2, 2]] * 25,
         ],
        "terns": [
            [[3, 3, 2, 3, 2, 2]] * 20,
        ]
    },
    (18, (3, 3, 2, 2, 2, 3, 3)): {
        "heavy": [
            [[3, 3, 2, 2, 2, 3, 3]] * 20,
        ],
        "first": [
            [[2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2]] * 20,
         ],
        "second": [
            [[1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1]] * 20,
         ],
        "terns": [
            [[1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1]] * 20,
        ]
    },
    (23, (3, 3, 2, 3, 3, 2, 3, 2, 2)): {
        "heavy": [
            [[3, 3, 2, 3, 3, 2, 3, 2, 2]] * 20,
        ],
        "first": [
            [[3, 2, 1, 1, 1, 3, 2, 1, 2, 3, 2, 1, 1]] * 20,
         ],
        "second": [
            [[3, 2, 1, 1, 1, 3, 2, 1, 2, 3, 2, 1, 1]] * 20,
         ],
        "terns": [
            [[2, 1, 3, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2]] * 20,
        ]
    },
    (24, (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)): {
        "heavy": [
            [[2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]] * 20,
            [[3, 3, 3, 3, 3, 3, 3, 3]] * 7],
        "first": [
            [[1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1]] * 10,
            [[1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2]] * 10,
            [[1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2]] * 10],
        "terns": [
            [[2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]] * 10,
            [[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]] * 10,
            [[3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 1, 3]] * 10]
    },
    (24, (2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)): {
        "heavy": [
            [[2, 1, 3, 2, 1, 3, 2, 1, 2, 1, 2, 1, 2, 1]] * 20,
            [[3, 3, 3, 3, 3, 3, 3, 3]] * 7],
        "first": [
            [[3, 3, 3, 3, 3, 3, 3, 3]] * 7,
            [[2, 1, 2, 6, 1, 2, 1, 2, 1, 2, 1, 2, 1]] * 20],
        "second": [
            [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] * 7],
        "terns": [
            [[1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1]] * 10],
    },
    (30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2)): {
        "heavy": [
            [[2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2]] * 20,
            [[3, 4, 3, 4, 3, 4, 3, 4, 2]] * 7,
            [[3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2]] * 7],
        "first": [
            [[1, 1, 1, 2, 2, 3, 2, 1, 1, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1]] * 7],
        "second": [
            [[3, 4, 7, 1, 1, 1, 2, 1, 1, 3, 2, 1, 1, 2]] * 3],
        "terns": [
            [[3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 3]] * 10],
    }
}


def get_grouping(meter, mode, check=True):
    '''returns the groupings for a given meter and mode

    well_formedness is checked by default, "default"-mode
    will combine first, second and terns-modes
    '''
    mode = None if mode == "default" else mode
    meter_length = meter if type(meter) == int else meter[0]
    res = _assemble(meter, mode)
    if check:
        if badly_formeD(meter_length, res):
            raise RuntimeError(
                "badly formed rhythm grouping. length: {}\nmode: {}\npattern: {}".format(
                    meter_length, mode, res))
    return res


def _assemble(id_, which=None, fallback=True):
    '''assembles note-length groupings.

    it is called during the loading of the module'''
    target = groupings.get(id_)
    if not target:
        logger.error("no dedicated note length groupings for {}".format(id_))
        target_length = id_[0]
        fitting = [groupings[key] for key in groupings.keys() if key[0] == target_length]
        try:
            target = choice(fitting)
        except Exception as error:
            message = ("Exception when falling back to length-based groupings "
                       "for: {}\n{}\n{}").format(id_, error.__class__, error)
            logger.error(message)
            raise RuntimeError(message)
    if which:
        if which in target:
            return sum(target[which], [])
        else:
            if fallback:
                return sum(target['heavy'], [])
            else:
                raise RuntimeError("non-existing meter mode")
    else:
        return (_assemble(id_, "first", fallback) +
                _assemble(id_, "second", fallback) +
                _assemble(id_, "terns", fallback))


DEFAULT_NOTE_LENGTH_GROUPINGS = _assemble(DEFAULT_METER_LENGTH)
DEFAULT_FAST_GROUPINGS = _assemble(DEFAULT_METER_LENGTH, "first")
DEFAULT_TERNARY_GROUPINGS = _assemble(DEFAULT_METER_LENGTH, "terns")
DEFAULT_SLOWER_GROUPINGS = _assemble(DEFAULT_METER_LENGTH, "heavy")


def analyze_grouping(g):
    """transform the grouping into a binary pattern for every beat, i.e.:

    >>> analyze_grouping([1,2,1,3])
    [1, 1, 0, 1, 1, 0, 0]
    """
    res = []
    for item in g:
        first = True
        for n in xrange(item):
            if first:
                res.append(1)
            else:
                res.append(0)
            first = False
    return res


def badly_formeD(meter_length, to_check):
    '''checks if a grouping is well-formed

    checks if the sum of items equals the specified target length'''
    odd = filter(lambda x: sum(x) != meter_length, to_check)
    return bool(odd)

if badly_formeD(DEFAULT_METER_LENGTH[0], DEFAULT_NOTE_LENGTH_GROUPINGS):
    raise RuntimeError('''not all note length groupings are well-formed:
            \n{0}\n\nin:{1}'''.format(badly_formeD(DEFAULT_METER_LENGTH,
                                      DEFAULT_NOTE_LENGTH_GROUPINGS),
                                      DEFAULT_NOTE_LENGTH_GROUPINGS))
