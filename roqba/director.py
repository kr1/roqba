import time
import logging
import random
import math
import threading

import metronome
import composer

logger = logging.getLogger('director')
logger.setLevel(logging.INFO)


class Director(object):
    def __init__(self, composer, state, behaviour, settings):
        self.composer = composer
        self.behaviour = behaviour
        self.playing = None
        self.state = state
        self.settings = settings
        self.gateway = composer.gateway
        self.speed_target = behaviour["speed_target"]
        self.speed = state["speed"]

        # keep this between 0 and MAX_SHUFFLE
        self.shuffle_delay = behaviour["shuffle_delay"]
        self.meter = composer.applied_meter
        self.metronome = metronome.Metronome(self.meter)
        self.automate_binaural_diffs = behaviour["automate_binaural_diffs"]
        self.speed_change = behaviour["speed_change"]
        self.MIN_SPEED = behaviour["min_speed"]
        self.MAX_SPEED = behaviour["max_speed"]
        self.MAX_SHUFFLE = behaviour["max_shuffle"]

    def set_meter(self, meter):
        self.composer.set_meter(meter)
        self.metronome.set_meter(composer.METERS[meter]["applied"])

    def _play(self, duration=None):
        """this is the core of the program giving the impulse for all actions.

        """
        self.start_time = time.time()
        self.playing = True
        logger.info("<<<<<<<<<<<<<<<<<<<<<<   start playing  >>>>>>>>>>>>>>>>\
>>>>>>>>>>>>>>")
        pos = 0
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
                self.shuffle_delay = random.random() * self.MAX_SHUFFLE
                logger.info("shuffle delay set to: {0}".format(
                                                  self.shuffle_delay))
                self.new_speed()
                self.state["speed"] = self.speed
                self.metronome.reset()
                self.composer.gateway.stop_all_notes()
                self.composer.set_scale(random.choice(
                                            composer.SCALES_BY_FREQUENCY))
                new_meter = random.choice(composer.METERS.keys())
                self.gateway.pd.send(["sys", "meter",
                                       str(new_meter).replace(",", " ").
                                       replace(" ", "_")])
                if self.automate_binaural_diffs:
                    self.composer.set_binaural_diffs()
                if self.behaviour["automate_transpose"]:
                    sample = self.behaviour["transposings"]
                    self.gateway.transpose = random.choice(sample)
                self.set_meter(new_meter)
                time.sleep(self.speed)
            shuffle_delta = (self.speed * self.shuffle_delay
                              if weight == metronome.LIGHT
                                else 0)
            time.sleep(self.speed + shuffle_delta)

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

    def new_speed(self):
        if self.speed_change == 'transition':
            self.speed += random.randint(-1000, 1000) / 66666.
        else:  # if self.speed_change == 'leap':
            if self.speed_target != 0.5:
                target = self.speed_target
                if  target < 0.3:
                    target = target ** 2
                speed_tmp = random.random() ** math.log(target, 0.5)
                self.speed = (self.MIN_SPEED +
                              ((self.MAX_SPEED - self.MIN_SPEED) *
                              speed_tmp))
            else:
                self.speed = self.MIN_SPEED + (random.random() *
                                    (self.MAX_SPEED - self.MIN_SPEED))
        #print "new speed values: {0}\n resetting metronome.".format(
        #                                                self.speed)
        return self.speed
