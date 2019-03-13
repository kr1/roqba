import itertools

SCALES = {
    "DIATONIC": [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    "HARMONIC": [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    "MELODIC": [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    "PENTATONIC": [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    "PENTA_MINOR": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    "GREEK_CHROMATIC": [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0],
    "GREEK_ENHARMONIC": [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0],
    "PTOLEMY_TROPOI": [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],  # (West - ancient greek music)
    # the next 2 scales start in minor, the final scale uses tunings
    "PERSIAN_SEGAH": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    "PERSIAN_SHUR": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
}

NOTES_PER_SCALE = {
    "DIATONIC": 7,
    "HARMONIC": 7,
    "MELODIC": 7,
    "PENTATONIC": 5,
    "PENTA_MINOR": 5,
    "GREEK_CHROMATIC": 7,
    "GREEK_ENHARMONIC": 7,
}

SCALES_BY_FREQUENCY = sum([
    ["DIATONIC"] * 6,
    ["HARMONIC"] * 4,
    ["MELODIC"] * 4,
    ["GREEK_ENHARMONIC"] * 3,
    ["GREEK_CHROMATIC"] * 3,
    ['PERSIAN_SEGAH'] * 2,
    ['PERSIAN_SHUR'] * 2,
    ["PENTATONIC"] * 1,
    ["PENTA_MINOR"] * 1],
    [])

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]),
                    set([3, 5, 0]), set([2, 5, 0])]

FOUR_NOTE_HARMONIES = [
    set([2, 4, 5]),
    set([2, 4, 8]),
    set([3, 5, 11]),
    set([2, 4, 6]),
    set([4, 5, 6]),
    set([4, 6, 12]),
    set([1, 2, 3]),
]

tmp_length_2_strict = [set(res) for res in
                          [n[:2] for n in
                              sum(
                                  [list(itertools.permutations(set_)) for set_ in STRICT_HARMONIES],
                                  []
                              )
                          ]
                      ]

ALL_STRICT_HARMONIES = STRICT_HARMONIES + tmp_length_2_strict

# TODO: create dynamically
BASE_HARMONIES = {2: [set([6]), set([6, 2]), set([6, 0]), set([0, 2]),
                      set([0, 4])],
                  3: [set([0]), set([6]), set([6, 2]), set([6, 0]),
                      set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])],
                  4: [set([0, 2]), set([6]), set([6, 2]), set([6, 0]),
                      set([0, 2, 5]), set([0, 2, 4, 6]),
                      set([0, 5]),  # experimental: for pentatonic-'trap'
                      set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])]
                  }

HARMONIES = STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]
HARMONIC_INTERVALS = [0, 2, 3, 4, 5, 6]

FOLLOWINGS = [-9, -5, -2, 2, 5, 9, 12]

DISHARMS = [1]

if __name__ == "__main__":
    print(SCALES_BY_FREQUENCY)
    print(tmp_length_2_strict)
    print("ALL_STRICT_HARMONIES", ALL_STRICT_HARMONIES)
