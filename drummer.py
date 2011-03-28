
class Drummer(object):
    def __init__(self,
                 composer,
                 meter):
        self.composer = composer
        self.meter = meter
        self.create_pattern()

    def create_pattern(self, patt=None):
        '''creates a drum pattern from a given (bass-)pattern

        as a fallback this method will create a pattern from the underlying meter'''
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
            self.pattern = {"low" : map(lambda x: 1 if x == 2 else 0, self.meter ),
                            "high":  map(lambda x: 1 if x == 1 else 0, self.meter),
                            "cont": [1 for n in indeces],
                            "tuned": [0 for n in indeces],
                            "mark": [0 for n in indeces]}

    def push_value(self, val):
        for k, v in self.pattern.items():
            v.append(val)

    def empty_pattern(self):
        '''initializes a empty pattern.dict'''
        self.pattern = {"low" :[],
                 "high": [],
                 "cont": [],
                 "tuned": [],
                 "mark": []}




