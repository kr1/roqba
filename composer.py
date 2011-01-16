

class Composer(object):
    def __init__(self):
        self.harm = {}
        self.voices = {}
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
        print "sending state: {0}".format(state)
        for v in self.voices.values():
            v.send(state)
    
    def calculate_possible_notes(self):
        self.harm

