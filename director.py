import time
import logging
import itertools
import threading

import metronome
import OSC_hub

logger = logging.getLogger('director')
logger.setLevel(logging.INFO)


class Director(object):
    def __init__(self, composer, speed, state, meter=[2, 0, 1, 0]):
        self.composer = composer
        self.playing = None
        self.state = state
        self.gateway = composer.gateway
        self.speed = speed
        self.metronome = metronome.Metronome(meter)

    def _play(self, duration=None):
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

            time.sleep(self.speed)
            cycle_pos, weight = self.metronome.beat()
            self.state.update({'weight': weight,
                               'cycle_pos': cycle_pos})
            if weight == metronome.HEAVY:
                self.composer.choose_rhythm()
            self.composer.generate(self.state)

    def pause(self):
        if self.playing:
            self.playing = False
            self.gateway.pause()
            #OSC_hub.client.stop_notes()
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
        #OSC_hub.client.stop_notes()

    def make_length(self):
        delta = int(time.time() - self.start_time)
        return "{0}:{1}".format(int(delta / 60),
                                str(delta % 60).zfill(2))
