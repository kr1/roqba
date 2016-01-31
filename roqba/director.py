import time
import logging
import math
import threading
from random import random, choice, randint
from Queue import deque

import metronome
from roqba.composers import baroq, amadinda
from roqba.utilities import random_between
from roqba.utilities.gui_connect import GuiConnect
from roqba.incoming_messages_mixin import IncomingMessagesMixin
from roqba.wavetable_mixin import WavetableMixin


logger = logging.getLogger('director')
logger.setLevel(logging.INFO)


class Director(IncomingMessagesMixin, WavetableMixin):
    def __init__(self, gateway, behaviour, settings):
        composer = globals().get(settings.get('composer', 'baroq'))
        if not composer:
            raise RuntimeError("Composer is not configured correctly")
        self.composer = composer.Composer(gateway, settings, behaviour)
        self.state = {"comp": self.composer, "speed": behaviour["speed"]}
        self.behaviour = behaviour
        self.playing = None
        self.stopped = False
        self.force_caesura = False
        self.settings = settings
        self.gateway = self.composer.gateway
        self.speed_target = behaviour["speed_target"]
        self.speed = self.state["speed"]
        self.has_gui = settings['gui']
        self.gui_sender = self.has_gui and GuiConnect() or None
        self.allowed_incoming_messages = (
            self.has_gui and
            self.behaviour.keys() + ['play', 'sys', 'scale',
                                     'force_caesura',
                                     'trigger_wavetable']
            or None)
        if self.has_gui:
            self.incoming = deque()
            self.gui_sender.update_gui(self)
            #start the reader thread
            thre = threading.Thread(target=self.gui_sender.read_incoming_messages,
                                    args=(self.incoming,))
            thre.daemon = True
            thre.start()

        # keep this between 0 and MAX_SHUFFLE
        self.shuffle_delay = behaviour["shuffle_delay"]
        self.meter = self.composer.applied_meter
        self.metronome = metronome.Metronome(self.meter)
        self.automate_binaural_diffs = behaviour["automate_binaural_diffs"]
        self.automate_meters = behaviour["automate_meters"]
        self.speed_change = behaviour["speed_change"]
        self.MIN_SPEED = behaviour["min_speed"]
        self.MAX_SPEED = behaviour["max_speed"]
        self.MAX_SHUFFLE = behaviour["max_shuffle"]
        self.musical_logger = logging.getLogger('musical')
        self.behaviour_logger = logging.getLogger('behaviour')
        self.gui_logger = logging.getLogger('gui')
        self.add_setters()

    def add_setters(self):
        self.behaviour.real_setters["meter"] = self.set_meter
        self.behaviour.real_setters["transpose"] = self.gateway.set_transpose
        self.behaviour.real_setters["speed"] = self.new_speed
        self.behaviour.real_setters["binaural_diff"] = self.composer.set_binaural_diffs
        self.behaviour.real_setters["slide_duration_msecs"] = self.gateway.set_slide_msecs_for_all_voices
        for vid in self.behaviour['per_voice'].keys():
            self.behaviour['per_voice'][vid].real_setters["pan_pos"] = \
                [self.composer.voices[vid].set_pan_pos, self.gateway]
            self.behaviour['per_voice'][vid].real_setters["slide_duration_msecs"] = \
                [self.gateway.set_slide_msecs, vid]

    def set_meter(self, meter):
        self.composer.set_meter(meter)
        self.meter = self.composer.applied_meter
        self.metronome.set_meter(self.composer.offered_meters[meter]["applied"])

    def _play(self, duration=None):
        """this is the core of the program giving the impulse for all actions.

        """
        self.start_time = time.time()
        self.playing = True
        self.musical_logger.info("<<<<<<   start playing   >>>>>>")
        pos = 0

        while not self.stopped:
            if not self.playing:
                self.check_incoming_messages()
                time.sleep(0.2)
                continue
            if duration:
                pos += self.speed
                if pos > duration:
                    self.playing = False
                    self.musical_logger.info("<<<<<   stop playing  >>>>>")

            cycle_pos, weight = self.metronome.beat()
            self.state.update({'weight': weight,
                               'cycle_pos': cycle_pos})
            # on heavy beats a new rhythm-grouping is loaded
            if weight == metronome.HEAVY:
                self.composer.choose_rhythm()
            comment = self.composer.generate(self.state)
            if ((comment == 'caesura' and
               random() < self.behaviour["caesura_prob"]) or
               self.force_caesura):
                if self.force_caesura:
                    self.force_caesura = False
                # take 5 + 1 times out....
                time.sleep(self.speed * 4)
                self.shuffle_delay = random() * self.MAX_SHUFFLE
                logger.info("shuffle delay set to: {0}".format(
                    self.shuffle_delay))
                self.new_speed()
                self.state["speed"] = self.speed
                self.metronome.reset()
                self.composer.gateway.stop_all_notes()
                if self.behaviour['automate_scale']:
                    self.composer.set_scale(choice(
                                            self.composer.offered_scales))
                if self.behaviour['automate_meters']:
                    self.new_random_meter()
                voices = self.composer.voices.values()
                if self.behaviour["automate_pan"]:
                    for v in voices:
                        if self.behaviour.voice_get(v.id, "automate_pan"):
                            max_pos = self.behaviour.voice_get(v.id,
                                                               "automate_pan")
                            v.pan_pos = (random() * max_pos) - max_pos / 2.0
                            self.gateway.send_voice_pan(v, v.pan_pos)
                if self.behaviour["automate_binaural_diffs"]:
                    if self.behaviour["pan_controls_binaural_diff"]:
                        for v in voices:
                            if not self.behaviour.voice_get(v.id, "automate_binaural_diffs"):
                                continue
                            diff = (abs(v.pan_pos) *
                                    self.behaviour.voice_get(v.id, "max_binaural_diff"))
                            self.composer.set_binaural_diffs(diff, v)
                    else:
                        self.composer.set_binaural_diffs()
                if self.behaviour["automate_note_duration_prop"]:
                    min_, max_ = self.behaviour["automate_note_duration_min_max"]
                    if self.behaviour["common_note_duration"]:
                        prop = random_between(min_, max_, 0.3)
                        #print "note duration proportion: ", prop
                        [setattr(v, 'note_duration_prop', prop) for v
                            in self.composer.voices.values()]
                    else:
                        for v in self.composer.voices.values():
                            min_, max_ = self.behaviour.voice_get(v.id,
                                                                  "automate_note_duration_min_max")
                            prop = random_between(min_, max_, 0.3)
                            v.note_duration_prop = prop
                if self.behaviour["automate_transpose"]:
                    sample = self.behaviour["transposings"]
                    new_transpose = choice(sample)
                    self.gateway.transpose = new_transpose
                    self.behaviour["transpose"] = new_transpose
                    self.gui_sender.send({'transpose': new_transpose})
                time.sleep(self.speed)
                if self.behaviour["automate_wavetables"]:
                    self.set_wavetables(voices=voices)
                if self.has_gui:
                    self.gui_sender.handle_caesura(self)
                self.musical_logger.info('caesura :: meter: {0}, speed: {1}, scale: {2}'.format(
                    self.composer.meter, self.speed, self.composer.scale))
            self.check_incoming_messages()
            shuffle_delta = (self.speed * self.shuffle_delay
                             if weight == metronome.LIGHT
                             else 0)
            time.sleep(self.speed + shuffle_delta)

    def check_incoming_messages(self):
        '''checks if there are incoming messages in the queue'''
        if self.has_gui:
            if self.playing:
                self.gui_sender.send_cycle_pos(self)
            while len(self.incoming) > 0:
                msg = self.incoming.pop()
                self.handle_incoming_message(msg)

    def pause(self):
        if self.playing:
            self.playing = False
            self.gateway.pause()
        return True

    def unpause(self):
        if not self.playing:
            self.playing = True
            self.gateway.unpause()
            #threading.Thread(target=self._play, args=()).start()
        return True

    def stop(self):
        if self.playing:
            logger.info("<<<<   stop playing = length: '{0}'   >>>>".format(
                self.make_length()))
        self.playing = False
        self.stopped = True
        self.gui_sender.receive_exit_requested = True
        self.gateway.stop()
        self.metronome.reset()
        self.composer.notator.reset()
        time.sleep(1)

    def make_length(self):
        delta = int(time.time() - self.start_time)
        return "{0}:{1}".format(int(delta / 60),
                                str(delta % 60).zfill(2))

    def new_random_meter(self):
        new_meter = choice(self.composer.selected_meters)
        self.set_meter(new_meter)
        self.gateway.pd.send(["sys", "meter",
                             str(new_meter).replace(",", " ").
                             replace(" ", "_")])

    def new_speed(self, val=None):
        if val:
            self.speed = val
            return self.speed
        if self.behaviour['automate_speed_change']:
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
