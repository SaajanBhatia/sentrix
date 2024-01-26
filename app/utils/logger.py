import logging
from logging.handlers import RotatingFileHandler


class CustomLogger:
    MAIN_LOG_FILEPATH = 'logs/app.log'

    def __init__(self, name):
        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler which logs even debug messages
        fh = RotatingFileHandler(
            CustomLogger.MAIN_LOG_FILEPATH, maxBytes=1000000, backupCount=5)
        fh.setLevel(logging.DEBUG)

        # Create a formatter and set the formatter for the handler.
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)
