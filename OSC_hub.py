import logging
from OSC import OSCClient, OSCMessage, OSCClientError

HOST = "localhost"
PORT = 9999

logger = logging.getLogger("OSC_hub")
client = OSCClient()
client.connect((HOST, PORT))


def send(address, msg):
    m = OSCMessage(address)
    m.message = msg
    try:
        client.send(m, 20)
    except OSCClientError:
        logger.error("error sending OSC message: {0} to {1}:{2}".format(msg,
                                                                        HOST,
                                                                        PORT))
        pass


def hub():
    while True:
        data = (yield)
        logger.info("sending out: {0}".format(data))
        if type(data) == dict:
            for v in data.values():
                if v.note_change:
                    address = str(v.id)
                    msg = str(v.note)
                    logger.info("sending out: /{0}/{1} for id:{2}".\
                               format(address, msg, v.id))
                    send(address, msg)
            #address = data["voice"]
            #msg = data["message"]
        else:
            address = "gen"
            msg = str(data)
