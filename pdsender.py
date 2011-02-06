import time
from  subprocess import PIPE, Popen


class PdSender(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pd = self.create_sender(host, port)
        self.send("sound 1")
    
    def create_sender(self, host, port):
        pd = Popen('pdsend {0} {1} udp'.format(port, host),
                    shell=True,
                    stdin=PIPE)
        return pd

    def send(self, msg):
        if msg.__class__ == [].__class__:
           msg = " ".join(map(lambda x: str(x),msg))
        self.pd.stdin.write("{0}\n".format(msg))
        return True

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


