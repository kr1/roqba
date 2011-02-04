
from Queue import Queue
import time
import logging
import threading
import logging.config

from voice import Voice
from composer import Composer
from director import Director
import OSC_hub

gateway = OSC_hub.NoteGateway()
gateway.hub().next()


def startup():
    logger.info("starting up ===========------------------->>>>>>>>>>>>>>>")
    s = gateway.hub()
    s.next()  # get the coroutine to the yield
    c = Composer(gateway)
    v1 = Voice(0, s, c)
    v2 = Voice(1, s, c)
    v3 = Voice(2, s, c)
    #v4 = Voice(3, s, c)
    return c
logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

go = True
composer = startup()
SPEED = 0.150
STATE = {"comp": composer}
METER = [2, 0, 1, 0, 1, 0, 1, 0]
#METER = [2, 0, 0, 0, 1, 0, 0, 0]
director = Director(composer, SPEED, STATE, METER)


def main():
    threading.Thread(target=director._play, args=()).start()
    composer.report()

if __name__ == "__main__":
    print '''please run this app from the interpreter as:
    \b\b\b\bimport main
    \b\b\b\bmain.main()
    \b\b\bstop it with:
    \b\b\b\bmain.director.stop()
    '''
