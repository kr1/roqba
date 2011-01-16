import time
import logging

from metronome import metro

logger = logging.getLogger('director')
logger.setLevel(logging.INFO)

class Director(object):
    def __init__(self, composer, speed, state):
        self.composer = composer
        self.playing = None
        self.state = state
        self.speed = speed
        self.metro = metro()

    def play(self, duration = None):
        self.start_time = time.time()
        self.playing = True
        logger.info("start playing")
        pos = 0
        self.playing = True
        while self.playing:
            if duration:
                pos += self.speed
                if pos > duration:
                    self.playing = False
                    logger.info("stop playing")
            time.sleep(self.speed)
            self.composer.send_state(self.state)
            self.metro.next()


    def stop(self):
        logger.info("stop playing ========== length: '{0}' -------------<<<<<<<<<<<<<<<<<".format(self.make_length()))
        self.playing = False

    def make_length(self):
        delta = int(time.time() - self.start_time)
        return "{0}:{1}".format(int(delta/60), 
                                str(delta % 60).zfill(2))
