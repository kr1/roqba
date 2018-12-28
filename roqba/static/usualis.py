import logging
import random
import itertools
from collections import namedtuple, defaultdict

# these movements are relative to the preceding note of the melody
# i. e. staps to be taken (2 up, 1 down, ...)
delta_movements = (
    (-1,),
    (1,),
    (-1, -1),
    (1, 1),
    (-1, -1, 1),
    (-1, -1, 2),
    (1, 1, -1),
    (1, 1, -2),
    (1, 1, 1, -1, 1, -3, 1),
    (1, 1, -2, -1, 1, 0),
    (0, 1, 0, 0, -2, -1, 1, 0)
)
musical_logger = logging.getLogger('musical')

DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL = defaultdict(list)

Deltatype = namedtuple('Delta', 'high low diff')

for mov in delta_movements:
    start = 0 - mov[0]
    high = max([sum(mov[:index]) for index, _ in enumerate(mov)])
    low = min([sum(mov[:index]) for index, _ in enumerate(mov)])
    diff = sum(mov)
    DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL[Deltatype(high, low, diff)].append(mov)

# these movements are relative to the target note
Note = namedtuple('Note', 'note length')
Ambitus = namedtuple('Ambitus', 'lower upper')


clausulae = (
    ((-4, 1), (-3, 1), (-2, 1), (-3, 3), (0, 3)),
    ((-3, 1), (-1, 1), (0, 1), (1, 3), (0, 3)),
    ((-2, 1), (1, 1), (03, 1), (1, 3), (0, 3)),
    ((-1, 1), (1, 1), (-1, 1), (0, 3), (0, 3)),
    ((0, 1), (-1, 1), (-1, 3), (0, 3)),
    ((1, 1), (-1, 1), (-1, 1), (0, 3), (0, 3)),
    ((2, 1), (2, 1), (3, 1), (1, 3), (0, 3)),
    ((3, 1), (2, 1), (3, 1), (1, 3), (0, 3)),
    ((4, 1), (3, 1), (2, 1), (3, 3), (0, 3)),
)


CLAUSULAE_BY_START_NOTE = defaultdict(list)
for clausula in clausulae:
    CLAUSULAE_BY_START_NOTE[clausula[0][0]].append(clausula)


def end_word(start_note):
    word = random.choice(CLAUSULAE_BY_START_NOTE[start_note])
    word = [Note(note, length) for note, length in word]
    musical_logger.debug("\nend word {0}\n".format(word))
    return word


def next_valid_word(start_note, high_limit, low_limit):
    should_go_upward = low_limit >= -1
    should_go_downward = high_limit <= 1
    free = not(should_go_downward or should_go_downward)
    valid_words = [movement for indicators, movement
                   in DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL.items()
                   if indicators.high <= high_limit
                   and indicators.low >= low_limit
                   and ((indicators.diff > 0 and should_go_upward)
                       or (indicators.diff < 0 and should_go_downward)
                       or free) ]
    valid_words = list(itertools.chain(*valid_words))
    word = random.choice(valid_words)
    word = [Note(note, length()) for note in word]
    musical_logger.debug("word {0}".format(word))
    return word


def length():
    value = random.random()
    if value < 0.05:
        return 3
    elif value < 0.08:
        return 2
    return 1


if __name__ == '__main__':
    print DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL
