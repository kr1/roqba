import os
from roqba.static.meters import METERS
from roqba.utilities.behaviour_dict import BehaviourDict

global_config = {
    'automate_style': True,
    'style_change_prob': 0.3,
    'max_caesurae_of_same_style': 15,
    'min_caesurae_of_same_style': 5
}
settings = {'number_of_voices': 4,
            'voice_registers': ['BASS', 'MID', 'MID', 'HIGH'],
            # 'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 ['SLAVE', 2], 'AUTONOMOUS'],
            'enable_adsr': False,
            'PD_HOST': 'localhost',
            'PD_PORT': int(os.environ.get('ROQBA_TO_PD_PORT', '12321')),
            'gui': True,
            'GUI_HOST': 'localhost',
            'TO_GUI_PORT': 12322,
            'FROM_GUI_PORT': 12323,
            'track_voices_length': 666,
            'lowest_note_num': 0,
            'highest_note_num': 127,
            'composer': 'baroq',
            'notate': False,
            'start_scale': 'DIATONIC'
            }

behaviour = {
    'adsr': [10, 10, 5, 20],
    'max_adsr': [50, 50, 40, 666],
    'min_adsr': [2, 2, 3, 20],
    'common_adsr': True,
    'automate_adsr': True,
    'automate_microspeed_change': True,
    'microspeed_variation': 0.06,
    'microspeed_max_speed_in_hz': 0.3,
    'automate_microvolume_change': True,
    'microvolume_variation': 0.2,
    'microvolume_max_speed_in_hz': 0.4,
    'default_volume': 0.666,
    'has_percussion': True,
    'percussion_automate_vol': True,
    'percussion_max_vol': 0.17,
    'percussion_min_vol': 0,
    "speed": 0.3,
    'half_beat': False,
    'automate_speed_change': True,
    "max_speed": 0.3,
    "min_speed": 0.12,
    # speed-target:
    # 0.5 means that the average of all speeds will be
    # +/- in the middle of the given range
    # 0.25 means that the average of speeds will be at the first
    # quarter of the range (predominantly fast)
    "speed_target": 0.25,
    "speed_change": "leap",  # alt:"transition"
    'caesura_prob': 0.9,
    "shuffle_delay": 0.1,  # keep this between 0 and MAX_SHUFFLE
    'default_behaviour': "AUTONOMOUS",
    "max_shuffle": 0.1,
    "automate_scale": True,

    # METERS
    'automate_meters': True,
    'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
    'meters': METERS.keys(),

    # WAVETABLES
    'automate_wavetables': True,
    'wavetable_specs': sum([[['random', ['all', 'even', 'odd']]] * 3,
                           [['random_harmonic', ['all', 'even', 'odd']]] * 5,
                           [['harmonic', ['all', 'even', 'odd']]] * 10],
                           []),
    'automate_num_partials': True,
    'default_num_partial': 13,
    'max_num_partials': 15,
    'common_wavetables': False,

    # TRANSPOSING
    'transpose': 12,
    'automate_transpose': True,
    'transposings': [10, 11, 12, 12, 12, 12, 13, 14],

    # PAN RELATED
    'default_pan_position': 0,
    'automate_pan': 1,

    # BINAURAL DIFF RELATED
    'pan_controls_binaural_diff': False,
    'common_binaural_diff': True,
    'automate_binaural_diffs': True,  # alt: False
    'binaural_diff': 0.666,
    'max_binaural_diff': 10,

    # SLIDE RELATED
    'automate_slide': True,
    'use_proportional_slide_duration': False,  # proportion or msecs
    'slide_duration_msecs': 100,
    'slide_duration_prop': 0.666,  # proportion

    # NOTE DURATION RELATED
    'automate_note_duration_prop': True,
    'automate_note_duration_min_max': [0.1, 3.3],
    'common_note_duration': False,
    'default_note_duration_prop': 0.8,  # proportion

    # SEQUENCE / MELODY RELATED
    'follow_bar_sequence': False,  # alt: True
    'bar_sequence': [6, 6, 4, 3, 2, 3],
    'should_play_a_melody': False,  # alt: melody as list

    'embellishment_speed_lim': 0.666,
    'default_embellishment_prob': 0.005,
    'default_pause_prob': 0.03,
    'per_voice': {
        1: BehaviourDict({
            'slide_duration_msecs': 100,
            'slide_duration_prop': 0.666,  # proportion
            'use_proportional_slide_duration': False,  # proportion or msecs
            'automate_binaural_diffs': True,  # alt: False
            'binaural_diff': 0.666,
            'default_pan_position': 0.2,
            'automate_pan': 0.25,
            'max_binaural_diff': 5,
            'automate_note_duration_prop': True,
            'automate_note_duration_min_max': [0.1, 3.3]},
            name='voice 1'),
        2: BehaviourDict({
            'automate_wavetables': True,
            'wavetable_specs': sum([[['random', ['even']]] * 2,
                                   [['random_harmonic', ['even']]] * 5],
                                   []),
            'max_num_partials': 5,
            'automate_pan': 0.75},
            name='voice 2'),
        3: BehaviourDict({
            'automate_wavetables': True,
            'wavetable_specs': sum([[['random', ['odd', 'all']]] * 2,
                                   [['random_harmonic', ['odd', 'all']]] * 5],
                                   []),
            'max_num_partials': 5,
            'automate_pan': 0.75},
            name='voice 3'),
        4: BehaviourDict({
            'automate_pan': 1.0,
            'max_binaural_diff': 15,
            'slide_duration_prop': 0.666,  # proportion
            'use_proportional_slide_duration': False,  # proportion or msecs
            'should_play_a_melody': True,
            'max_num_partials': 6,
            'automate_note_duration_min_max': [0.6, 9.3]},
            name='voice 4')
    }
}

