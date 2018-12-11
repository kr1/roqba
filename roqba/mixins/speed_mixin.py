import math
from random import randint, random


class SpeedMixin(object):
    def set_speed_in_bpm(self, bpm):
        return self.new_speed(bpm=bpm)

    def new_speed(self, val=None, bpm=None):
        if val:
            self.speed = val
        elif bpm:
            self.speed = 30.0 / bpm
        elif self.behaviour['automate_speed_change']:
            if self.speed_change == 'transition':
                self.speed += randint(-1000, 1000) / 66666.
            else:  # if self.speed_change == 'leap':
                if self.behaviour['speed_target'] != 0.5:
                    target = self.behaviour['speed_target']
                    if target < 0.3:
                        target = target ** 2
                    speed_tmp = random() ** math.log(target, 0.5)
                    self.speed = (self.behaviour["min_speed"] +
                                  ((self.behaviour["max_speed"] - self.behaviour["min_speed"]) *
                                  speed_tmp))
                else:
                    self.speed = self.behaviour["min_speed"] + (random() *
                                                                (self.behaviour["max_speed"] -
                                                                 self.behaviour["min_speed"]))
            #print "new speed values: {0}\n resetting metronome.".format(
            #                                                self.speed)
        self.gateway.pd.send(['sys', 'speed', str(self.speed * 1000)])
        return self.speed
