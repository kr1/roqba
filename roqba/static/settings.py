
settings = {'number_of_voices': 4,
            'voice_registers': ['BASS', 'MID', 'MID', 'HIGH'],
            #'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 
                                 'SLAVE', 'AUTONOMOUS'],
            'PD_HOST': 'localhost',
            'PD_PORT': 12321,
            'track_voices_length': 666,
            'lowest_note_num': 0,
            'highest_note_num': 127,
            }

behaviour = {"speed": 0.3,
             "max_speed": 0.3,
             "min_speed": 0.12,
             # speed-target:
             # 0.5 means that the average of all speeds will be
             # +/- in the middle of the given range
             # 0.25 means that the average of speeds will be at the first
             # quarter of the range
             "speed_target": 0.25,
             'slide_in_msecs': 200,
             "speed_change": "leap",  # alt:"transition"
             "shuffle_delay": 0.1,  # keep this between 0 and MAX_SHUFFLE
             'default_behaviour': "AUTONOMOUS",
             "max_shuffle": 0.1,
             'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
             #'meter': (5, (2, 3)),
             'transpose': 12,
             'automate_transpose': True,
             'automate_meters': False,
             'transposings': [10, 11, 12, 12, 12, 12, 13, 14],
             'binaural_diff': 0.666,
             'max_binaural_diff': 10,
             'slide_duration_msecs': 100,
             'automate_binaural_diffs': True,  # alt: False
             'default_slide_duration_prop': 0.666,  # proportion
             'automate_note_duration_prop': True,
             'automate_note_duration_min_max': [0.1, 3.3],
             'common_note_duration': True,
             'default_note_duration_prop': 0.8,  # proportion
             'embellishment_speed_lim': 0.666,
             'default_pause_prob': 0.03,
             'default_embellishment_prob': 0.005
            }
