import logging

comp_logger = logging.getLogger("composer")
note_logger = logging.getLogger("transcriber")

DIATONIC = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
HARMONIC = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
MELODIC =  [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]

HARMONIES = [[2, 4, 6], [2, 4, 7], [3, 5, 7], [2, 5, 7],
             [2, 4, 8], [2, 6, 8]]
DISHARMS = [1]

class Composer(object):
    def __init__(self):
        self.harm = {}
        self.voices = {}
        self.num_voices = 4
        self.scale = []

    def x():
        pass

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
        

if __name__ == "__main__":
    print DIATONIC, len(DIATONIC)
    print HARMONIC, len(HARMONIC)
    print MELODIC, len(MELODIC)

