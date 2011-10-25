'''this module defines a custom dict

BehaviourDict is a subclass of dict and modifies mainly the
__setitem__ method by calling a setter method for
the given key if the setter method has been registered before'''


class BehaviourDict(dict):
    '''defines a dictionary-class with custom setter methods

    upon every __setitem__ call it checks if it has registered setter 
    methods and calls them with the given value'''
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.real_setters = {}
        self._update(*args, **kwargs)

    def __setitem__(self, item, value):
        '''sets the specified key to the given value

        and calls a setter method registered for the given key'''
        dict.__setitem__(self, item, value)
        #print "behaviour dict-{0}: setting {1} to {2}".format(self, item, value)
        if item in self.real_setters.keys():
            instructions = self.real_setters[item]
            #print "with instructions", instructions, "of type: ", type(instructions)
            if type(instructions).__name__ == 'instancemethod':
                self.real_setters[item](value)
            elif type(instructions).__name__ == 'list': 
                callable = self.real_setters[item][0] # first argument is the callable
                #print "callable: ", callable
                if len(instructions) == 2:
                    #print "calling {0} with {1} and {2}".format(callable, instructions[1], value)
                    callable(instructions[1], value)
                elif len(instructions) == 3:
                    #print "calling {0} with {1} and {2} and {3}".format(callable, instructions[1], instructions[2], value)
                    callable(instructions[1], instructions[2], value)

    def _update(self, *args, **kwargs):
        '''assures that __setitem__  is called from __init__'''
        for k, v in dict(*args, **kwargs).iteritems():
# temporarily commented rudiment from earlier setting handling
#            if type(v) == dict:
#                self[k] = v['val']
#                self.real_setters[k] = v['setter']
#            else:
            self[k] = v

    def voice_get(self, vid, key):
        '''returns the value for the specified key.

        if the value is present for the voice, this value is returned
        otherwise the defaukt value for this key is returned'''
        if vid in self["per_voice"].keys():
                if key in self["per_voice"][vid].keys():
                    return self["per_voice"][vid][key]
                else:
                    try:
                        return self[key] 
                    except KeyError:
                        msg = "inexistent key: "
                        msg += "{0} for both voice: {1} and default"
                        raise RuntimeError(msg.format(key, vid))
        else:
            msg = "voice_get() called for unregistered voice: {0}"
            raise RuntimeError(msg.format(vid))

def test_setter(val):
    print "from test_setter, val:", val

if __name__ == "__main__":
    kd = BehaviourDict({"erre": {'val': [34, 56], 'setter': test_setter},
                        17: 45
                       }.items())
    print kd
    print kd.real_setters
    kd[5] = "wer"
    kd.__setitem__('tee', (45, 56))
    kd['erre'] = [45, 46]
    kd['single'] = 666
    print kd
    print kd.real_setters
