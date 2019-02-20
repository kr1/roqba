import logging
import random
import itertools
from collections import namedtuple, defaultdict

musical_logger = logging.getLogger('musical')


class UsualisError(Exception):
    pass


# these movements are relative to the preceding note of the melody
# i. e. steps to be taken (2,-1, 0 means 2 up, 1 down, same note again)
delta_movements = (
    (-1, 0, 0),
    (1, 0),
    (0, 1),
    (0, -1),
    (-1, -1),
    (0, -1, -1, 0),
    (0, 1, 1, 0),
    (1, 1, -1, 1),
    (-1, -1, 1, 1, 1),
    (-1, -1, 1, 2, -1),
    (-1, -1, 2),
    (1, 1, -1),
    (1, 1, -1, -1),
    (1, 1, -2),
    (1, 1, 1, -1, 1, -3, 1),
    (1, -4, 1, 1, 1, 1, -2, 1, 1),
    (-1, 4, -1, -1, -1, -1, 2, -1, -1),
    (1, 1, -2, -1, 1, -1),
    (1, 1, -1, -1, -2, -1, 1, -1),
    # from the source (p. 781 Pascha, ed 1961)
    (0, 0, 2, -1, 1),
    (-2, -1, -1, 1, 1, -2),
    (2, -1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1),
    (0, 0, -1, 1, 2, 2),
    (0, 0, 0, 2, -1, -1, 0),
    (-2, 2, 0, 0, -2, -1, 1, 2, 0, 2, -1, 1, -2, 0),
    (0, 0, -1, 1, 0, -2, 1, -2, 0),
    (3, 1, 1, -1, 1, 0, -1, 1, -1, -1, 1),
    (-1, -2, 2, -1, 1, 1, -1),
    (-1, 2, 1, -1, 1, -2, 1, -1, 0),
    (0, 0, -2, 2, -1, 1, -2, 0, 1, 1, -3),
    (1, -1, 3, 1, 1, 1, -1, 1, -1, -1, 1, 1, 0),
    (-3, 1, 0, 2, -1, -1, 1, -1, 0, -1, 1, 0, -1),
)

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
    ((-5, 1), (-4, 1), (-3, 1), (-2, 1), (-3, 2), (-2, 1), (-1, 3), (0, 3)),
    ((-4, 1), (-3, 1), (-2, 1), (-3, 3), (0, 3)),
    ((-3, 1), (-1, 1), (0, 1), (1, 3), (0, 3)),
    ((-2, 1), (1, 1), (3, 1), (1, 3), (0, 3)),
    ((-1, 1), (1, 1), (-1, 1), (0, 3), (0, 3)),
    ((0, 1), (-1, 1), (-2, 2), (-1, 2), (0, 3)),
    ((0, 1), (0, 1), (2, 1), (1, 1), (2, 1), (1, 1), (1, 1), (0, 3)),
    ((0, 1), (3, 1), (2, 1), (1, 1), (2, 1), (3, 1), (2, 1), (0, 3)),
    ((0, 1), (0, 1), (-1, 1), (-2, 1), (-1, 1), (0, 1), (-1, 3), (0, 3)),
    ((1, 1), (2, 1), (4, 1), (3, 1), (1, 1), (2, 1), (0, 1), (0, 3)),
    ((1, 1), (-1, 1), (-1, 1), (0, 3), (0, 3)),
    ((2, 1), (2, 1), (3, 1), (1, 3), (0, 3)),
    ((2, 1), (1, 2), (0, 1), (1, 1), (0, 3)),
    ((2, 1), (4, 1), (3, 1), (2, 2), (3, 2), (0, 3)),
    ((2, 1), (3, 1), (4, 1), (3, 1), (2, 1), (1, 1), (2, 1), (1, 2), (0, 1), (0, 3)),
    ((3, 1), (2, 1), (3, 1), (1, 3), (0, 3)),
    ((4, 1), (3, 1), (2, 1), (3, 3), (0, 3)),
    ((4, 1), (3, 1), (1, 1), (0, 1), (2, 1), (1, 1), (0, 1), (0, 3)),
    ((5, 1), (4, 1), (3, 2), (2, 1), (3, 1), (2, 1), (1, 3), (0, 3)),
)


CLAUSULAE_BY_START_NOTE = defaultdict(list)
for clausula in clausulae:
    CLAUSULAE_BY_START_NOTE[clausula[0][0]].append(clausula)


def end_word(start_note):
    word = random.choice(CLAUSULAE_BY_START_NOTE[start_note])
    word = [Note(note, length) for note, length in word]
    musical_logger.debug("\nend word {0}\n".format(word))
    return word


def safe_next_valid_word(start_note, high_limit, low_limit, double_prop=0.06, triple_prob=0.03):
    """calls next_valid_word with the same arguments.

    if a UsualisError is raised it returns a way back into
    the ambitus"""
    try:
        word = next_valid_word(start_note, high_limit, low_limit, double_prop, triple_prob)
        return word
    except UsualisError:
        direction = 1 if start_note < 0 else -1
        word = [Note(direction, length(double_prop, triple_prob))
                for _ in range(0, 2 + int(random.random() * abs(start_note)))]
        musical_logger.error('Usualis: no real word, using dynamically created: {}'.format(word))
        return word


def next_valid_word(start_note, high_limit, low_limit, double_prop=0.06, triple_prob=0.03):
    """selects a new words from the available pool

    according to the given start_note and limits.
    Raises a UsualisError if no suitable candidates are found"""
    should_go_upward = abs(start_note - low_limit) < abs(start_note - high_limit)
    should_go_downward = not(should_go_upward)
    valid_words = []
    for indicators, movement in DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL.items():
        end_note = start_note + indicators.diff
        if ((indicators.high <= high_limit and indicators.low >= low_limit)  # statically in range
            and (end_note <= high_limit and end_note >= low_limit)  # end-note in range
            and (start_note <= high_limit and start_note >= low_limit)  # start-note in range
            and (indicators.diff > 0 and should_go_upward
                 or (indicators.diff < 0 and should_go_downward))):
            valid_words.append(movement)
    valid_words = list(itertools.chain(*valid_words))
    try:
        word = random.choice(valid_words)
    except IndexError:
        message = "No next valid word for {}, headroom: {}, legroom: {}".format(
            start_note, high_limit, low_limit)
        musical_logger.error(message)
        raise UsualisError(message)
    word = [Note(note, length(double_prop, triple_prob)) for note in word]
    musical_logger.debug("word {0}".format(word))
    return word


def length(double_prop, triple_prob):
    value = random.random()
    if value < triple_prob:
        return 3
    elif value < double_prop:
        return 2
    return 1


if __name__ == '__main__':
    print(DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL)
