import logging

from OSC import OSCClient, OSCMessage, OSCClientError
from roqba_sc import *
from pdsender import PdSender

HOST = "localhost"
PORT = 9999
PD_HOST = "msf"
PD_PORT = 11211
block_messages = False
TRANSPOSE = 30

class NoteGateway(object):
    def __init__(self):
        ## XxxxX: make these settings configurable
        self.logger = logging.getLogger("OSC_hub")
        #client = OSCClient()
        #client.connect((HOST, PORT))
        #client = SC_Gateway("192.168.0.104")
        #client.load_scsyndef()
        #client.create_nodes(3)
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

    def pd_send_note(self, voice_id, msg):
        self.pd.send(["ctl", voice_id, msg + TRANSPOSE])
        return True
        
    def send(self, address, msg):
        if not block_messages:
            if msg > 0:
                if msg < 70:
                    msg = (msg+12)**1.7
                client.play_note(client.node_ids[address], msg)
            else:
                client.stop_note(client.node_ids[address])
        return True
    #    m = OSCMessage(address)
    #    m.message = msg
    #    try:
    #        client.send(m, 20)
    #    except OSCClientError:
    #        logger.error("error sending OSC message: {0} to {1}:{2}".format(msg,
    #                                                                        HOST,
    #                                                                        PORT))
    #        pass
    
    
    def hub(self):
        while True:
            data = (yield)
            self.logger.info("sending out: {0}".format(data))
            if type(data) == dict:
                for v in data.values():
                    if v.note_change:
                        address = v.id
                        msg = v.note
                        self.logger.info("sending out: /{0}/{1} for id:{2}".\
                                   format(address, msg, v.id))
                        #send(address, msg)
                        self.pd_send_note(v.id, msg)
                #address = data["voice"]
                #msg = data["message"]
            else:
                address = "gen"
                msg = str(data)
