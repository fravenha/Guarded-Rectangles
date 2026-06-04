import logging
import os

LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL", "INFO")

class LambdaLevelFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG:   "[%(levelname)s] %(message)s  | (%(module)s:%(funcName)s:%(lineno)d)",
        logging.INFO:    "[%(levelname)s] %(message)s", 
        logging.WARNING: "[%(levelname)s] %(message)s  | (%(module)s:%(funcName)s:%(lineno)d)",
        logging.ERROR:   "[%(levelname)s] %(message)s  | (%(module)s:%(funcName)s:%(lineno)d)",
        logging.CRITICAL:"[%(levelname)s] %(message)s  | (%(module)s:%(funcName)s:%(lineno)d)"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.basicConfig(
    level = LOGGER_LEVEL,
    force = True,
)

custom_formatter = LambdaLevelFormatter()
for handler in logging.root.handlers:
    handler.setFormatter(custom_formatter)

logger = logging.getLogger("lambda")
"""Preconfigures logger, defaults to `INFO` level
Logger levels:  
DEBUG < INFO < WARN < ERROR
"""