import logging
from OSC import OSCClient, OSCMessage, OSCClientError


logger = logging.getLogger("OSC_hub")
client = OSCClient()
client.connect( ('localhost', 9999))

def send(address, msg):        
    m = OSCMessage(address)
    m.message = msg
    try:
        client.send(m, 20)
    except OSCClientError:
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
                    logger.info("sending out: /{0}/{1} for id:{2}".format(address, msg, v.id))
                    send(address, msg)
            #address = data["voice"]
            #msg = data["message"]
        else:
            address = "gen"
            msg = str(data)
        
        

