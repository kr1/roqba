import logging
from OSC import OSCClient, OSCMessage, OSCClientError


logger = logging.getLogger("OSC_hub")
client = OSCClient()
client.connect( ('localhost', 9999))

def hub():
    while True:
        data = (yield)
        logger.info("sending out: {0}".format(data))
        if type(data) == dict:
            address = data["voice"]
            msg = data["message"]
        else:
            address = "gen"
            msg = str(data)
        m = OSCMessage(address)
        m.message = msg
        try:
            client.send(m, 20)
        except OSCClientError:
            pass
            

