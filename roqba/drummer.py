from collections import namedtuple
from random import random, choice

from .utilities.sine_controllers import MultiSine

ContFrame = namedtuple("ContFrame", 'confirm vol pan pan2 ctl ctl2 meta')


class Drummer(object):
    def __init__(self,
                 composer,
                 meter=[0, 0, 0, 0, 0, 0]):
        self.composer = composer
        self.meter = meter
        self.create_pattern()
        self.peak_speed = 100
        self.mark_prob = 0.09
        self.empty_threshold = 0.6
        self.full_threshold = 0.99
        self.activation_level = "medium"  # ["low", "medium", "high"]
        self.pan_positions = {"low": 0,
                              "high": 0,
                              "cont": 0,
                              "tuned": 0,
                              "mark": 0}
        self.new_pan_positions()
        self.ctl_values = {
            "low": {"val": 150, "devi": 30},
            "high": {"val": 800, "devi": 30},
            "cont": {"val": 1200, "devi": 400,
                     "fun": MultiSine([0.01, 0.2, 0.77, 6], False).get_value},
            "cont2": {"val": 2800, "devi": 1000,
                      "fun": MultiSine([0.05, 0.2, 0.47, 4.5], False).get_value},
            "cont_pan": {"val": 0, "devi": 1,
                         "fun": MultiSine([0.03, 0.35, 0.65, 4], False).get_value},
            "cont2_pan": {"val": 0, "devi": 1,
                          "fun": MultiSine([0.03, 0.25, 0.67, 4], False).get_value},
            "tuned": {"val": 500, "devi": 100},
            "mark": {"val": 10000, "devi": 1000,
                     "fun": MultiSine([0.05, 0.02, 0.77, 10], False).get_value}
        }
        self.high_low_seq()
        self.generator = self.generate()
        next(self.generator)
        self.cont_accent_mult = 0.3
        self.mark_accent_mult = 0.1
        self.frame = {}

    def new_pan_positions(self):
        for key in self.pan_positions:
            self.pan_positions[key] = random() * 2 - 1

    def generate(self):
        while True:
            state, cycle_pos = (yield)
            sum_ = sum([v.note_change and 1 or 0 for v in list(state["comp"].voices.values())])
            density = sum_ / float(len(state["comp"].voices))
            meter_pos = cycle_pos
            self.frame = {}
            for k, v in list(self.pattern.items()):
                if v[meter_pos] or k == 'mark':
                    #  to-do make more dynamic
                    vol = 0.5
                    ctl = None
                    meta = None
                    confirm_cont = True
                    confirm_mark = True
                    if k == "cont":
                        cont_frame = self.cont_frame(state,
                                                     density)
                        self.frame['cont'] = {"vol": cont_frame.vol,
                                              "pan": cont_frame.pan,
                                              "ctl": cont_frame.ctl,
                                              "meta": cont_frame.meta}
                        self.frame['cont2'] = {"vol": cont_frame.vol,
                                               "pan": cont_frame.pan2,
                                               "ctl": cont_frame.ctl2,
                                               "meta": cont_frame.meta}
                        continue
                    elif k == 'mark':
                        confirm_mark, vol, ctl, meta = self.mark_frame(state,
                                                                       density)
                    if not confirm_cont or not confirm_mark:
                        continue
                    self.frame[k] = {"vol": vol,
                                     "pan": self.pan_positions[k],
                                     "ctl": ctl and int(ctl) or ctl,
                                     "meta": meta}

    def cont_frame(self, state, density):
        '''assembles the frame for the cont-voice'''
        meta = None
        if density > self.full_threshold:
            return ContFrame(False, None, None, None, None, None, None)
        elif density < self.empty_threshold:
            meta = "empty"
        vol = 0.5 + state["weight"] * self.cont_accent_mult
        if "fun" in list(self.ctl_values["cont"].keys()):
            addendum = (self.ctl_values["cont"]["fun"]() *
                        self.ctl_values["cont"]["devi"])
            addendum2 = (self.ctl_values["cont2"]["fun"]() *
                         self.ctl_values["cont2"]["devi"])
            pan = (self.ctl_values["cont_pan"]["fun"]() *
                   self.ctl_values["cont_pan"]["devi"])
            pan2 = (self.ctl_values["cont2_pan"]["fun"]() *
                    self.ctl_values["cont2_pan"]["devi"])
        else:
            addendum = (random() * self.ctl_values["cont"]["devi"] *
                        choice([1, -1]))
            addendum = (random() * self.ctl_values["cont2"]["devi"] *
                        choice([1, -1]))
            pan = (random() * self.ctl_values["cont_pan"]["devi"] *
                   choice([1, -1]))
            pan2 = (random() * self.ctl_values["cont2_pan"]["devi"] *
                    choice([1, -1]))
        ctl = self.ctl_values["cont"]["val"] + addendum
        ctl2 = self.ctl_values["cont2"]["val"] + addendum2
        return ContFrame(True, vol, pan, pan2, ctl, ctl2, meta)

    def mark_frame(self, state, density):
        '''assembles the frame for the mark-voice'''
        meta = None
        if (density > self.full_threshold) or random() > self.mark_prob:
            return (False, None, None, None)
        elif density > self.full_threshold:
            meta = "mark"
        vol = 0.5 + state["weight"] * self.mark_accent_mult
        if "fun" in list(self.ctl_values["mark"].keys()):
            addendum = (self.ctl_values["mark"]["fun"]() *
                        self.ctl_values["mark"]["devi"])
        else:
            addendum = (random() * self.ctl_values["mark"]["devi"] *
                        choice([1, -1]))
        ctl = self.ctl_values["mark"]["val"] + addendum
        return True, vol, ctl, meta

    def create_pattern(self, patt=None):
        '''creates a drum pattern from a given (bass-)pattern

        as a fallback this method will create a (generic) pattern
        using the underlying meter'''
        indeces = range(len(self.meter))
        if patt:
            self.empty_pattern()
            next_trigger = "low"
            for p in patt:
                self.push_value(0)
                self.pattern["cont"][-1] = 1
                if not p == 0:
                    self.pattern[next_trigger][-1] = 1
                    next_trigger = "low" if next_trigger == "high" else "high"
        else:
            self.pattern = {"low": [1 if x == 2 else 0 for x in self.meter],
                            "high": [1 if x == 1 else 0 for x in self.meter],
                            "cont": [1 for n in indeces],
                            "tuned": [0 for n in indeces],
                            "mark": [0 for n in indeces]}
        self.smoothen()
        self.high_low_seq()

    def smoothen(self):
        '''post - creation method to smoothen loop-related duplications'''
        self.pattern

    def high_low_seq(self):
        '''creates a pattern consisting of the sequence of low-high changes

        format to be defined'''
        p = self.pattern
        res = []
        indeces = range(len(self.pattern["low"]))
        for i in indeces:
            if p["low"][i]:
                res.append(-1)
            elif p["high"][i]:
                res.append(1)
            else:
                res.append(0)
        self.high_low_pattern = res
        return res

    def push_value(self, val):
        '''append a value to all keys of the pattern'''
        for k, v in list(self.pattern.items()):
            v.append(val)

    def empty_pattern(self):
        '''initializes a empty pattern-dict

        keys are:
          - low (bass-drum function)
          - high (snare-function)
          - cont (continuous => hi-hat/ride cymbal function)
          - tuned (should allow melodies (from tom-tom upwards))
          - mark (special marker (crash, splash, etc))
          '''
        self.pattern = {"low": [],
                        "high": [],
                        "cont": [],
                        "tuned": [],
                        "mark": []}
