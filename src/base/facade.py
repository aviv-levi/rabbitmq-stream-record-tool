import logging

logger = logging.getLogger(__name__)

class Facade:
    def __init__(self, configuration, channel):
        self._configuration = configuration
        self._channel = channel

    def start(self):
        logger.info("Facade start")
        self._channel.queue_declare(queue='hello')