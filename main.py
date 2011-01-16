
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
STATE = {"possible":[2,6,9],
         "composer":composer}
director = Director(composer, SPEED, STATE)


def main():
    ## stop execution by setting go to False
    print "app is running in a thread. stop by setting:\nmain.go = False"
    threading.Thread(target = director.play, args=()).start()
    composer.report()

if __name__ == "__main__":
    main()
