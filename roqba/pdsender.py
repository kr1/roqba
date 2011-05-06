import time
from  subprocess import PIPE, Popen
from mock import Mock
import logging

def sound_off():
    pd = PdSender.create_sender("localhost", 11211)
    pd.stdin.write("sound 0\n")
    return pd

class PdSender(object):
    def __init__(self, host, port):
        self.host = host
        self.logger = logging.getLogger("sender")
        self.port = port
        self.pd = self.create_sender(host, port)
        self.no_pd = False
        self.send("sound 1")

    @staticmethod
    def create_sender(host, port):
        pd = Popen('pdsend {0} {1} udp'.format(port, host),
                    shell=True,
                    stdin=PIPE)
        return pd

    def send(self, msg):
        if msg.__class__ == [].__class__:
            msg = " ".join(map(lambda x: str(x),msg))
        if self.no_pd:
            self.logger.info("no pd instance")
        try:
            res = self.pd.stdin.write("{0}\n".format(msg))
            return res
        except:
            msg = "no pd-instance found, falling back to mocking!"
            self.no_pd = True
            print msg
            self.logger.info(msg)
            self.send = Mock()


    def __del__(self):
        print "switching off the lights...."
        self.send("sound 0")

if __name__ == "__main__":
    import random
    pd = PdSender("msf", 11211)
    pd.send("sound 1")
    for i in xrange(4):
        pd.send(["ctl 1",random.randrange(60, 75)])
        time.sleep(0.15)
        pd.send(["ctl 2",random.randrange(60, 75)])
        time.sleep(0.15)
    pd.send(["ctl", 1, -1, "\nctl", 2, -1])


