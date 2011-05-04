import random

class Drummer(object):
    def __init__(self,
                 composer,
                 meter=[0, 0, 0, 0, 0, 0]):
        self.composer = composer
        self.meter = meter
        self.create_pattern()
        self.pan_positions = {"low": 0,
                              "high": 0,
                              "cont": 0,
                              "tuned": 0,
                              "mark": 0}
        self.ctl_values = {"low": {"val" : 150, "devi" : 30},
                           "high": {"val" : 800, "devi" : 30},
                           "cont": {"val" : 1000, "devi" : 500},
                           "tuned": {"val" : 500, "devi" : 100},
                           "mark": {"val" : 10000, "devi" : 1000}
                          }
        self.high_low_seq()
        self.generator = self.generate()
        self.generator.next()
        self.cont_accent_mult = 0.3
        self.cont_ctl_rand_deviation = 1000
        self.frame = {}

    def generate(self):
        while True:
            state = (yield)
            meter_pos = state['cycle_pos']
            #print meter_pos
            self.frame = {}
            for k,v in self.pattern.items():
                if v[meter_pos]:
                    ## to-do make more dynamic
                    vol = 0.5
                    ctl = None
                    if k == "cont":
                        vol = 0.5 + state["weight"] * self.cont_accent_mult
                        ctl = self.ctl_values[k]["val"] + (self.ctl.values[k][0]["devi"] * random.choice([1, -1]))
                        #print "cont: vol:", vol
                    self.frame[k] = {"vol": vol,
                                     "pan": self.pan_positions[k], 
                                     "ctl": ctl}
                    

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
            self.pattern = {"low" : map(lambda x: 1 if x == 2 else 0, self.meter),
                            "high":  map(lambda x: 1 if x == 1 else 0, self.meter),
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
            if p["low"][i]: res.append(-1)
            elif p["high"][i]: res.append(1)
            else: res.append(0)
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
        self.pattern = {"low" :[],
                 "high": [],
                 "cont": [],
                 "tuned": [],
                 "mark": []}




