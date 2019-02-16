'''this module defines a custom dict

BehaviourDict is a subclass of dict and modifies mainly the
__setitem__ method by calling a setter method for
the given key if the setter method has been registered before'''

import pprint
import time
import logging

from roqba.utilities.logger_adapter import StyleLoggerAdapter


class BehaviourDict(dict):
    '''defines a dictionary-class with custom setter methods

    upon every __setitem__ call it checks if it has registered setter
    methods and calls them with the given value'''
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.real_setters = {}
        if 'name' in list(kwargs.keys()):
            self.name = kwargs['name']
        else:
            self.name = None
        self.saved_behaviours = self.read_or_create_saved_behaviours()
        behaviour_logger = logging.getLogger('behaviour')
        self.behaviour_logger = StyleLoggerAdapter(behaviour_logger, None)
        self._update(*args, **kwargs)

    def read_or_create_saved_behaviours(self, name='.saved_behaviours'):
        """reads saved behaviours if there are, otherwise creates them"""
        try:
            with open(name, 'r+') as behaviour_file:
                try:
                    saved_behaviours = eval(behaviour_file.read())
                except SyntaxError:
                    saved_behaviours = {}
        except IOError:
            open(name, 'w').close()
            saved_behaviours = {}
        return saved_behaviours

    def write_saved_behaviours(self, name='.saved_behaviours'):
        """writes the saved behaviours to file"""
        with open(name, 'w+') as behaviour_file:
            behaviour_file.write(pprint.pformat(self.saved_behaviours))

    def save_current_behaviour(self, name=None, write_to_file=True):
        """adds current behaviour to the saved behaviours dict"""
        time_key = time.strftime('%Y-%m-%d--%H:%M:%S', time.localtime())
        self.saved_behaviours[name or time_key] = self
        if write_to_file:
            self.write_saved_behaviours()

    def __setitem__(self, item, value):
        '''sets the specified key to the given value

        and calls a setter method registered for the given key'''
        dict.__setitem__(self, item, value)
        self.behaviour_logger.info(
            "behaviour dict-{0}: setting '{1}' to '{2}'".format(self.name, item, value))
        if item in list(self.real_setters.keys()):
            instructions = self.real_setters[item]
            if type(instructions).__name__ == 'instancemethod':
                self.real_setters[item](value)
            elif type(instructions).__name__ == 'list':
                callable = self.real_setters[item][0]  # first argument is the callable
                if len(instructions) == 2:
                    callable(instructions[1], value)
                elif len(instructions) == 3:
                    callable(instructions[1], instructions[2], value)

    def _update(self, *args, **kwargs):
        '''assures that __setitem__  is called from __init__'''
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def voice_get(self, vid, key):
        '''returns the value for the specified key.

        if the value is present for the voice, this value is returned
        otherwise the default value for this key is returned'''
        if vid in list(self["per_voice"].keys()):
            if key in self["per_voice"][vid]:
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
    print("from test_setter, val:", val)


if __name__ == "__main__":
    kd = BehaviourDict(list({
        "erre": {'val': [34, 56], 'setter': test_setter}, 17: 45}.items()))
    print(kd)
    print(kd.real_setters)
    kd[5] = "wer"
    kd.__setitem__('tee', (45, 56))
    kd['erre'] = [45, 46]
    kd['single'] = 666
    print(kd)
    print(kd.real_setters)
