import logging
logger = logging.getLogger("OSC_hub")

def hub():
    while True:
        data = (yield)
        logger.info("sending out: {0}".format(data))
