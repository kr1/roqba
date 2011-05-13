import logging
import time
from metronome import HEAVY

from pdsender import PdSender

#HOST = "localhost"
#PORT = 9999
PD_HOST = "localhost"
PD_PORT = 12321
block_messages = False
TRANSPOSE = 12


class NoteGateway(object):
    def __init__(self):
        ## XxxxX: make these settings configurable
        self.logger = logging.getLogger("sender")
        self.slide = True
        self.slide_duration_prop = 0.7
        self.voice_ids = []
        self.transpose = TRANSPOSE
        self.pd = PdSender(PD_HOST, PD_PORT)

    def pause(self):
        self.block_messages = True
        self.pd.send("sound 0")

    def unpause(self):
        self.block_messages = True
        self.pd.send("sound 1")

    def stop(self):
        time.sleep(1)
        del self.pd

    def stop_all_notes(self):
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

    def pd_send_note(self, voice_id, msg):
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
            self.logger.info("sending out: {0}".format(data))
            if type(data) == dict:
                for v in data.values():
                    if v.note_change:
                        msg = v.real_note if v.real_note else 0
                        #self.logger.info("sending out: voice: {1}: {0}".\
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
                            self.pd.send(["voice", "rhythm", v.id,
                                str(v.note_length_grouping).replace(",", "_")])
                #address = data["voice"]
                #msg = data["message"]
            else:
                msg = str(data)