styles = {
    "slow_and_slidy": {
        'settings': {
            'composer': 'baroq',
            'number_of_voices': 4,
            'voice_registers': ['BASS', 'LOW_MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', ['SLAVE', 2]],
        },
        'behaviour': {
            'per_voice': {
                1: BehaviourDict({
                    'use_proportional_slide_duration': True
                }),
                2: BehaviourDict({
                    'use_proportional_slide_duration': True
                }),
                3: BehaviourDict({
                    'use_proportional_slide_duration': True
                }),
                4: BehaviourDict({
                    'use_proportional_slide_duration': True
                }),
            },
            'max_speed': 1.2,
            'automate_slide': True,
            'slide_duration_prop': 1.0,
            'use_proportional_slide_duration': True,
            'transposings':  [1, 2, 3, 3, 3, 3, 4, 5],
            'speed_target': 0.45
        }
    },
    "fixed_meter_playalong": {
        "settings": {
            'composer': 'baroq',
            'number_of_voices': 3,
            'voice_registers': ['BASS', 'LOW_MID', 'LOW_MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', ['SLAVE', 2]],
        },
        "behaviour": {
            "speed": 0.2,
            'automate_adsr': True,
            'automate_wavetables': True,
            'automate_microspeed_change': False,
            'common_wavetables': False,
            'max_speed': 0.5,
            'caesura_prob': 0.07,
            'slide_duration_prop': 0.1,
            'min_speed': 0.08,
            "shuffle_delay": 0.02,
            'follow_bar_sequence': True,
            'bar_sequence': [5, 5, 5, 5, 2, 2, 2, 2],
            # 'bar_sequence': [6, 6, 4, 3, 2, 3],
            # 'bar_sequence': [1, 1, 1, 1, 4,
            #                  1, 1, 1, 1, 2, 6, 3, 2],
            'adsr': [10, 10, 5, 20],
            'automate_meters': False,
            # "meter": (15, (3, 3, 2, 3, 2, 2)),
            "meter": (23, (3, 3, 2, 3, 3, 2, 3, 2, 2)),
            # "meter": (30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2)),
            "meters": [(15, (3, 3, 2, 3, 2, 2))],
            'common_note_duration': False,
            'automate_binaural_diffs': False,
            'binaural_diff': 0.666,
            'max_binaural_diff': 3,
            'half_beat': False,
            'automate_speed_change': False,
            'per_voice': {
                1: BehaviourDict({
                    'adsr': [20, 200, 10, 200],
                    'use_proportional_slide_duration': True
                }),
                2: BehaviourDict({
                    'adsr': [10, 120, 30, 200],
                    'use_proportional_slide_duration': True
                }),
                3: BehaviourDict({
                    'adsr': [20, 80, 10, 300],
                    'use_proportional_slide_duration': True
                }),
            }
        }
    },
    "bulgarian": {
        "settings": {
            'composer': 'baroq',
            'number_of_voices': 4,
            'voice_registers': ['BASS', 'LOW_MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', ['SLAVE', 2]],
        },
        "behaviour": {
            'automate_meters': True,
            "meter": (7, (3, 2, 2)),
            "meters": [
                [(5, (2, 3))] * 2,
                [(5, (3, 2))] * 5,
                [(7, (3, 2, 2))] * 12,
                [(11, (3, 3, 3, 2))] * 5,
                [(12, (1, 2, 2, 1, 2, 2, 2))] * 3,
                [(15, (3, 3, 2, 3, 2, 2))] * 7,
                [(30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2))] * 10,
            ],
            "speed": 0.17,
            "max_speed": 0.25,
            "min_speed": 0.1,
            "speed_change": "leap",  # alt:"transition"
            'embellishment_speed_lim': 0.5,
            'default_pause_prob': 0.07,
            'default_embellishment_prob': 0.05,
            "max_shuffle": 0.2,  # todo: check possibility for -
            # constraints on dual and triple grouping
            'common_note_duration': False,
            'automate_binaural_diffs': False,
            'automate_scale': True,
            'binaural_diff': 0.666,
            'max_binaural_diff': 10,
            'caesura_prob': 0.15,
            'per_voice': {
                1: BehaviourDict({}),
                2: BehaviourDict({}),
                3: BehaviourDict({}),
                4: BehaviourDict({}),
            },
        }
    },
    "rock": {
        "settings": {
            'composer': 'baroq',
            'number_of_voices': 4,
            'voice_registers': ['ROCK_BASS', 'FLAT_MID', 'FLAT_MID', 'HIGH'],
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
            'default_pan_position': 0,
            'embellishment_speed_lim': 0.1,
            'default_pause_prob': 0.1,
            'default_embellishment_prob': 0.05,
            "max_shuffle": 0.3,  # todo: check possibility for -
            # constraints on dual and triple grouping
            'common_note_duration': False,
            'automate_note_duration_prop': True,
            'automate_note_duration_min_max': [0.9, 3.3],
            'automate_binaural_diffs': False,
            'binaural_diff': 0.666
        }
    },
    'amadinda': {
        'settings': {
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS'],
            'voice_registers': ['FLAT_MID', 'FLAT_MID', 'HIGH'],
            'number_of_voices': 3,
            'enable_adsr': True,
            'composer': 'amadinda'},
        'behaviour': {
            'pattern_played_maximum': 99,
            'pattern_played_minimum': 5,
            'adsr': [10, 10, 30, 120],
            'max_adsr': [30, 30, 30, 333],
            "automate_scale": True,
            'min_adsr': [7, 7, 20, 100],
            'automate_adsr': True,
            'automate_binaural_diffs': True,
            'automate_meters': True,
            'automate_microspeed_change': True,
            'microspeed_variation': 0.13,
            'microspeed_max_speed_in_hz': 2,
            'automate_pan': False,
            'automate_slide': False,
            'automate_speed_change': True,
            'binaural_diff': 0.666,
            'common_adsr': True,
            'common_binaural_diff': False,
            'default_pan_position': 0,
            'half_beat': True,
            'max_binaural_diff': 6.2,
            'max_speed': 0.27,
            "max_shuffle": 0.05,
            'microvolume_variation': 0.9,
            'microvolume_max_speed_in_hz': 5,
            "meters": [
                [(9, (2, 1, 1, 2, 1, 1, 1))] * 2,
                [(9, (2, 1, 2, 1, 1, 1, 1))] * 2,
                [(12, (2, 2, 2, 1, 2, 2 ,1))] * 2,
                [(12, (2, 2, 2, 1, 1, 1, 2 ,1))] * 2,
                [(18, (2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1))] * 5,
                [(18, (2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1))] * 5,
                [(24, (2, 2, 2, 1, 1, 1, 2 ,1, 2, 2, 2, 1, 2, 2 ,1))] * 5,
                [(36, (2, 2, 2, 1, 1, 1, 2 ,1, 2, 2, 2, 1, 2, 2 ,1, 2, 2, 2, 1, 1, 1, 2 ,1))] * 4,
                [(36, (2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1))] * 5,
            ],
            'min_speed': 0.1,
            'sequence_length_grid': 6,
            'max_number_of_tones_in_3rd_voice': 4,
            'min_number_of_tones_in_3rd_voice': 2,
            'octave_offset': 6,
            'per_voice': {
                1: BehaviourDict({}),
                2: BehaviourDict({}),
                3: BehaviourDict({}),
                4: BehaviourDict({}),
            },
            'slide_duration_msecs': 0,
            'speed': 0.13,
            "speed_change": "leap",  # alt:"transition"
            "speed_target": 0.3,
            'tone_range': 12,
            'transpose': 6,
            'transposings': [6, 7, 8, 9],
            'wavetable_specs': [['harmonic', ['all']]],
            'automate_num_partials': True,
            'default_num_partial': 1,
            'max_num_partials': 4,
            'automate_wavetables': True,
            'common_wavetables': True,
        }
    },
    'rendezvous': {
        'settings': {
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS'],
            'enable_adsr': False,
            'composer': 'rendezvous'},
        'behaviour': {
            'max_speed': 0.75,
            'min_speed': 0.1,
            'speed': 0.1,
            'automate_slide': False,
            'default_embellishment_prob': 0.1,
            'adsr': [40, 40, 100, 20000],
            'half_beat': False,
            'automate_adsr': False,
            'transition_strategy': "direct",  # one of ['direct', 'conservative', 'lax', 'in_range',
                                              #         'outgoing', 'roles', 'random']
            'common_transitions': False,  # upward and downward movements should be parallel?
            'binaural_diff': 0.15,
            'fixed_rendezvous_length': False,  # boolean or number of ticks
            'min_rendezvous_length': 3,  # used as min random when length is not fixed
            'max_rendezvous_length': 3,  # used as max random when length is not fixed
            'min_rendezvous_tickoffset': 5,  # how long it takes min to rendezvous
            'max_rendezvous_tickoffset': 20,  # how long it takes max to rendezvous
            'num_rendezvous_between_caesurae': 10,
            'automate_note_duration_prop': False,
            'per_voice': {
                1: BehaviourDict({}),
                2: BehaviourDict({}),
                3: BehaviourDict({}),
                4: BehaviourDict({}),
            },
        }
    },
    'greek_enharmonic': {
        "settings": {
            'composer': 'baroq',
            'number_of_voices': 4,
            'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 ['SLAVE', 2], 'AUTONOMOUS'],
            'start_scale': 'GREEK_ENHARMONIC'},
        "behaviour": {
            'adsr': [40, 40, 100, 20000],
            'automate_adsr': True,
            'automate_binaural_diffs': False,
            'automate_meters': True,
            "automate_scale": False,
            'automate_slide': True,
            'automate_note_duration_prop': False,
            'binaural_diff': 0.333,
            'common_note_duration': True,
            'common_transitions': False,  # upward and downward movements should be parallel?
            'default_pause_prob': 0.07,
            'default_embellishment_prob': 0.3,
            'embellishment_speed_lim': 0.7,
            'follow_bar_sequence': False,
            'half_beat': False,
            "max_shuffle": 0.2,  # todo: check possibility for -
            "max_speed": 0.8,
            "min_speed": 0.1,
            "meters": [
                [(5, (2, 3))] * 2,
                [(5, (3, 2))] * 5,
                [(7, (3, 2, 2))] * 5,
                [(7, (2, 3, 2))] * 5,
                [(7, (2, 2, 3))] * 5,
                [(9, (2, 2, 2, 3))] * 10,
                [(11, (3, 3, 3, 2))] * 5,
                [(12, (1, 2, 2, 1, 2, 2, 2))] * 3,
                [(15, (3, 3, 2, 3, 2, 2))] * 7,
                [(30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2))] * 10,
            ],
            "speed": 0.17,
            "speed_change": "leap",  # alt:"transition"
            'transition_strategy': "direct",  # one of ['direct', 'conservative', 'lax', 'in_range',
                                              #         'outgoing', 'roles', 'random']
            'per_voice': {
                1: BehaviourDict({}),
                2: BehaviourDict({}),
                3: BehaviourDict({}),
                4: BehaviourDict({}),
            },
            'should_play_a_melody': False,
        }
    },
    'greek_chromatic': {
        "settings": {
            'composer': 'baroq',
            'number_of_voices': 4,
            'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 ['SLAVE', 2], 'AUTONOMOUS'],
            'start_scale': 'GREEK_CHROMATIC'},
        "behaviour": {
            'adsr': [40, 40, 100, 20000],
            'automate_adsr': False,
            'automate_binaural_diffs': False,
            'automate_meters': True,
            "automate_scale": False,
            'automate_slide': False,
            'automate_note_duration_prop': False,
            'binaural_diff': 0.666,
            'common_note_duration': False,
            'common_transitions': False,  # upward and downward movements should be parallel?
            'default_pause_prob': 0.07,
            'default_embellishment_prob': 0.1,
            'embellishment_speed_lim': 0.5,
            'follow_bar_sequence': False,
            'half_beat': False,
            'max_binaural_diff': 10,
            "max_shuffle": 0.2,  # todo: check possibility for -
            "max_speed": 0.25,
            "min_speed": 0.1,
            "meters": [
                [(5, (2, 3))] * 2,
                [(5, (3, 2))] * 5,
                [(7, (3, 2, 2))] * 5,
                [(7, (2, 3, 2))] * 5,
                [(7, (2, 2, 3))] * 5,
                [(9, (2, 2, 2, 3))] * 10,
                [(11, (3, 3, 3, 2))] * 5,
                [(12, (1, 2, 2, 1, 2, 2, 2))] * 3,
                [(15, (3, 3, 2, 3, 2, 2))] * 7,
                [(30, (3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2))] * 10,
            ],
            "speed": 0.17,
            "speed_change": "leap",  # alt:"transition"
            'transition_strategy': "direct",  # one of ['direct', 'conservative', 'lax', 'in_range',
                                              #         'outgoing', 'roles', 'random']
            'per_voice': {
                1: BehaviourDict({}),
                2: BehaviourDict({}),
                3: BehaviourDict({}),
                4: BehaviourDict({}),
            },
            'should_play_a_melody': False,
        }
    },
    'aulos': {
        'settings': {
            'number_of_voices': 2,
            'voice_registers': ['FLAT_MID', 'FLAT_MID'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS'],
            'enable_adsr': True,
            'gui': True,
            'composer': 'baroq',
            'notate': True,
            'start_scale': 'GREEK_CHROMATIC' },
        'behaviour': {
            'max_adsr': [2000, 2000, 100, 30],
            'min_adsr': [10, 10, 40, 5],
            'automate_microspeed_change': True,
            'microspeed_variation': 0.06,
            'microspeed_max_speed_in_hz': 0.05,
            'automate_microvolume_change': True,
            'microvolume_variation': 1.8,
            'microvolume_max_speed_in_hz': 0.4,
            'default_volume': 0.666,
            "speed": 0.3,
            'half_beat': True,
            'automate_speed_change': True,
            'has_percussion': True,
            'percussion_automate_vol': True,
            'percussion_max_vol': 0.25,
            'percussion_min_vol': 0,
            "max_speed": 1.2,
            "min_speed": 0.08,
            # speed-target:
            # 0.5 means that the average of all speeds will be
            # +/- in the middle of the given range
            # 0.25 means that the average of speeds will be at the first
            # quarter of the range (predominantly fast)
            "speed_target": 0.2,
            "speed_change": "leap",  # alt:"transition"
            'caesura_prob': 0.05,
            "shuffle_delay": 0.05,  # keep this between 0 and MAX_SHUFFLE
            'default_behaviour': "AUTONOMOUS",
            "max_shuffle": 0.3,
            "automate_scale": True,

            # METERS
            'automate_meters': True,
            'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
            'meters': METERS.keys(),

            # WAVETABLES
            'automate_wavetables': True,
            #'wavetable_specs': sum([[['random_harmonic', ['all', 'odd']]]] * 5,
            'wavetable_specs': sum([[['harmonic', ['all']]]] * 5,
                                   []),
            'automate_num_partials': True,
            'default_num_partial': 3,
            'max_num_partials': 5,
            'common_wavetables': True,

            # TRANSPOSING
            'transpose': 12,
            'automate_transpose': True,
            'transposings': [10, 11, 12, 12, 12, 12, 13, 14],

            # PAN RELATED
            'default_pan_position': 0,
            'automate_pan': 1,

            # BINAURAL DIFF RELATED
            'pan_controls_binaural_diff': False,
            'common_binaural_diff': True,
            'automate_binaural_diffs': True,  # alt: False
            'binaural_diff': 0.666,
            'max_binaural_diff': 10,

            # SLIDE RELATED
            'automate_slide': True,
            'use_proportional_slide_duration': False,  # proportion or msecs
            'slide_duration_msecs': 100,
            'slide_duration_prop': 0.666,  # proportion

            # NOTE DURATION RELATED
            'automate_note_duration_prop': False,
            'automate_note_duration_min_max': [0.1, 3.3],
            'common_note_duration': True,
            'default_note_duration_prop': 3.5,  # proportion

            # SEQUENCE / MELODY RELATED
            'follow_bar_sequence': False,  # alt: True

            'embellishment_speed_lim': 0.3,
            'default_embellishment_prob': 0.07,
            'default_pause_prob': 0.22,
            'per_voice': {
                1: BehaviourDict({
                    'slide_duration_msecs': 100,
                    'slide_duration_prop': 0.666,  # proportion
                    'use_proportional_slide_duration': False,  # proportion or msecs
                    'automate_binaural_diffs': True,  # alt: False
                    'binaural_diff': 0.666,
                    'default_pan_position': 1,
                    'automate_pan': 1,
                    'max_binaural_diff': 5},
                    name='voice 1'),
                2: BehaviourDict({
                    'default_pan_position': 0,
                    'automate_pan': 1},
                    name='voice 2'),
            }
        }
    },
    'usualis': {
        'settings': {
            'number_of_voices': 4,
            'voice_registers': ['MID', 'MID', 'MID', 'MID'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS'],
            'enable_adsr': False,
            'humanize_oscillator_tuning': 0.04,
            'gui': True,
            'composer': 'usualis',
            'notate': False,
            'start_scale': 'DIATONIC' },
        'behaviour': {
            'adsr': [10, 10, 5, 20],
            'automate_adsr': False,
            'max_adsr': [7, 7, 90, 3666],
            'min_adsr': [2, 2, 70, 2666],
            'max_triple_length_prob': 0.1,
            'min_triple_length_prob': 0.05,
            'max_double_length_prob': 0.2,
            'min_double_length_prob': 0.08,
            'min_phrase_length': 20,
            'drone_prob': 0.37,
            'automate_microspeed_change': True,
            'microspeed_variation': 0.06,
            'microspeed_max_speed_in_hz': 0.3,
            'automate_microvolume_change': True,
            'microvolume_variation': 0.2,
            'microvolume_max_speed_in_hz': 0.4,
            'default_volume': 0.666,
            "speed": 0.3,
            'half_beat': True,
            'automate_speed_change': True,
            'has_percussion': False,
            "max_speed": 0.8,
            "min_speed": 0.4,
            # speed-target:
            # 0.5 means that the average of all speeds will be
            # +/- in the middle of the given range
            # 0.25 means that the average of speeds will be at the first
            # quarter of the range (predominantly fast)
            "speed_target": 0.5,
            "speed_change": "leap",  # alt:"transition"
            'caesura_prob': 1, #any caesura by the composer is accepted by the director
            "shuffle_delay": 0.01,  # keep this between 0 and MAX_SHUFFLE
            'default_behaviour': "AUTONOMOUS",
            "max_shuffle": 0.6,
            "automate_scale": True,

            # METERS
            'automate_meters': False,
            'meter': (12, (1, 2, 2, 1, 2, 2, 2)),
            'meters': METERS.keys(),

            # WAVETABLES
            'automate_wavetables': True,
            'wavetable_specs': sum([[['random', ['all', 'even', 'odd']]] * 3,
                                   [['random_harmonic', ['all', 'even', 'odd']]] * 5,
                                   [['harmonic', ['all', 'even', 'odd']]] * 10],
                                   []),
            'automate_num_partials': True,
            'default_num_partial': 3,
            'max_num_partials': 7,
            'common_wavetables': False,

            # TRANSPOSING
            'transpose': 12,
            'automate_transpose': True,
            'transposings': [6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 9, 10, 11, 12, 12, 12, 12, 13, 14],

            # PAN RELATED
            'default_pan_position': 0,
            'automate_pan': 1,

            # BINAURAL DIFF RELATED
            'pan_controls_binaural_diff': False,
            'common_binaural_diff': True,
            'automate_binaural_diffs': True,  # alt: False
            'binaural_diff': 0.666,
            'max_binaural_diff': 5,

            # SLIDE RELATED
            'automate_slide': True,
            'use_proportional_slide_duration': False,  # proportion or msecs
            'slide_duration_msecs': 100,
            'slide_duration_prop': 0.666,  # proportion

            # NOTE DURATION RELATED
            'automate_note_duration_prop': True,
            'automate_note_duration_min_max': [0.1, 1.0],
            'common_note_duration': True,
            'default_note_duration_prop': 0.8,  # proportion

            # SEQUENCE / MELODY RELATED
            'follow_bar_sequence': False,  # alt: True

            'embellishment_speed_lim': 0.666,
            'default_embellishment_prob': 0.005,
            'default_pause_prob': 0.03,
            'per_voice': {
                1: BehaviourDict({
                    'slide_duration_msecs': 100,
                    'slide_duration_prop': 0.666,  # proportion
                    'use_proportional_slide_duration': False,  # proportion or msecs
                    'automate_binaural_diffs': True,  # alt: False
                    'binaural_diff': 0.666,
                    'default_pan_position': 1,
                    'automate_pan': 1,
                    'max_binaural_diff': 5,
                    'automate_note_duration_prop': True,
                    'automate_note_duration_min_max': [0.1, 3.3]},
                    name='voice 1'),
                2: BehaviourDict({
                    'default_pan_position': 0,
                    'automate_pan': 1},
                    name='voice 2'),
                3: BehaviourDict({
                    'default_pan_position': 0.25,
                    'automate_pan': 1},
                    name='voice 3'),
                4: BehaviourDict({
                    'default_pan_position': 0.75,
                    'automate_pan': 1},
                    name='voice 4'),
                }
            }
        }
    }


def flatten_meters(behaviour):
    if "meters" in behaviour.keys() and type(behaviour["meters"][0]) == list:
        behaviour["meters"] = sum(behaviour["meters"], [])

flatten_meters(behaviour)


def behaviour_and_settings_from_style(default_settings, style_name):
    if default_settings.styles.get(style_name):
        default_settings.settings.update(default_settings.styles[style_name]["settings"])
        default_settings.behaviour.update(default_settings.styles[style_name]["behaviour"])
    default_settings.behaviour["style"] = style_name
    flatten_meters(default_settings.behaviour)
    behaviour_dict = BehaviourDict(default_settings.behaviour.items(), name='global')
    return default_settings.settings, default_settings.behaviour, behaviour_dict
