import logging

comp_logger = logging.getLogger("composer")
note_logger = logging.getLogger("transcriber")

DIATONIC = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
HARMONIC = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
MELODIC =  [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]), set([3, 5, 0]), set([2, 5, 0])]
HARMONIES =        STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]

DISHARMS = [1]

MOVEMENT_PROBS = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 
                  5, 5, 6, 6, 7, 7, 
                  8, 8, 8, 8, 8, 8, 9, 9, 10 ,11, 12, 13]

class Composer(object):
    def __init__(self, num_voices = 4):
        self.harm = {}
        self.voices = {}
        self.num_voices = num_voices
        self.scale = []

    def __repr__(self):
        return "<Composer-Instance for {0}>".format(self.harm)

    def report(self):
        print "harmonies: {0}".format(self.harm)
        #print "voices: {0}".format(self.voices)

    def add_voice(self, id, voice):
        self.voices.update({id:voice})

    def send_state(self, state):
        #print "sending state: {0}".format(state)
        note_logger.info("sending state: {0}".format(state))
        for v in self.voices.values():
            v.send(state)
    
    def calculate_possible_notes(self):
        self.harm

    def random_harmonic(self):
        res = []
        while not self.acceptable_harmony(res):
           for v in self.voices:
               res.append(v.random_note())
        return res
    
    @staticmethod
    def acceptable_harmony(chord):
        flat = map(lambda x: x % 7, chord)
        return set(flat) in STRICT_HARMONIES
    
    @staticmethod
    def get_deltas(chord):
        chord.sort()
        base = chord[0]
        return map(lambda x: x - base, chord)[1:]

if __name__ == "__main__":
    print DIATONIC, len(DIATONIC)
    print HARMONIC, len(HARMONIC)
    print MELODIC, len(MELODIC)
    print HARMONIES
    print STRICT_HARMONIES

    print Composer().get_deltas([12,8,10,15])
    print Composer.acceptable_harmony(Composer.get_deltas([12,8,10,15]))
    print Composer().acceptable_harmony([2,4,6])
