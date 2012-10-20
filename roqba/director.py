import time
import logging
import math
import threading
from random import random, choice, randint
from Queue import deque

import metronome
import composer
from roqba.utilities import random_between
from roqba.utilities import pd_wavetables as wavetables
from roqba.utilities.gui_connect import GuiConnect
from roqba.utilities.behaviour_dict import BehaviourDict


logger = logging.getLogger('director')
logger.setLevel(logging.INFO)


class Director(object):
    def __init__(self, composer, state, behaviour, settings):
        self.composer = composer
        self.behaviour = behaviour
        self.playing = None
        self.stopped = False
        self.force_caesura = False
        self.state = state
        self.settings = settings
        self.gateway = composer.gateway
        self.speed_target = behaviour["speed_target"]
        self.speed = state["speed"]
        self.has_gui = settings['gui']
        self.gui_sender = self.has_gui and GuiConnect() or None
        self.allowed_incoming_messages = (self.has_gui and
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
        self.meter = composer.applied_meter
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

    def set_meter(self, meter):
        self.composer.set_meter(meter)
        self.meter = self.composer.applied_meter
        self.metronome.set_meter(composer.METERS[meter]["applied"])

    def _play(self, duration=None):
        """this is the core of the program giving the impulse for all actions.

        """
        self.start_time = time.time()
        self.playing = True
        self.musical_logger.info("<<<<<   start playing   >>>>>>")
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
                self.composer.set_scale(choice(
                                            composer.SCALES_BY_FREQUENCY))
                if self.automate_meters:
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
                    self.gateway.transpose = choice(sample)
                time.sleep(self.speed)
                if self.behaviour["automate_wavetables"]:
                    self.set_wavetables(voices=voices)
                if self.has_gui:
                    self.gui_sender.handle_caesura(self)
                self.musical_logger.info('caesura :: meter: {0}, speed: {1}, scale: {2}'.format(self.composer.meter,
                                                               self.speed,
                                                               self.composer.scale))
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

    def set_wavetables(self, vid=None, voices=None, manual=False, wavetable=None):
        '''sets new wavetables for those voices that have the

        wavetable automation flag turned on (or the manual flag set).
        when a voice-id is specified only this voice is considered'''
        incoming_wavetable = wavetable
        voices = voices if voices else [self.composer.voices[vid]]
        if self.behaviour["common_wavetables"] and not vid:
            if not wavetable:
                wt_item = choice(self.behaviour["wavetable_specs"])
                wavetable_generation_type = wt_item[0]
                fun = getattr(wavetables, wt_item[0] + '_wavetable')
                num_partials = (self.behaviour["automate_num_partials"] and
                                randint(1, self.behaviour["max_num_partials"])  or
                                self.behaviour["default_num_partial"])
                partial_pool = choice(wt_item[1])
                wavetable = fun(num_partials, partial_pool)
        else:
            wavetable = None
        for v in voices:
            wt = wavetable  # this is used to maintain the original state for every voice
            if self.behaviour.voice_get(v.id, "automate_wavetables") or manual:
                if not wavetable:
                    wt_sample = self.behaviour.voice_get(v.id, "wavetable_specs")
                    wt_item = choice(wt_sample)
                    #print "set wavetables, voice: ", v.id, wt_item
                    wavetable_generation_type = wt_item[0]
                    fun = getattr(wavetables, v.wavetable_generation_type + '_wavetable')
                    max_partials = self.behaviour.voice_get(v.id, "max_num_partials")
                    num_partials = (self.behaviour.voice_get(v.id, "automate_num_partials") and
                                    randint(1, max_partials)  or
                                    self.behaviour.voice_get(v.id, "default_num_partial"))
                    partial_pool = choice(wt_item[1])

                    wavetable = fun(v.num_partials, v.partial_pool)
                if not incoming_wavetable:
                    v.num_partials = num_partials
                    v.partial_pool = partial_pool
                    v.wavetable_generation_type = wavetable_generation_type
                self.gateway.stop_notes_of_voice(v.id)
                #print v.id, wavetable
                self.gateway.pd_send_wavetable(v.id, wavetable)
                wavetable = wt

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
                    if  target < 0.3:
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
        return self.speed

    def handle_incoming_message(self, msg):
        """handles incoming messages from the gui interface

        TODO: keep a current-settings dataobject where to track
        all current settings and which can be used to write a snapshot 
        of a particular moment
        """
        key, val = msg.items()[0]
        self.gui_logger.info("incoming message '{0}' with value '{1}'".format(key, val))
        if key[0:6] == 'voice_':
            split = key.split("_")
            vid = int(split[1])
            voice = self.composer.voices[vid]
            v_key = "_".join(split[2:])
            self.behaviour_logger.info("setting {0} of voice {1} to {2}".format(v_key, vid, val))
            if v_key in ['wavetable_generation_type',
                         'num_partials',
                         'partial_pool']:
                setattr(self.composer.voices[vid], v_key, val)
                wavetable = voice.make_wavetable()
                self.set_wavetables(manual=True, wavetable=wavetable, vid=vid)
                return
            # settings that must be transmitted to the sound-engine
            if v_key in ['volume']:
                voice.volume = val
                self.gateway.send_voice_volume(voice, val)
                return
            # this is the standard handling
            self.behaviour["per_voice"][vid][v_key] = val
            if v_key == "mute":
                self.gateway.mute_voice(vid, val == True)
            elif v_key == "trigger_wavetable":
                self.set_wavetables(vid=vid, manual=True)
                self.gui_sender.update_gui(self)
        elif key in self.allowed_incoming_messages:
            if key in self.behaviour.keys():
                self.behaviour_logger.info("setting {0} to {1}".format(key, val))
                self.behaviour[key] = val
            elif key == "play":
                val and self.unpause() or self.pause()
            elif key == "sys":
                if val == 'update':
                    self.gui_sender.update_gui(self)
                elif val == 'save_behaviour':
                    self.behaviour.save_current_behaviour()
                elif val[0] == 'save_behaviour':
                    self.behaviour.save_current_behaviour(name=val[1])
                elif val[0] == 'change_behaviour':
                    new_behaviour = val[1]
                    self.behaviour_logger.info("setting behaviour to: {0}".format(new_behaviour))
                    self.behaviour = BehaviourDict(self.behaviour.saved_behaviours[new_behaviour])
                    for key, per_voice in self.behaviour['per_voice'].items():
                        per_voice = BehaviourDict(per_voice)
                    self.gui_sender.update_gui(self)
                    #TODO: apply new behaviour (attention recreation of behaviour dicts?)
            elif key == 'scale':
                self.composer.set_scale(val)
            elif key == "force_caesura":
                self.force_caesura = True
            elif key == "trigger_wavetable":
                self.behaviour_logger.info("setting a new wavetable for all voices")
                self.set_wavetables(manual=True, voices=self.composer.voices.values())
                self.gui_sender.update_gui(self)
