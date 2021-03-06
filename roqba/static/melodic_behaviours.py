'''this module holds sets of attributes to be used in creating
various melodic environments
'''

from .scales_and_harmonies import *
from .movement_probabilities import *

registers = {
    "BASS": {
        "name": "BASS",
        "sort_importance": 10,
        "voice_composer_attrs": {
              "note_length_groupings": "HEAVY_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.005,
              "legato_prob": 0.02,
              #"slide": True,
              #"slide_duration_prop": 0.1, 
              "change_rhythm_after_times": 8,
              "movement_probs": BASS_MOVEMENT_PROBS,
              "pause_prob": 0.1,
              "range": [21, 33]
              }
    },
    "ROCK_BASS": {
        "name": "ROCK_BASS",
        "sort_importance": 10,
        "voice_composer_attrs": {
              "note_length_groupings": "FAST_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.002,
              "legato_prob": 0.02,
              #"slide": True,
              #"slide_duration_prop": 0.1, 
              "change_rhythm_after_times": 8,
              "movement_probs": ROCK_BASS_MOVEMENT_PROBS,
              "pause_prob": 0.1,
              "range": [15, 24]
              }
    },
    "MID": {
        "name":"MID",
        "sort_importance": 5,
        "voice_composer_attrs": {
              "note_length_groupings": "DEFAULT_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.01,
              "legato_prob": 0.1,
              #"slide": True,
              #"slide_duration_prop": 0.1, 
              "change_rhythm_after_times": 4,
              "movement_probs": MIDDLE_VOICES_MOVEMENT_PROBS,
              "pause_prob": 0.1,
              "range":[30, 45]},
    },
    "LOW_MID": {
        "name":"LOW_MID",
        "sort_importance": 5,
        "voice_composer_attrs": {
              "note_length_groupings": "DEFAULT_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.01,
              "legato_prob": 0.1,
              #"slide": True,
              #"slide_duration_prop": 0.1,
              "change_rhythm_after_times": 10,
              "movement_probs": MIDDLE_VOICES_MOVEMENT_PROBS,
              "pause_prob": 0.1,
              "range":[22, 38]},
    },
    "FLAT_MID": {
        "name": "FLAT_MID",
        "sort_importance": 5,
        "voice_composer_attrs": {
              "note_length_groupings": "FAST_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.01,
              "legato_prob": 0.06,
              #"slide": True,
              #"slide_duration_prop": 0.1, 
              "change_rhythm_after_times": 4,
              "movement_probs": FLAT_MID_MOVEMENT_PROBS,
              "pause_prob": 0.1,
              "range": [27, 40]
              }
    },
    "HIGH": {
        "name":"HIGH",
        "sort_importance": 1,
        "voice_composer_attrs": {
            "note_length_groupings": "TERNARY_GROUPINGS"},
        "voice_attrs":{
            "embellishment_prob": 0.015,
            "legato_prob": 0.05,
            #"slide": True,
            #"slide_duration_prop": 0.2, 
            "change_rhythm_after_times": 1,
            "movement_probs": DEFAULT_MOVEMENT_PROBS,
            "pause_prob": 0.03,
            "range":[35, 48]}
    }
}

melody_sets = {
  "roqba" : {
    "lead": {
       "scale": "DIATONIC",
       "grouping": "ternary",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.01,
       "change_rhythm_after_times" : 1,
       "movement": DEFAULT_MOVEMENT_PROBS,
       "range" : [35, 48]
    },
    "alto": {
       "scale": "DIATONIC",
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [30, 45]
    },
    "tenor": {
       "scale": "DIATONIC",
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [27, 42]
    },
    "bass": {
       "scale": "DIATONIC",
       "grouping": "heavy",
       "slide" : True,
       "slide_duration_prop" : 0.3,
       "embellishment_prob" : 0.005,
       "change_rhythm_after_times" : 8,
       "movement": BASS_MOVEMENT_PROBS,
       "range" : [21, 33]
    }
  },
  "penta" : {
    "lead": {
       "scale": "PENTA_MINOR",
       "grouping": "ternary",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.01,
       "change_rhythm_after_times" : 1,
       "movement": DEFAULT_MOVEMENT_PROBS,
       "range" : [28, 36]
    },
    "alto": {
       "scale": "PENTA_MINOR",
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [20, 33]
    },
    "tenor": {
       "scale": "PENTA_MINOR",
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [18, 31]
    },
    "bass": {
       "scale": "PENTA_MINOR",
       "grouping": "heavy",
       "slide" : True,
       "slide_duration_prop" : 0.3,
       "embellishment_prob" : 0.01,
       "change_rhythm_after_times" : 8,
       "movement": BASS_MOVEMENT_PROBS,
       "range" : [11, 22]
    }
  }
}

if __name__ == "__main__":
    print(melody_sets)
    print(registers)
