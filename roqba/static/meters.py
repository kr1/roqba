'''this module contains meter-constants'''

METERS = {
   (8, (4, 4)): {
        "human": (8, (4, 4)),
        "applied": [2, 0, 1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.333333
    },
    (8, (3, 3, 2)): {
        "human": (8, (3, 3, 2)),
        "applied": [2, 0, 0, 1, 0, 0, 1, 0],
        "max_shuffle": 0.1
    },
    (8, (2, 2, 2, 2)): {
        "human": (8, (2, 2, 2, 2)),
        "applied": [2, 0, 1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.333333
    },
    (5, (3, 2)): {
        "human": (5, (3, 2)),
        "applied": [2, 0, 0, 1, 0],
        "max_shuffle": 0.15
    },
    (5, (2, 3)): {
        "human": (5, (2, 3)),
        "applied": [2, 0, 1, 0, 0],
        "max_shuffle": 0.15
    },
    (6, (3, 3)): {
        "human": (6, (3, 3)),
        "applied": [2, 0, 0, 1, 0, 0],
        "max_shuffle": 0.1
    },
    (6, (2, 2, 2)): {
        "human": (6, (2, 2, 2)),
        "applied": [2, 0, 1, 0, 1, 0],
        "max_shuffle": 0.3333333
    },
    (7, (3, 2, 2)): {
        "human": (7, (3, 2, 2)),
        "applied": [2, 0, 0, 1, 0, 1, 0],
        "max_shuffle": 0.15
    },
    (9, (3, 3, 3)): {
        "human": (9, (3, 3, 3)),
        "applied": [2, 0, 0, 1, 0, 0, 1, 0, 0],
        "max_shuffle": 0.15
    },
    (11, (3, 3, 3, 2)): {
        "human": (12, (3, 3, 3, 2)),
        "applied": [2, 0, 0, 1, 0, 0,
                    1, 0, 0, 1, 0],
        "max_shuffle": 0.1
    },
    (12, (3, 3, 2, 2, 2)): {
        "human": (12, (3, 3, 2, 2, 2)),
        "applied": [2, 0, 0, 1, 0, 0,
                    1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.1
    },
    (12, (2, 2, 2, 3, 3)): {
        "human": (12, (2, 2, 2, 3, 3)),
        "applied": [2, 0, 1, 0, 1, 0,
                    1, 0, 0, 1, 0, 0],
        "max_shuffle": 0.1
    },
    (12, (1, 2, 2, 1, 2, 2, 2)): {
        "human": (12, (1, 2, 2, 1, 2, 2, 2)),
        "applied": [2, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.1
    },
    (15, (3, 3, 2, 3, 2, 2)): {
        "human": (12, (3, 3, 2, 3, 2, 2)),
        "applied": [2, 0, 0, 1, 0, 0, 2, 0,
                    2, 0, 0, 1, 0, 2, 0],
        "max_shuffle": 0.05
    },
    (24, (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)): {
        "human": (24, (1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2)),
        "applied": [2, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 0,
                    2, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.06
    },
    (24, (2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)): {
        "human": (24, (2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)),
        "applied": [2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1,
                    2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1],
        "max_shuffle": 0.06
    },
    (30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2)): {
        "human": (30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2)),
        "applied": [2, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 0,
                    2, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 0],
        "max_shuffle": 0.05
    }
}
