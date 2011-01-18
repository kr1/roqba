
from Queue import Queue
import time
import logging
import threading
import logging.config

from voice import Voice
from composer import Composer
from director import Director
from OSC_hub import hub

def startup():
    #logging.basicConfig(filename="log.txt")
    #logger = logging.getLogger('startup')
    #logger.setLevel(logging.INFO)
    logger.info("starting up ===========------------------->>>>>>>>>>>>>>>")
    s = hub()
    s.next() # get the coroutine to the yield
    c = Composer()
    v1 = Voice(1, s, c)
    v2 = Voice(2, s, c)
    v3 = Voice(3, s, c)
    return c
logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

go = True 
composer = startup()
SPEED = 0.250
STATE = {"comp":composer}
director = Director(composer, SPEED, STATE)


def main():
    threading.Thread(target = director.play, args=()).start()
    composer.report()

if __name__ == "__main__":
    print '''please run this app from the interpreter as:
    \b\b\b\bimport main
    \b\b\b\bmain.main()
    \b\b\bstop it with:
    \b\b\b\bmain.director.stop()
    '''
