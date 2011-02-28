
from Queue import Queue
import time
import logging
import threading
import logging.config

from voice import Voice
from composer import Composer
from director import Director
import note_gateway

gateway = note_gateway.NoteGateway()
gateway.hub().next()


def startup():
    logger.info("starting up ===========------------------->>>>>>>>>>>>>>>")
    c = Composer(gateway)
    v1 = Voice(1, c)
    v1.set_state("HIGH")
    v2 = Voice(2, c)
    v2.set_state("MID")
    v3 = Voice(3, c)
    v3.set_state("MID")
    v4 = Voice(4, c)
    v4.set_state("BASS")
    return c
logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

go = True
composer = startup()
SPEED = 0.300
STATE = {"comp": composer, "speed": SPEED}
director = Director(composer, STATE)


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
