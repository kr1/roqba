"""this module contains probability values for melody sequences."""

default_probs = [[1] * 30,
                 [2] * 10,
                 [3] * 4,
                 [4] * 2,
                 [5] * 2,
                 [6] * 2,
                 [7] * 4,
                 [8, 9, 10, 11, 12] * 1
                ]

mid_probs = [[1] * 20,
             [2] * 7,
             [3] * 5,
             [4, 5, 6, 7] * 1
            ]

bass_probs = [[1] * 6,
              [2] * 10,
              [3] * 5,
              [4] * 10,
              [5] * 5,
              [6] * 2,
              [7] * 1
             ]

DEFAULT_MOVEMENT_PROBS = sum(default_probs, [])
MIDDLE_VOICES_MOVEMENT_PROBS = sum(mid_probs, [])
BASS_MOVEMENT_PROBS = sum(bass_probs, [])

ORNAMENTS = {(0, 1): [[(0.5, 0), (0.5, 1)],
                      [(0.5, 0), (0.5, -1)],
                      [(0.25, 0), (0.25, -1), (0.25, 0), (0.25, -1)],
                      [(0.25, 0), (0.25, 1), (0.25, 0), (0.25, 1)],
                      [(0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1)]],
             (0, 2): [[(0.25, 2), (0.25, 1), (0.25, 2), (0.25, 1)],
                      [(0.25, 2), (0.25, 3), (0.25, 2), (0.25, 1)],
                      [(0.25, 0), (0.25, 1), (0.25, 2), (0.25, 1)],
                      [(0.25, 0), (0.25, 1), (0.25, 0), (0.25, -1)],
                      [(0.3333333333, 0), (0.3333333333, 1), (0.3333333333, 0),
                       (0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1)],
                      [(0.3333333333, 0), (0.3333333333, -1), (0.3333333333, 0),
                       (0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1)],
                      [(0.3333333333, 0), (0.3333333333, 1), (0.3333333333, 0),
                       (0.3333333333, -1), (0.3333333333, 0), (0.3333333333, -1)]
                      ],
             (1, 1): [[(0.5, 1), (0.5, 0)],
                      [(0.5, 1), (0.5, 2)],
                      [(0.3333333333, 0), (0.3333333333, 1), (0.3333333333, 0)]],
             (1, 2): [[(0.25, 0), (0.25, 1), (0.25, 0), (0.25, 1)],
                      [(0.25, 1), (0.25, 2), (0.25, 1), (0.25, 0)],
                      [(0.25, 1), (0.25, 0), (0.25, 1), (0.25, 2)],
                      [(0.3333333333, 1), (0.3333333333, 2), (0.3333333333, 1),
                       (0.3333333333, 0), (0.3333333333, 1), (0.3333333333, 0)],
                      [(0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1),
                       (0.3333333333, 2), (0.3333333333, 1), (0.3333333333, 2)]],
             (1, 3): [[(1/3.0, 0), (1/3.0, 1), (1/3.0, 0),
                       (1/3.0, 1), (1/3.0, 0), (1/3.0, 1),
                       (1/3.0, 0), (1/3.0, 1), (1/3.0, 0)]],
             (1, 4): [[(1/3.0, 1), (1/3.0, 0), (1/3.0, 1),
                       (1/3.0, 0), (1/3.0, 1), (1/3.0, 0),
                       (1/3.0, 1), (1/3.0, 0), (1/3.0, 1),
                       (1/3.0, 0), (1/3.0, 1), (1/3.0, 0)]],
             (2, 1): [[(0.5, 2), (0.5, 1)],
                      [(0.5, 0), (0.5, 1)],
                      [(0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1)],
                      [(0.3333333333, 1), (0.3333333333, 2), (0.3333333333, 1)]],
             (3, 1): [[(0.5, 1), (0.5, 2)],
                      [(0.3333333333, 1), (0.3333333333, 0), (0.3333333333, 1)],
                      [(0.3333333333, 1), (0.3333333333, 2), (0.3333333333, 1)]],
             (4, 1): [[(0.5, 2), (0.5, 3)],
                      [(0.5, 4), (0.5, 3)],
                      [(0.3333333333, 1), (0.3333333333, 2), (0.3333333333, 1)]],
             (5, 1): [[(0.5, 5), (0.5, 4)],
                      [(0.5, 3), (0.5, 4)],
                      [(0.25, 1), (0.25, 2), (0.25, 3), (0.25, 4)],
                      [(0.3333333333, 2), (0.3333333333, 0), (0.3333333333, 2)],
                      [(0.3333333333, 4), (0.3333333333, 5), (0.3333333333, 4)]
                      ]
            
            }

if __name__ == "__main__":
    print DEFAULT_MOVEMENT_PROBS
    print MIDDLE_VOICES_MOVEMENT_PROBS
    print BASS_MOVEMENT_PROBS
    print ORNAMENTS.keys()
    print ORNAMENTS

