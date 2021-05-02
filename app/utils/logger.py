"""Complete Logging Module."""

import logging
from .singleton import Singleton
import os
from pathlib import Path
from .configuration import Configurations
from .constants import PROJECT_NAME

conf = Configurations()


class Logger(metaclass=Singleton):
    """Logger wrapper with all config and its wrapper methods."""

    def __init__(self):
        """Initialation Class."""
        directory = Path("logs")
        if not os.path.exists(directory):
            os.makedirs(directory)
        static_directory = Path("static")
        if not os.path.exists(static_directory):
            os.makedirs(static_directory)
        # setting loglevel from config.json
        input_level = conf.log_level
        if input_level is None:
            level = logging.getLevelName("INFO")
        else:
            level = logging.getLevelName(input_level)
        self.logger = logging.getLogger(PROJECT_NAME)
        self.logger.setLevel(level)
        log_file = os.path.join(directory, "{}.log".format(PROJECT_NAME))
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        log_handler = logging.FileHandler(log_file, mode="a", delay=0, encoding=None)
        log_handler.setFormatter(log_format)

        log_handler.setLevel(level)
        self.logger.addHandler(log_handler)

    def info(self, msg):
        """Logger wrapper for info level."""
        self.logger.info(msg)

    def warn(self, msg):
        """Logger wrapper for warn level."""
        self.logger.warning(msg)

    def error(self, msg):
        """Logger wrapper for error level."""
        self.logger.error(msg)

    def exception(self, msg):
        """Logger wrapper for exception level."""
        self.logger.exception(msg)

    def critical(self, msg):
        """Logger wrapper for critical level."""
        self.logger.critical(msg)

    def debug(self, msg):
        """Logger wrapper for debug level."""
        self.logger.debug(msg)
