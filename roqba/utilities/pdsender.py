import time
import logging
import socket


class PdSender(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = logging.getLogger("sender")
        self.send("sound 1")

    @staticmethod
    def format_msg_list(msg):
        '''formats an incoming list as a space separated string'''
        if msg.__class__ == [].__class__: 
            msg = " ".join(map(lambda x: str(x), msg))
        return msg

    def send(self, msg):
        '''formats and sends an incoming message to the specified host:port

        as a UDP Datagram
        msg -> list'''
        msg = self.format_msg_list(msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("{0}\n".format(msg) + "\n", (self.host, self.port))

    def __del__(self):
        print "switching off the lights...."
        self.send("sound 0")

if __name__ == "__main__":
    import random
    pd = PdSender("msf", 11211)
    pd.send("sound 1")
    for i in xrange(4):
        pd.send(["ctl 1", random.randrange(60, 75)])
        time.sleep(0.15)
        pd.send(["ctl 2", random.randrange(60, 75)])
        time.sleep(0.15)
    pd.send(["ctl", 1, -1, "\nctl", 2, -1])
