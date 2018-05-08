"""
Logger for writing JiRA statistics to a file.
"""
import logging
import os
import time
import utility_path

class JiraLogger:
    """
    Log information retrieved from JiRA.
    """

    def __init__(self, filename=time.strftime("%Y%m%d-%H%M%S"),
                 formatter='%(message)s'):
        """
        Initialize the logger.
        """
        self._logger = logging.getLogger('component_status_update')
        self._logger.setLevel(logging.DEBUG)

        # Initialize a file handler.
        file_handler = logging.FileHandler(os.path.join(
            utility_path.get_main_dir(),
            'logs',
            filename))
        file_handler.setLevel(logging.INFO)

        # Initialize a formatter.
        formatter = logging.Formatter(formatter)

        # Add handler and formatter to logger.
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def debug(self, msg):
        """
        Log a message with level DEBUG on the logger.
        """
        return self._logger.debug(msg)

    def error(self, msg):
        """
        Log a message with level ERROR on the logger.
        """
        return self._logger.error(msg)

    def info(self, msg):
        """
        Log a message with level INFO on the logger.
        """
        return self._logger.info(msg)
