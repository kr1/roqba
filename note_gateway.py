import logging
import time
from metronome import HEAVY

from pdsender import PdSender

#HOST = "localhost"
#PORT = 9999
PD_HOST = "localhost"
PD_PORT = 11211
block_messages = False
TRANSPOSE = 12


class NoteGateway(object):
    def __init__(self):
        ## XxxxX: make these settings configurable
        self.logger = logging.getLogger("sender")
        #client = OSCClient()
        #client.connect((HOST, PORT))
        #client = SC_Gateway("192.168.0.104")
        #client.load_scsyndef()
        #client.create_nodes(3)
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
        time.sleep(2)
        del self.pd

    def stop_all_notes(self):
        for v in self.voice_ids:
            self.pd.send(["voice", v, 0])
    
    def set_slide_to_0(self):
        for v in self.voice_ids:
            self.pd.send(["voice", "slide", v, 0])
        

    def pd_send_note(self, voice_id, msg):
        if voice_id not in self.voice_ids:
            self.voice_ids.append(voice_id)
        self.pd.send(["voice", voice_id, msg + self.transpose])
        return True

    def hub(self):
        while True:
            data = (yield)
            self.logger.info("sending out: {0}".format(data))
            if type(data) == dict:
                for v in data.values():
                    if v.note_change:
                        msg = v.real_note if v.real_note else 0
                        self.logger.info("sending out: voice: {1}: {0}".\
                                          format(msg, v.id))
                        #send(address, msg)
                        if self.slide and v.slide:
                            if v.slide_duration_prop:
                                dur_prop = v.slide_duration_prop
                            else:
                                dur_prop = self.slide_duration_prop
                            self.pd.send(["voice",
                                          "slide",
                                          v.id,
                                          (v.duration_in_msec *  dur_prop)])
                        self.pd_send_note(v.id, msg)
                        if v.weight == HEAVY:
                            self.pd.send(["voice", "rhythm", v.id,
                                str(v.note_length_grouping).replace(",", "_")])
                #address = data["voice"]
                #msg = data["message"]
            else:
                address = "gen"
                msg = str(data)
