import time

from random import choice
from roqba.static.movement_probabilities import ORNAMENTS, DRUM_FILLS


class RhythmAndMeterMixin(object):
    def choose_rhythm(self):
        '''chooses a new rhythm randomly from each voices groupings'''
        for v in self.voices.values():
            if not v.playing_a_melody:
                v.set_rhythm_grouping(
                    choice([grouping for grouping in v.note_length_groupings
                            if sum(grouping) == self.meter[0]]))

    def drum_fill_handler(self, v, state):
        '''handles the sending of drum-fill notes'''
        identifier = 'cont' if v == 'cont2' else 'cont2'
        possible_fills = [fill for fill in DRUM_FILLS
                          if state['speed'] / len(fill) > self.behaviour['min_speed'] * 0.5]
        chosen = choice(possible_fills)
        for fraction in chosen:
            if (state["speed"] * 1000 * fraction) < self.drummer.peak_speed:
                break
            self.gateway.pd_send_drum_note(identifier, self.drummer.frame[identifier]["vol"],
                                           self.drummer.frame[identifier]["pan"],
                                           self.drummer.frame[identifier]["ctl"])
            time.sleep(state["speed"] * fraction)

    def drum_mark_handler(self, v, state):
        '''handles the sending of a drum mark'''
        vol = self.drummer.frame[v]["vol"],
        pan = self.drummer.frame[v]["pan"],
        ctl = self.drummer.frame[v]["ctl"],
        tick = state["speed"] / 50
        vol_tmp = vol[0]
        for idx in xrange(6):
            vol_tmp *= 0.9
            ctl_new = ctl[0] - ((idx ** 2) * (random.random() * 600 + 200))
            self.gateway.pd_send_drum_note(v, vol_tmp, pan[0], ctl_new)
            time.sleep(4 * tick)
            self.gateway.pd_send_drum_note(v, 0, pan[0], ctl_new)
            time.sleep(1 * tick)
