'''this module holds set of attributes that should create an interesting 
melody creation environment
'''

from scales_and_harmonies import *
from movement_probabilities import *

registers = {
    "BASS": {
        "name": "BASS",
        "voice_composer_attrs": {
              "note_length_groupings": "HEAVY_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.005,
              "legato_prob": 0.02,
              "range": [21, 33]
              }
    }, 
    "MID": {
        "name":"MID",
        "voice_composer_attrs": {
              "note_length_groupings": "DEFAULT_GROUPINGS"},
        "voice_attrs":{
              "embellishment_prob": 0.01,
              "legato_prob": 0.1,
              "pause_prob": 0.1,
              "range":[30, 45]},
    },
    "HIGH": {
        "name":"HIGH",
        "voice_composer_attrs": {
            "note_length_groupings": "TERNARY_GROUPINGS"},
        "voice_attrs":{
            "embellishment_prob": 0.015,
              "legato_prob": 0.05,
              "pause_prob": 0.03,
            "range":[35, 48]}
    }
}

melody_sets = {
  "roqba" : {
    "lead": {
       "scale": DIATONIC,
       "grouping": "ternary",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.01,
       "change_rhythm_after_times" : 1,
       "movement": DEFAULT_MOVEMENT_PROBS,
       "range" : [35, 48]
    },
    "alto": {
       "scale": DIATONIC,
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [30, 45]
    },
    "tenor": {
       "scale": DIATONIC,
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [27, 42]
    },
    "bass": {
       "scale": DIATONIC,
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
       "scale": PENTA_MINOR,
       "grouping": "ternary",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.01,
       "change_rhythm_after_times" : 1,
       "movement": DEFAULT_MOVEMENT_PROBS,
       "range" : [28, 36]
    },
    "alto": {
       "scale": PENTA_MINOR,
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [20, 33]
    },
    "tenor": {
       "scale": PENTA_MINOR,
       "grouping": "default",
       "slide" : True,
       "slide_duration_prop" : 0.1,
       "embellishment_prob" : 0.015,
       "change_rhythm_after_times" : 4,
       "movement": MIDDLE_VOICES_MOVEMENT_PROBS,
       "range" : [18, 31]
    },
    "bass": {
       "scale": PENTA_MINOR,
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
    print melody_sets
    print registers
