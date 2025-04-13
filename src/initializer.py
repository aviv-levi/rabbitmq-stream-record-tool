import os
import logging
from src.base.facade import Facade


class Initializer:
    def initialize_logger(self):
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO)
        # set higher logging level for httpx to avoid all GET and POST requests being logged
        logging.getLogger("httpx").setLevel(logging.WARNING)

    def initialize(self) -> Facade:
        self.initialize_logger()
        return Facade()