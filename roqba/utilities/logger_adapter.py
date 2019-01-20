import os
import logging


class StyleLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        ROQBA_STYLE = os.environ.get("ROQBA_STYLE", None)
        if ROQBA_STYLE:
            return '[{}] {}'.format(ROQBA_STYLE, msg), kwargs
        return msg, kwargs

    def debug(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)
