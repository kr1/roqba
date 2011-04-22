
class Drummer(object):
    def __init__(self,
                 composer,
                 meter=[0, 0, 0, 0, 0, 0]):
        self.composer = composer
        self.meter = meter
        self.create_pattern()
        self.high_low_seq()
        self.generator = self.generate()
        self.generator.next()
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
                    self.frame[k] = {"vol": 1,
                                     "pan": 0, 
                                     "ctl": None}
                    

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




