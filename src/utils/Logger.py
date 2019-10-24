import logging
from utils.TimeUtils import *

class LoggerUtils():
    def __init__(self, log_filename):
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)

    def debug_with_time(self, message):
        logging.debug("{} => {}".format(get_current_time(), message))
    
    def debug(self, message):
        logging.debug(message)

    def info_with_time(self, message):
        logging.info("{} => {}".format(get_current_time(), message))

    def info(self, message):
        logging.info(message)

    def error_with_time(self, message):
        logging.error("{} => {}".format(get_current_time(), message))

    def error(self, message):
        logging.error(message)

    def exception_with_time(self, message):
        logging.exception("{} => {}".format(get_current_time(), message))

    def exception(self, message):
        logging.exception(message)
        