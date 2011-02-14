import logging
from random import choice as sample

import metronome
from notator import Notator

comp_logger = logging.getLogger("composer")
note_logger = logging.getLogger("transcriber")

DIATONIC = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
HARMONIC = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
MELODIC = [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]

STRICT_HARMONIES = [set([2, 4, 6]), set([2, 4, 0]),
                    set([3, 5, 0]), set([2, 5, 0])]

# TODO: create dynamically
BASE_HARMONIES = {2:[set([6]), set([6, 2]), set([6, 0]), set([0, 2]), set([0, 4])],
                  3:[set([0]), set([6]), set([6, 2]), set([6, 0]), set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])],
                  4:[set([0, 2]), set([6]), set([6, 2]), set([6, 0]), set([0, 4]), set([0, 2]), set([0, 2, 4]), set([2, 4])]
                  }
HARMONIES = STRICT_HARMONIES + [set([2, 4, 1]), set([2, 6, 1])]
HARMONIC_INTERVALS = [0, 2, 3, 4, 5, 6]

DISHARMS = [1]
MINMAX = [0, 128]


class Composer(object):
    def __init__(self,
                 gateway=None,
                 num_voices=3,
                 scale=DIATONIC):
        self.harm = {}
        self.voices = {}
        self.num_voices = num_voices
        self.scale = scale
        self.generate_real_scale(*MINMAX)
        self.gateway = gateway
        self.hub = gateway.hub()
        # XxxxX consider making NoteGateway a Singleton
        self.hub.next()
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
        self.voices.update({id: voice})

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here
        
        any of the voices can change.
        """
        tmp_harm = []
        counter = 0
        for v in self.sort_voices_by_importance():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            v.generator.send(state)
            tmp_harm.append(v.note)
            if state["weight"] == metronome.HEAVY or state["weight"] == metronome.MEDIUM:
                patience = 0
                while not self.acceptable_harm_for_length(tmp_harm,\
                                                          counter) and\
                                                          patience < 100:
                    if len(tmp_harm) > counter:
                        tmp_harm.pop()
                    v.generator.send(state)
                    tmp_harm.append(v.note)
                    patience += 1
            counter += 1
        # here we have arrived at the next level
        # now we set the "real note" field according to the present scale
        self.add_duration_in_msec(state)
        self.apply_scale()
        # the stream analyzer can be used to check for chords, simultaneities
        self.stream_analyzer()
        # send the voices to the note-hub
        self.hub.send(self.voices)  # this sends the voices to the hub
        self.notator.note_to_file({"notes": tmp_harm,
                                   "weight": state["weight"],
                                   "cycle_pos": state["cycle_pos"]})
        return self.comment

    def apply_scale(self):
        for v in self.voices.values():
            if v.note_change:
                v.real_note = self.real_scale[v.note]
        
#        for v in self.voices.values():
#            if v.note_change:
#                v.real_note = self.scale_walker(self.scale,
#                                                v.real_note,
#                                                v.note_delta)

    def generate_real_scale(self, min, max):
        self.real_scale = []
        value = 0
        for n in xrange(min, max):
            value += 1
            index = n % len(self.scale)
            if self.scale[index]:
                self.real_scale.append(value)
        #print self.real_scale

    def acceptable_harm_for_length(self, harm, length):
        if length in [0, 1]:
            return True
        else:
            deltas = self.flatten_chord(self.get_deltas(harm))
            if length == 2:
                return deltas[0] in HARMONIC_INTERVALS
            else:
                return set(deltas) in STRICT_HARMONIES

    def calculate_possible_notes(self):
        self.harm

    def sort_voices_by_importance(self):
        dirs = filter(lambda x: x.dir, self.voices.values())
        no_dirs = list(set(self.voices.values()) - set(dirs))
        return dirs + no_dirs

    def choose_rhythm(self):
        for v in self.voices.values():
            v.set_rhythm_grouping(sample(v.note_length_groupings))

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

    def stream_analyzer(self):
        """analyses the stream of notes.
        
        searches for target-harmonies and sets a flag"""
        # check if all notes are new
        self.comment = 'normal'
        note_changes = [v.note_change for v in self.voices.values()]
        all_notes_change = reduce(lambda x, y :
                                 x and y,
                                 note_changes)
        if all_notes_change:
            harmony = map(lambda x: x.note, self.voices.values())
            #print "all_notes_change: harmony {0}".format(harmony)
            if self.is_base_harmony(harmony):
                self.comment = "caesura"
                print "all notes change to a base harmony"

    def acceptable_harmony(self, chord):
        flat = self.flatten_chord(chord)
        return set(flat) in STRICT_HARMONIES

    def is_base_harmony(self, chord):
        flat = self.flatten_chord(chord)
        #print set(flat)
        return set(flat) in BASE_HARMONIES[self.num_voices]

    @staticmethod
    def flatten_chord(chord):
        flat = map(lambda x: x % 7, chord) 
        return flat

    @staticmethod
    def get_deltas(chord):
        chord.sort()
        base = chord[0]
        return map(lambda x: x - base, chord)[1:]

    @staticmethod
    def scale_walker(scale, present_note, delta):
        """walks the <scale> <delta> steps starting at <present_note>"""
        if delta == 0:
            return present_note
        dir = delta / abs(delta)
        steps = 0
        index = 1
        octave = present_note // len(scale)
        mod = present_note % len(scale)
        while steps < abs(delta):
            check_index = (mod + (dir * index)) % len(scale)
            if scale[check_index]:
                steps += 1
                if steps == abs(delta):
                    break
                index += 1
            else:
                index += 1
            #print check_index, scale[check_index], index, steps
        return (index * dir) + mod + (octave * len(scale))

    def add_duration_in_msec(self, state):
        for v in self.voices.values():
            v.duration_in_msec = int(v.note_duration_steps * state["speed"] * 1000)

if __name__ == "__main__":
    print DIATONIC, len(DIATONIC)
    print HARMONIC, len(HARMONIC)
    print MELODIC, len(MELODIC)
    print HARMONIES
    print STRICT_HARMONIES

    print Composer().get_deltas([12, 8, 10, 15])
    print "get deltas([2, 5]):", Composer.get_deltas([2, 5])
    print Composer.acceptable_harmony(Composer.get_deltas([12, 8, 10, 15]))
    print Composer().acceptable_harmony([2, 4, 6])
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
