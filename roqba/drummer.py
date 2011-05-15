from random import random, choice

from sine_controllers import MultiSine


class Drummer(object):
    def __init__(self,
                 composer,
                 meter=[0, 0, 0, 0, 0, 0]):
        self.composer = composer
        self.meter = meter
        self.create_pattern()
        self.peak_speed = 80
        self.mark_prob = 0.03
        self.empty_threshold = 0.2
        self.full_threshold = 0.99
        self.activation_level = "medium"  # ["low", "medium", "high"]
        self.pan_positions = {"low": 0,
                              "high": 0,
                              "cont": 0,
                              "tuned": 0,
                              "mark": 0}
        self.ctl_values = {
            "low": {"val": 150, "devi": 30},
            "high": {"val": 800, "devi": 30},
            "cont": {"val": 1200, "devi": 400,
                     "fun": MultiSine([0.1, 0.2, 0.77, 10], False).get_value},
            "tuned": {"val": 500, "devi": 100},
            "mark": {"val": 10000, "devi": 1000,
                     "fun": MultiSine([0.05, 0.02, 0.77, 10], False).get_value}
        }
        self.high_low_seq()
        self.generator = self.generate()
        self.generator.next()
        self.cont_accent_mult = 0.3
        self.mark_accent_mult = 0.1
        self.frame = {}

    def generate(self):
        while True:
            state = (yield)
            #print state["comp"].voices.values()
            sum_ = sum(map(lambda v: v.note_change and 1 or 0,
                              state["comp"].voices.values()))
            density = sum_ / float(len(state["comp"].voices))
            meter_pos = state['cycle_pos']
            #print meter_pos
            self.frame = {}
            for k, v in self.pattern.items():
                if v[meter_pos] or k == 'mark':
                    ## to-do make more dynamic
                    vol = 0.5
                    ctl = None
                    meta = None
                    if k == "cont":
                        confirm, vol, ctl, meta = self.cont_frame(state,
                                                                  density)
                    elif k == 'mark':
                        confirm, vol, ctl, meta = self.mark_frame(state,
                                                              density)
                    if not confirm:
                        continue
                    self.frame[k] = {"vol": vol,
                                     "pan": self.pan_positions[k],
                                     "ctl": ctl and int(ctl) or ctl,
                                     "meta": meta}

    def cont_frame(self, state, density):
        '''assembles the frame for the cont-voice'''
        meta = None
        if density > self.full_threshold:
            return (False, None, None, None)
        elif density < self.empty_threshold:
            meta = "empty"
        vol = 0.5 + state["weight"] * self.cont_accent_mult

        ## check if that value is callable
        if "fun" in self.ctl_values["cont"].keys():
            addendum = (self.ctl_values["cont"]["fun"]() *
                        self.ctl_values["cont"]["devi"])
        else:
            addendum = (random() * self.ctl_values["cont"]["devi"] *
                                  choice([1, -1]))
        ctl = self.ctl_values["cont"]["val"] + addendum
        return (True, vol, ctl, meta)

    def mark_frame(self, state, density):
        '''assembles the frame for the mark-voice'''
        if (density < self.full_threshold) or random() > self.mark_prob:
            return (False, None, None, None)
        elif density > self.full_threshold:
            meta = "mark"
        vol = 0.5 + state["weight"] * self.mark_accent_mult
        if "fun" in self.ctl_values["mark"].keys():
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
        indeces = xrange(len(self.meter))
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
            self.pattern = {"low": map(lambda x: 1 if x == 2 else 0,
                                        self.meter),
                            "high":  map(lambda x: 1 if x == 1 else 0,
                                         self.meter),
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
        indeces = xrange(len(self.pattern["low"]))
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
        for k, v in self.pattern.items():
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
