from roqba.static.meters import METERS
from roqba.utilities.behaviour_dict import BehaviourDict

settings = {'number_of_voices': 4,
            'voice_registers': ['BASS', 'MID', 'MID', 'HIGH'],
            # 'voice_registers': ['ROCK_BASS', 'MID', 'MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 ['SLAVE', 2], 'AUTONOMOUS'],
            'PD_HOST': 'localhost',
            'PD_PORT': 12321,
            'gui': True,
            'GUI_HOST': 'localhost',
            'TO_GUI_PORT': 12322,
            'FROM_GUI_PORT': 12323,
            'track_voices_length': 666,
            'lowest_note_num': 0,
            'highest_note_num': 127,
            'composer': 'baroq',
            'notate': True
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
    'follow_bar_sequence': False, # alt: True
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
        'settings': {},
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
            'voice_registers': ['ROCK_BASS', 'LOW_MID', 'LOW_MID', 'HIGH'],
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS',
                                 ['SLAVE', 1], 'AUTONOMOUS'],
        },
        "behaviour": {
            "speed": 0.2,
            'max_speed': 0.5,
            'caesura_prob': 0.001,
            'min_speed': 0.08,
            "shuffle_delay": 0.02,
            'follow_bar_sequence': True,
            #'bar_sequence': [6, 6, 4, 3, 2, 3],
            'bar_sequence': [6, 4, 2, 3],
            'automate_meters': False,
            "meter": (15, (3, 3, 2, 3, 2, 2)),
            "meters": [(15, (3, 3, 2, 3, 2, 2))],
            'common_note_duration': False,
            'automate_binaural_diffs': False,
            'binaural_diff': 0.666,
            'max_binaural_diff': 3,
            'half_beat': False,
            'automate_speed_change': False,
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
            }
        }
    },
    "bulgarian": {
        "settings": {'composer': 'baroq'},
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
            'binaural_diff': 0.666,
            'max_binaural_diff': 10
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
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', ['SLAVE', 3]],
            'composer': 'amadinda'},
        'behaviour': {
            'adsr': [10, 10, 5, 20],
            'max_adsr': [20, 20, 30, 666],
            'min_adsr': [7, 7, 2, 10],
            'automate_adsr': True,
            'automate_binaural_diffs': True,  # alt: False
            'automate_microspeed_change': True,
            'microspeed_variation': 0.08,
            'microspeed_max_speed_in_hz': 2,
            'automate_pan': False,
            'automate_num_partials': True,
            'automate_slide': False,
            'automate_speed_change': True,
            'automate_wavetables': True,
            'binaural_diff': 0.3333,
            'common_adsr': True,
            'common_wavetables': True,
            'default_num_partial': 5,
            'default_pan_position': 0,
            'half_beat': True,
            'max_binaural_diff': 1.2,
            'max_num_partials': 9,
            'max_speed': 0.17,
            "max_shuffle": 0.05,
            'microvolume_variation': 0.9,
            'microvolume_max_speed_in_hz': 5,
            'meter': (24, (2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)),
            'min_speed': 0.08,
            'sequence_length': 12,
            'number_of_tones_in_3rd_voice': 4,
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
            "speed_target": 0.25,
            'tone_range': 12,
            'transpose': 6,
            'transposings': [6, 7, 8, 9],
            'wavetable_specs': [['harmonic', ['all']]],
        }
    },
    'rendezvous': {
        'settings': {
            'voice_behaviours': ['AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS', 'AUTONOMOUS'],
            'enable_adsr': False,
            'composer': 'rendezvous'},
        'behaviour': {
            'max_speed': 0.25,
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
    }
}


if "meters" in behaviour.keys() and type(behaviour["meters"][0]) == list:
    behaviour["meters"] = sum(behaviour["meters"], [])
