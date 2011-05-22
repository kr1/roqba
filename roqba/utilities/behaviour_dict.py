'''this module defines a behaviour dict class

BehaviourDict is a subclass of dict and modifies mainly the
__setitem__ method by calling a setter method for
the given key if the setter method has been registered before'''


class BehaviourDict(dict):
    '''defines a dictionary-class with custum setter methods

    upon every call it checks if it has registered setter methods to be
    called and calls them with the given value'''
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.real_setters = {}
        self._update(*args, **kwargs)

    def __setitem__(self, item, value):
        '''sets the specified key to the given value

        and calls a setter method registered for the given key'''
        dict.__setitem__(self, item, value)
        if item in self.real_setters.keys():
            self.real_setters[item](value)

    def _update(self, *args, **kwargs):
        '''assures that __setitem__  is called from __init__'''
        for k, v in dict(*args, **kwargs).iteritems():
            if type(v) == dict:
                self[k] = v['val']
                self.real_setters[k] = v['setter']
            else:
                self[k] = v


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