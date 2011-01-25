import logging
from random import choice as sample

import metronome
from notator import Notator
from note_length_groupings import DEFAULT_NOTE_LENGTH_GROUPINGS as GROUPINGS

comp_logger = logging.getLogger("composer")
note_logger = logging.getLogger("transcriber")

DIATONIC = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
HARMONIC = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
MELODIC =  [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]), set([3, 5, 0]), set([2, 5, 0])]
HARMONIES =        STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]
HARMONIC_INTERVALS = [0, 2, 3, 4, 5, 6]

DISHARMS = [1]

DEFAULT_MOVEMENT_PROBS = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1 ,1 ,1 ,1 ,1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 
                  7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 10 ,11, 12, 13]


class Composer(object):
    def __init__(self, hub = None, num_voices = 3):
        self.harm = {}
        self.voices = {}
        self.num_voices = num_voices
        self.scale = []
        self.hub = hub
        self.highest = 0
        self.lowest = 1000000
        self.notator = Notator(self.num_voices)

    def __repr__(self):
        return "<Composer-Inst with {0}>".format(self.harm)

    def report(self):
        print "harmonies: {0}".format(self.harm)
        print "voices: {0}\nnotes:{1}".format(self.voices,
                                                map(lambda x: x.note, self.voices.values()))

    def add_voice(self, id, voice):
        self.voices.update({id:voice})

    def generate(self, state):
        """main generating function, the next harmony is produced here"""
        #print "sending state: {0}".format(state)

        #note_logger.info("sending state: {0}".format(state))
        tmp_harm = []
        counter = 0
        for v in self.sort_voices_by_importance():
            if len(self.voices) < self.num_voices: raise RuntimeError
            v.generator.send(state)
            tmp_harm.append(v.note)
            if state["weight"] == metronome.HEAVY: 
                while not self.acceptable_harm_for_length(tmp_harm, counter):
                    if len(tmp_harm) > counter: tmp_harm.pop()
                    v.generator.send(state)
                    tmp_harm.append(v.note)
            counter += 1
        print "tmp_harm: {0}".format(tmp_harm)
        self.hub.send(self.voices)
        self.notator.note_to_file(tmp_harm)
        #target.send({"voice":str(self.id),"message":str(val)})

    def acceptable_harm_for_length(self, harm, length):
        if length in [0,1]:
            return True
        elif length == 2:
            return self.flatten_chord(self.get_deltas(harm))[0] in HARMONIC_INTERVALS 
        else: 
            return acceptable_harmony(chord)
        #return sample([True, False])

    def calculate_possible_notes(self):
        self.harm

    def sort_voices_by_importance(self):
        dirs = filter(lambda x: x.dir, self.voices.values())
        no_dirs = list(set(self.voices.values()) - set(dirs))
        return dirs + no_dirs

    def choose_rhythm(self):
        for v in self.voices.values():
            v.set_rhythm_grouping(sample(GROUPINGS))
            
    def random_harmonic(self):
        res = []
        while not self.acceptable_harmony(res):
           for v in self.voices:
               res.append(v.random_note())
        return res

    def highest_note_of_piece(self):
        self.highest

    def lowest_note_of_piece(self):
        self.lowest
    
    @staticmethod
    def acceptable_harmony(chord):
        flat = flatten_chord(chord)
        return set(flat) in STRICT_HARMONIES
    
    @staticmethod
    def flatten_chord(chord):
        return map(lambda x: x % 7, chord)

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
    print "get deltas([2,5]):", Composer.get_deltas([2,5])
    print Composer.acceptable_harmony(Composer.get_deltas([12,8,10,15]))
    print Composer().acceptable_harmony([2,4,6])
    from voice import Voice
    c = Composer()
    v1 = Voice(1, None, c)
    v1.dir = 1
    c.add_voice(v1.id, v1)
    v2 = Voice(2, None, c)
    c.add_voice(v2.id, v2)
    v3 = Voice(3, None, c)
    v3.dir = 0
    c.add_voice(v3.id, v3)


    print c.sort_voices_by_importance()
