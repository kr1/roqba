import logging
import time

from metronome import HEAVY
from utilities.pdsender import PdSender


class NoteGateway(object):
    def __init__(self, settings, behaviour):
        self.logger = logging.getLogger("sender")
        self.settings = settings
        self.slide = True
        self.slide_duration_prop = behaviour['default_slide_duration_prop']
        self.voice_ids = []
        self.block_messages = False
        self.transpose = behaviour["transpose"]
        self.pd = PdSender(settings["PD_HOST"], settings["PD_PORT"])

    def pause(self):
        '''blocks new messages and turns off sound-production'''
        self.block_messages = True
        self.pd.send("sound 0")

    def unpause(self):
        '''turns on sound-production and lets messages flow again'''
        self.block_messages = True
        self.pd.send("sound 1")

    def stop(self):
        '''destroys the puredata-sender object'''
        time.sleep(1)
        del self.pd

    def stop_all_notes(self):
        '''sends a stop message to all active voices'''
        for v in self.voice_ids:
            self.pd.send(["voice", v, 0])

    def set_slide_to_0(self):
        '''this method bypasses the slide functionality

        by setting slide-duration to 0'''
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
        self.pd.send(["voice", voice_id, 0 if msg == 0 else
                                         msg + self.transpose])
        return True

    def pd_send_drum_note(self, voice,  vol, pan, ctl):
        '''sends a note-message for a drum-voice'''
        args = ["perc", voice, vol, pan, ctl]
        self.pd.send(args)

    def drum_hub(self):
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

    def hub(self):
        '''generator method that sends notes to all melodic voices

        according to the present state'''
        while True:
            data = (yield)
            if not self.block_messages:
                self.logger.info("sending out: {0}".format(data))
                if type(data) == dict:
                    for v in data.values():
                        if v.note_change:
                            msg = v.real_note if v.real_note else 0
                            #self.logger.info("sending out:\
                            #                  voice: {1}: {0}".\
                            #                  format(msg, v.id))
                            if self.slide and v.slide:
                                if v.slide_duration_prop:
                                    dur_prop = v.slide_duration_prop
                                else:
                                    dur_prop = self.slide_duration_prop
                                self.set_slide_msecs(v.id,
                                              (v.duration_in_msec * dur_prop))
                            self.pd_send_note(v.id, msg)
                            if v.weight == HEAVY:
                                self.pd.send(["voice",
                                              "rhythm",
                                              v.id,
                                              str(v.note_length_grouping).\
                                                  replace(",", "_")])
                    #address = data["voice"]
                    #msg = data["message"]
                else:
                    msg = str(data)