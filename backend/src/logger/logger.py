import logging
import os


class Logger:
    def __init__(self):
        self.log_directory = os.path.join(os.path.dirname(__file__), '..', 'logger')
        self.filename = os.path.join(self.log_directory, 'logs.log')
        self.level = logging.DEBUG
        self.filemode = 'a'
        self.format = '%(asctime)s-%(message)s-%(levelname)s'

        with open(self.filename, 'w'):
            pass

    def set_logger(self) -> None:
        logging.basicConfig(
            level=self.level,
            filename=self.filename,
            filemode=self.filemode,
            format=self.format
        )

    def make_router_logger(self, name: str) -> 'APIRouterLogger':
        lo = logging.getLogger(name)
        lo.setLevel(self.level)
        file_handler = logging.FileHandler(self.filename, mode=self.filemode)
        file_handler.setFormatter(logging.Formatter(self.format))
        lo.addHandler(file_handler)
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(logging.Formatter(self.format))
        # lo.addHandler(stream_handler)

        api_logger = APIRouterLogger(lo)
        return api_logger


class APIRouterLogger:
    def __init__(self, api_logger):
        self.logger = api_logger

    def debug(self, message: str) -> None:
        self.logger.debuge(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.info(message)

    def critical(self, message: str) -> None:
        self.logger.info(message)


logger = Logger()
logger.set_logger()
