"""the purpose of this class is to communicate with the sound-engine.

its main concerns are:
- starting, stopping, pausing the engine
- sending notes
- sending controlling messages
"""
from random import random, choice
import logging
import time

from metronome import HEAVY
from utilities.pdsender import PdSender


class NoteGateway(object):
    def __init__(self, settings, behaviour):
        self.logger = logging.getLogger("sender")
        self.settings = settings
        self.slide = True
        self.behaviour = behaviour
        self.slide_duration_prop = behaviour['slide_duration_prop']
        self.voice_ids = []
        self.block_messages = False
        self.transpose = behaviour["transpose"]
        self.behaviour = behaviour
        self.pd = PdSender(settings["PD_HOST"], settings["PD_PORT"])
        self.hub = self.hub_gen()
        self.hub.next()
        self.drum_hub = self.drum_hub_gen()
        self.drum_hub.next()

    def pause(self):
        '''blocks new messages and turns off sound-production'''
        self.block_messages = True
        self.pd.send("sound 0")

    def unpause(self):
        '''turns on sound-production and lets messages flow again'''
        self.block_messages = False
        self.pd.send("sound 1")

    def stop(self):
        '''destroys the puredata-sender object'''
        time.sleep(1)
        del self.pd

    def stop_all_notes(self):
        '''sends a stop message to all active voices'''
        for v in self.voice_ids:
            self.stop_notes_of_voice(v)

    def stop_notes_of_voice(self, vid):
        '''sends the stop message to a specified voice'''
        self.pd.send(["voice", vid, 0])

    def mute_voice(self, vid, val):
        '''sends a message to mute/unmute a voice to pd

        use vid=drums to mute/unmute the drums
        '''
        val = 1 if val else 0
        if vid == "drums":
            msg = ["perc", "mute", val]
        else:
            msg = ["voice", vid, "mute", val]
        self.pd.send(msg)

    def set_slide_to_0(self):
        '''this method bypasses the slide functionality

        by setting slide-duration to 0'''
        self.logger.info("Send slide to 0")
        for v in self.voice_ids:
            self.pd.send(["voice", "slide", v, 0])

    def set_slide_msecs(self, voice_id, msecs):
        '''sends a message containing the general slide-time in millisecs'''
        self.pd.send(["voice", "slide", voice_id, msecs])

    def set_slide_msecs_for_all_voices(self, msecs):
        '''sends a message containing the general slide-time in millisecs'''
        for v in self.voice_ids:
            self.pd.send(["voice", "slide", v, msecs])

    def pd_send_note(self, voice_id, msg):
        '''send out a single note'''
        if voice_id not in self.voice_ids:
            self.voice_ids.append(voice_id)
        detune = self.settings.get('humanize_oscillator_tuning')
        if detune:
            detune = random() * detune * choice([1, -1])
            self.logger.info("detune: {}".format(detune))
        else:
            detune = 0
        self.pd.send(["voice", voice_id, 0 if msg == 0 else
                      msg + self.transpose + detune])
        return True

    def pd_send_duration(self, voice_id, val):
        '''send out the duration for a given voice'''
        if voice_id not in self.voice_ids:
            self.voice_ids.append(voice_id)
        self.pd.send(["voice", voice_id, "dur", val])
        return True

    def pd_send_wavetable(self, voice_id, wavetable):
        '''send out the duration for a given voice'''
        self.pd.send(["voice", voice_id, "wavetable", wavetable])
        return True

    def send_voice_pan(self, voice, pan):
        '''sends a pan-message for a voice'''
        args = ["sound", "pan", voice.id, pan]
        self.pd.send(args)

    def send_voice_volume(self, voice, val):
        '''sends a volume message for a voice

        use values from 0 to 1'''
        args = ["voice", voice.id, "volume", val]
        # print "sending: ", args
        self.pd.send(args)

    def send_voice_adsr(self, voice, adsr):
        '''sends a adsr-message for a voice'''
        args = ["voice", voice.id, "adsr", " ".join([str(element) for element in adsr])]
        self.pd.send(args)

    def send_voice_peak_level(self, voice, peak_level):
        '''sends a peak_level-message for a voice'''
        args = ["voice", voice.id, "peak_level", "{:.6f}".format(peak_level)]
        self.pd.send(args)

    def pd_send_drum_note(self, voice,  vol, pan, ctl):
        '''sends a note-message for a drum-voice'''
        args = ["perc", voice, vol, pan, ctl]
        self.pd.send(args)

    def set_drum_volume(self, vol):
        '''sends volume for the drums'''
        args = ["perc", "vol", str(vol)]
        self.pd.send(args)

    def drum_hub_gen(self):
        '''generator method that sends notes to all drum voices

        according to present state'''
        while True:
            data = (yield)
            if not self.block_messages:
                self.logger.info("drums out: {0}".format(data))
                for k, v in data.items():
                    if v["meta"] != "empty":
                        args = ["perc", k]
                        if v["vol"]:
                            args.append(v["vol"])
                        args.append(v["pan"])
                        if v["ctl"]:
                            args.append(v["ctl"])
                        self.pd.send(args)

    def hub_gen(self):
        '''generator method that sends notes to all melodic voices

        according to the present state'''
        while True:
            data = (yield)
            if self.block_messages:
                continue
            self.logger.info("sending out: {0}".format(data))
            if type(data) == dict:
                for v in data.values():
                    if v.note_change:
                        msg = v.real_note if v.real_note else 0
                        # self.logger.info("sending out:\ voice: {1}: {0}".\ format(msg, v.id))
                        if self.slide and v.slide:
                            if self.behaviour.voice_get(v.id, "use_proportional_slide_duration"):
                                # self.logger.info("{0} has slide_prop: {1}".format(
                                #    v.id, v.slide_duration_prop))
                                dur_prop = v.slide_duration_prop
                                slide_length = v.duration_in_msec * dur_prop
                            else:
                                slide_length = self.behaviour.voice_get(
                                    v.id, "slide_duration_msecs")
                            self.set_slide_msecs(v.id, slide_length)
                        self.pd_send_duration(v.id, v.duration_in_msec * v.note_duration_prop)
                        self.pd_send_note(v.id, msg)
                        if v.weight == HEAVY:
                            self.pd.send(["voice",
                                          "rhythm",
                                          v.id,
                                          str(v.note_length_grouping).replace(",", "_")])
            else:
                msg = str(data)

    def set_transpose(self, val):
        self.transpose = val
