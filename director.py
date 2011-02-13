import time
import logging
import random
import itertools
import threading

import metronome

logger = logging.getLogger('director')
logger.setLevel(logging.INFO)


class Director(object):
    def __init__(self, composer, state, meter=[2, 0, 1, 0]):
        self.composer = composer
        self.playing = None
        self.state = state
        self.gateway = composer.gateway
        self.speed = state["speed"]
        self.metronome = metronome.Metronome(meter)
        self.speed_change = 'leap'
        self.MIN_SPEED = 0.1
        self.MAX_SPEED = 0.7

    def _play(self, duration=None):
        """this is the core of the program giving the impulse for all actions.

        """
        self.start_time = time.time()
        self.playing = True
        logger.info("<<<<<<<<<<<<<<<<<<<<<<   start playing  >>>>>>>>>>>>>>>>\
>>>>>>>>>>>>>>")
        pos = 0
        self.playing = True
        while self.playing:
            if duration:
                pos += self.speed
                if pos > duration:
                    self.playing = False
                    logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<   stop playing  \
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            cycle_pos, weight = self.metronome.beat()
            self.state.update({'weight': weight,
                               'cycle_pos': cycle_pos})
            # on heavy beats a new rhythm-grouping is loaded
            if weight == metronome.HEAVY:
                self.composer.choose_rhythm()
            comment = self.composer.generate(self.state)
            if comment == 'caesura':
                # take 5 + 1 times out....
                time.sleep(self.speed * 4)
                if self.speed_change == 'transition':
                    self.speed += random.randint(-1000, 1000) / 66666.
                else:  #if self.speed_change == 'leap':
                    self.speed = self.MIN_SPEED + (random.random() *
                                            (self.MAX_SPEED - self.MIN_SPEED))
                print "new speed values: {0}\n resetting metronome.".format(
                                                                self.speed)
                self.state["speed"] = self.speed
                self.metronome.reset()
                self.composer.gateway.stop_all_notes()
                time.sleep(self.speed)
            time.sleep(self.speed)

    def pause(self):
        if self.playing:
            self.playing = False
            self.gateway.pause()
        return True

    def unpause(self):
        if not self.playing:
            self.playing = True
            self.gateway.unpause()
            threading.Thread(target=self._play, args=()).start()
        return True

    def stop(self):
        if self.playing:
            logger.info("<<<<<<<<<<<<<<   stop playing = length: '{0}' >>>>>>>\
>>>>>>>>>>>>>>>>>>".format(self.make_length()))
        self.playing = False
        self.gateway.stop()
        self.metronome.reset()
        self.composer.notator.reset()
        time.sleep(1)

    def make_length(self):
        delta = int(time.time() - self.start_time)
        return "{0}:{1}".format(int(delta / 60),
                                str(delta % 60).zfill(2))
