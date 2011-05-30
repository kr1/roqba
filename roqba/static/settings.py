
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
             'automate_speed_change': True,
             "max_speed": 0.3,
             "min_speed": 0.12,
             # speed-target:
             # 0.5 means that the average of all speeds will be
             # +/- in the middle of the given range
             # 0.25 means that the average of speeds will be at the first
             # quarter of the range
             "speed_target": 0.25,
             "speed_change": "leap",  # alt:"transition"
             'slide_in_msecs': 200,
             "shuffle_delay": 0.1,  # keep this between 0 and MAX_SHUFFLE
             'default_behaviour': "AUTONOMOUS",
             "max_shuffle": 0.1,
             'automate_meters': True,
             'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
             #'meters': [(12, (1, 2, 2, 1, 2, 2, 2)), 8],
             'meters': [[(12, (1, 2, 2, 1, 2, 2, 2))] * 4, 
                        [(7, (3, 2, 2))] * 10],
             #'meter': (5, (2, 3)),
             'transpose': 12,
             'automate_transpose': True,
             'transposings': [10, 11, 12, 12, 12, 12, 13, 14],
             'automate_binaural_diffs': True,  # alt: False
             'binaural_diff': 0.666,
             'max_binaural_diff': 10,
             'slide_duration_msecs': 100,
             'default_slide_duration_prop': 0.666,  # proportion
             'automate_note_duration_prop': True,
             'automate_note_duration_min_max': [0.1, 3.3],
             'common_note_duration': True,
             'default_note_duration_prop': 0.8,  # proportion
             'embellishment_speed_lim': 0.666,
             'default_pause_prob': 0.03,
             'default_embellishment_prob': 0.005
            }

styles = {"bulgarian": {
              "settings": {
               },
               "behaviour": {
                   'automate_meters': True,
                   "meter": (7, (3, 2, 2)),
                   "meters": [
                       (5, (2, 3)),
                       (5, (3, 2)),
                       (7, (3, 2, 2))
                   ],
                   "speed": 0.17,
                   "max_speed": 0.25,
                   "min_speed": 0.1,
                   "speed_change": "leap",  # alt:"transition"
                   'embellishment_speed_lim': 0.5,
                   'default_pause_prob': 0.07,
                   'default_embellishment_prob': 0.05,
                   "max_shuffle": 0.2,  #todo: check possibility for - 
                   ## constraints on dual and triple grouping
                   'common_note_duration': False,
                   'automate_binaural_diffs': False,
                   'binaural_diff': 0.666
               } 
         }
}

style = None

if style:
    behaviour.update(styles["behaviour"])

if "meters" in behaviour.keys() and type(behaviour["meters"][0]) == list:
    behaviour["meters"] = sum(behaviour["meters"], [])

if __name__ == "__main__":
    print styles
