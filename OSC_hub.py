import logging
from OSC import OSCClient, OSCMessage, OSCClientError


logger = logging.getLogger("OSC_hub")
client = OSCClient()
client.connect( ('localhost', 9999))

def hub():
    while True:
        data = (yield)
        m = OSCMessage(data["voice"])
        m.message = data["message"]
        logger.info("sending out: {0}".format(data))
        try:
            client.send(m, 20)
        except OSCClientError:
            pass
            

