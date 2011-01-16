from random import choice as sample
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


def hub():
    while True:
        data = (yield)
        print "sink: ", data

def voice(target, id):
    while True:
        state = (yield)
        print state, ", possible: ", state.get("possible", [])
        val = desc(state["composer"],sample(state["possible"]))
        state["composer"].harm.update({id:val})
        target.send(val)

def desc(c, val):
    return val - 1

def startup():
    s = hub()
    s.next() # get the coroutine to the yield
    c = Composer()
    v1 = voice(s,1)
    v1.next() # get the coroutine to the yield
    c.add_voice(1,v1)
    v2 = voice(s,2)
    v2.next() # get the coroutine to the yield
    v3 = voice(s,3)
    v3.next() # get the coroutine to the yield
    c.add_voice(2,v2)
    c.add_voice(3,v3)
    return c

def main(c):
    c.send_state({"possible":[2,6,9],
                  "composer":c})
    c.report()

if __name__ == "__main__":
    composer = startup()
    main(composer)
