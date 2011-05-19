'''this module contains meter-constants'''

METERS = {
    8: {
        "human": 8,
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
    6: {
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
    }
}
