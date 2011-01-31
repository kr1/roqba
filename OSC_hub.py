import logging

from OSC import OSCClient, OSCMessage, OSCClientError
from roqba_sc import *

HOST = "localhost"
PORT = 9999

## XxxxX: make these settings configurable
block_messages = False
logger = logging.getLogger("OSC_hub")
#client = OSCClient()
#client.connect((HOST, PORT))
client = SC_Gateway("192.168.0.104")
client.load_scsyndef()
client.create_nodes(3)


def send(address, msg):
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


def hub():
    while True:
        data = (yield)
        logger.info("sending out: {0}".format(data))
        if type(data) == dict:
            for v in data.values():
                if v.note_change:
                    address = v.id
                    msg = v.note
                    logger.info("sending out: /{0}/{1} for id:{2}".\
                               format(address, msg, v.id))
                    send(address, msg)
            #address = data["voice"]
            #msg = data["message"]
        else:
            address = "gen"
            msg = str(data)
