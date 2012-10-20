import itertools

SCALES = {
    "DIATONIC": [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    "HARMONIC": [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    "MELODIC": [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    "PENTATONIC": [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    "PENTA_MINOR": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]
  }

SCALES_BY_FREQUENCY = sum([
    ["DIATONIC"] * 4,
    ["HARMONIC"] * 2,
    ["MELODIC"] * 2,
    ["PENTATONIC"] * 2,
    ["PENTA_MINOR"] * 1],
  [])

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]),
                    set([3, 5, 0]), set([2, 5, 0])]

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
                      set([0, 5]), # experimental: for pentatonic-'trap'
                      set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])]
                  }

HARMONIES = STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]
HARMONIC_INTERVALS = [0, 2, 3, 4, 5, 6]

FOLLOWINGS = [-5, -3, -2, 2, 4,  5]

DISHARMS = [1]

if __name__ == "__main__":
    print SCALES_BY_FREQUENCY
    print tmp_length_2_strict
    print  "ALL_STRICT_HARMONIES", ALL_STRICT_HARMONIES
