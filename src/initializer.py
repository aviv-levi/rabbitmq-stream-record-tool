import logging

import pika

from src.base.facade import Facade
import yaml


class Initializer:
    def initialize_logger(self):
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO)
        logging.getLogger("pika").setLevel(logging.WARNING)


    def initialize_configuration(self):
        with open("src/configuration.yaml") as stream:
            return yaml.safe_load(stream)

    def initialize_rabbitmq_channel(self, rabbitmq_configuration):
        connection_parameters = pika.ConnectionParameters(host=rabbitmq_configuration["Host"],
                                                          port=rabbitmq_configuration["Port"],
                                                          credentials=pika.PlainCredentials(
                                                              username=rabbitmq_configuration["Username"],
                                                              password=rabbitmq_configuration["Password"]))
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        return channel

    def initialize(self) -> Facade:
        self.initialize_logger()
        configuration = self.initialize_configuration()
        channel = self.initialize_rabbitmq_channel(configuration['RabbitMq'])
        return Facade(configuration=configuration, channel=channel)