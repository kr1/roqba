import time
import logging
import socket
from queue import deque


class Sender(object):
    def __init__(self):
        self.msg_queue = deque([], 3000)

    def trace_send(self, msg):
        self.msg_queue.append((int(time.time() * 1000), msg))


class PdSender(Sender):
    def __init__(self, host, port):
        super(PdSender, self).__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logger = logging.getLogger("sender")
        self.send("sound 1")

    @staticmethod
    def format_msg_list(msg):
        '''formats an incoming list as a space separated string'''
        if msg.__class__ == [].__class__:
            msg = " ".join([str(x) for x in msg])
        return msg

    def send(self, msg):
        '''formats and sends an incoming message to the specified host:port

        as a UDP Datagram
        msg -> list'''
        msg = self.format_msg_list(msg)
        self.trace_send(msg)
        self.sock.sendto(str.encode("{0}\n".format(msg) + "\n"), (self.host, self.port))

    def __del__(self):
        self.logger.info("setting sound to 0. switching off the lights....")
        self.send("sound 0")

if __name__ == "__main__":
    import random
    pd = PdSender("msf", 11211)
    pd.send("sound 1")
    for i in range(4):
        pd.send(["ctl 1", random.randrange(60, 75)])
        time.sleep(0.15)
        pd.send(["ctl 2", random.randrange(60, 75)])
        time.sleep(0.15)
    pd.send(["ctl", 1, -1, "\nctl", 2, -1])
