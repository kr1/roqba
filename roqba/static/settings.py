from roqba.static.meters import METERS
from roqba.utilities.behaviour_dict import BehaviourDict

settings = {'number_of_voices': 4,
            'voice_registers': ['BASS', 'MID', 'MID', 'HIGH'],
            #'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 'SLAVE', 'AUTONOMOUS'],
            'PD_HOST': 'localhost',
            'PD_PORT': 12321,
            'gui': True,
            'GUI_HOST': 'localhost',
            'TO_GUI_PORT': 12322,
            'FROM_GUI_PORT': 12323,
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
             'caesura_prob': 0.9,   
             "shuffle_delay": 0.1,  # keep this between 0 and MAX_SHUFFLE
             'default_behaviour': "AUTONOMOUS",
             "max_shuffle": 0.1,
             # METERS
             'automate_meters': True,
             'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
             'meters': METERS.keys(),
             #'meters': [(12, (1, 2, 2, 1, 2, 2, 2)), 8],
             #'meters': [[(12, (1, 2, 2, 1, 2, 2, 2))] * 4,
             #           [(7, (3, 2, 2))] * 10],
             #'meter': (5, (2, 3)),
             # WAVETABLES
             'automate_wavetables': sum([[['random', ['all', 'even', 'odd']]] * 2,
                                         [['random_harmonic', ['all', 'even', 'odd']]] * 5,
                                         [['harmonic', ['all', 'even', 'odd']]] * 10], 
                                         []),
             #'automate_wavetables': False,
             'automate_num_partials': True,
             'default_num_partial': 13,
             'max_num_partials': 15,
             'common_wavetables': False,
             'transpose': 12,
             'automate_transpose': True,
             'transposings': [10, 11, 12, 12, 12, 12, 13, 14],
             'default_pan_position': 0,
             'automate_pan' : 1,
             'pan_controls_binaural_diff': True,
             'automate_binaural_diffs': True,  # alt: False
             'binaural_diff': 0.666,
             'max_binaural_diff': 10,
             'slide_duration_msecs': 100, #TODO : defined twice - which is read?
             'automate_slide': True,
             'default_slide_duration_prop': 0.666,  # proportion
             'automate_note_duration_prop': True,
             'automate_note_duration_min_max': [0.1, 3.3],
             'common_note_duration': False,
             'default_note_duration_prop': 0.8,  # proportion
             'embellishment_speed_lim': 0.666,
             'default_pause_prob': 0.03,
             'default_embellishment_prob': 0.005,
             'should_play_a_melody': False,  #alt: melody as list
             'per_voice': {
                1: BehaviourDict({
                    'slide_duration_msecs': 100,
                    'default_slide_duration_prop': 0.666,  # proportion
                    'automate_binaural_diffs': True,  # alt: False
                    'binaural_diff': 0.666,
                    'default_pan_position': 0.2,
                    'automate_pan' : 0.25,
                    'max_binaural_diff': 5,
                    'automate_note_duration_prop': True,
                    'automate_note_duration_min_max': [0.1, 3.3]
                    }),
                2: BehaviourDict({
                    'automate_wavetables': sum([[['random', ['even']]] * 2,
                                         [['random_harmonic', ['even']]] * 5],
                                         []),
                    'max_num_partials': 5,
                    'automate_pan' : 0.75
                    }),
                3: BehaviourDict({
                    'automate_wavetables': sum([[['random', ['odd']]] * 2,
                                         [['random_harmonic', ['odd']]] * 5],
                                         []),
                    'max_num_partials': 5,
                    'automate_pan' : 0.75
                    }),
                4: BehaviourDict({
                    'automate_pan' : 1.0,
                    'max_binaural_diff': 15,
                    'default_slide_duration_prop': 0.96,  # proportion
                    #'should_play_a_melody': [0, [0, 1, 1, 2, -2, -1, -1, -3, 3, -3, 3]],  #alt: False
                    'should_play_a_melody': [4, [[0, 3], [0, 3], [0, 2], [1, 2], [-2, 2], 
                                                 [1, 3], [-2, 3], [-2, 6], [4, 3], [0, 3], 
                                                 [0, 2], [3, 2], [-2, 2], [-1, 6], [-2, 6]]],  #alt: False
                    'max_num_partials': 3,
                    'automate_note_duration_min_max': [0.6, 9.3]
                })
              } 
            }

styles = {"bulgarian": {
              "settings": {
               },
               "behaviour": {
                   'automate_meters': True,
                   "meter": (7, (3, 2, 2)),
                   "meters": [
                       [(5, (2, 3))] * 2,
                       [(5, (3, 2))] * 5,
                       [(7, (3, 2, 2))] * 12
                   ],
                   "speed": 0.17,
                   "max_speed": 0.25,
                   "min_speed": 0.1,
                   "speed_change": "leap",  # alt:"transition"
                   'embellishment_speed_lim': 0.5,
                   'default_pause_prob': 0.07,
                   'default_embellishment_prob': 0.05,
                   "max_shuffle": 0.2,  # todo: check possibility for -
                   ## constraints on dual and triple grouping
                   'common_note_duration': False,
                   'automate_binaural_diffs': False,
                   'binaural_diff': 0.666,
                   'max_binaural_diff': 10
               }
         },
         "rock": {
              "settings": {
                  'number_of_voices': 4,
                  'voice_registers': ['ROCK_BASS', 'FLAT_MID', 'FLAT_MID',
                  'HIGH'],
                  'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                       ['SLAVE', 2], 'AUTONOMOUS'],

               },
               "behaviour": {
                   'automate_meters': True,
                   "meter": (8, (4, 4)),
                   "meters": [
                       [(8, (4, 4))] * 2,
                       [(8, (3, 3, 2))] * 1
                   ],
                   "speed": 0.25,
                   'automate_speed_change': True,
                   "max_speed": 0.25,
                   "min_speed": 0.18,
                   "speed_change": "leap",  # alt:"transition"
                   'embellishment_speed_lim': 0.1,
                   'default_pause_prob': 0.1,
                   'default_embellishment_prob': 0.05,
                   "max_shuffle": 0.3,  # todo: check possibility for -
                   ## constraints on dual and triple grouping
                   'common_note_duration': False,
                   'automate_note_duration_prop': True,
                   'automate_note_duration_min_max': [0.9, 3.3],
                   'automate_binaural_diffs': False,
                   'binaural_diff': 0.666
               }

         }
}

#style = 'rock'
style = None

if style:
    settings.update(styles[style]["settings"])
    behaviour.update(styles[style]["behaviour"])
    behaviour["style"] = style

if "meters" in behaviour.keys() and type(behaviour["meters"][0]) == list:
    behaviour["meters"] = sum(behaviour["meters"], [])

if __name__ == "__main__":
    print styles
    print behaviour 
