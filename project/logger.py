import sys
import logging


class Logger(object):
    _logger = None

    @classmethod
    def logger(cls):
        if not Logger._logger:
            Logger._logger = logging.getLogger('Invera_todo')
            Logger._logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            log_format = (
                f"[%(asctime)s:%(levelname)s:%(module)s.py-%(lineno)d"
                f"] %(message)s"
            )
            date_format = '%y-%m-%d@%H:%M:%S'
            formatter = logging.Formatter(log_format, datefmt=date_format)
            handler.setFormatter(formatter)
            Logger._logger.addHandler(handler)
        return Logger._logger
