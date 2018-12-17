import random
from collections import namedtuple, defaultdict

# these movements are relative to the preceding note of the melody
# i. e. staps to be taken (2 up, 1 down, ...)
delta_movements = (
    (-1,),
    (1,),
    (0, 0, 1, 1, -2, -1, 1, 0),
    (0, 1, 0, 0, -2, -1, 1, 0)
)

DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL = defaultdict(list)

Deltatype = namedtuple('Delta', 'high low diff')

for mov in delta_movements:
    start = 0 - mov[0]
    high = max([sum(mov[:index]) for index, _ in enumerate(mov)])
    low = min([sum(mov[:index]) for index, _ in enumerate(mov)])
    diff = sum(mov)
    DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL[Deltatype(high, low, diff)].append(mov)

# this movemente are relative to the target note
Clausula = namedtuple('Clausula', 'note length')

clausulae = (
    ((0, 1), (-1, 1), (-1, 3), (0, 3)),
    ((-1, 1), (1, 1), (-1, 1), (0, 3), (0, 3)),
    ((3, 1), (2, 1), (3, 1), (1, 3), (0, 3)),
)

CLAUSULAE_BY_START_NOTE = defaultdict(list)
for clausula in clausulae:
    CLAUSULAE_BY_START_NOTE[clausula[0][0]].append(clausula)


def end_word(start_note):
    word = random.choice(CLAUSULAE_BY_START_NOTE[start_note])
    return word


def next_valid_word(start_note, high_limit, low_limit):
    valid_words = [movement for indicators, movement
                   in DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL.items()
                   if indicators.high <= high_limit
                   and indicators.low >= low_limit]
    return random.choice(valid_words)


if __name__ == '__main__':
    print DELTA_MOVEMENTS_BY_AMPLITUDE_AND_VERTICAL
