import logging
import os
import threading
import time
import uuid
from datetime import datetime

import pika
from src.core.running_mode import running_mode

logger = logging.getLogger(__name__)

class Facade:
    def __init__(self, configuration, channel, mode):
        self._configuration = configuration
        self._channel = channel
        self._mode = mode

    def start(self):
        logger.info("Facade started")
        match self._mode:
            case running_mode.stream:
                self._start_stream()
            case running_mode.record:
                self._start_record()
            case _:
                raise Exception("Unknown running mode")

    def _load_local_binary_files(self, path):
        binary_files = []
        for root, _, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "rb") as f:
                        binary_data = f.read()
                        binary_files.append(binary_data)
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")
        return binary_files

    def _start_stream(self):
        logger.info("Facade start_stream")
        binary_files = []
        stream_configuration = self._configuration['Stream']
        self._channel.exchange_declare(exchange=stream_configuration['Exchange'])

        match stream_configuration['From']:
            case 'Local':
                local_configuration = stream_configuration['Local']
                binary_files = self._load_local_binary_files(local_configuration['Source'])
            case 'S3':
                pass
            case _:
                raise Exception("Unknown Datasource")

        rate = stream_configuration['Rate']
        duration = stream_configuration['Duration']
        exchange = stream_configuration['Exchange']
        loop = bool(stream_configuration['Loop'])
        sent_count = 0
        seconds = 0
        while seconds < duration and (loop or sent_count == 0):
            for i in range(len(binary_files)):
                if sent_count % rate == 0:
                    time.sleep(1)
                    seconds += 1
                    if seconds == duration:
                        break
                self._channel.basic_publish(exchange=exchange,
                      routing_key='/',
                      body=binary_files[i])
                sent_count += 1

    def _start_record(self):
        logger.info("Facade start_record")
        record_configuration = self._configuration['Record']


        queue_name = f'rabbitmq-stream-record-tool-{uuid.uuid4()}'
        duration = int(record_configuration['Duration'])
        self._channel.queue_declare(queue=queue_name, exclusive=True)
        self._channel.queue_bind(exchange=record_configuration['Exchange'], queue=queue_name, routing_key='/')

        def callback(ch, method, properties, body):
            match record_configuration['To']:
                case 'Local':
                    local_configuration = record_configuration['Local']
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{uuid.uuid4()}.txt"
                    filepath = os.path.join(local_configuration['Destination'], filename)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(body.decode())
                case 'S3':
                    pass
                case _:
                    raise Exception("Unknown Datasource")



        self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        # Start consuming in a separate thread
        def start_consuming():
            try:
                self._channel.start_consuming()
            except pika.exceptions.ConnectionClosedByBroker:
                pass

        consume_thread = threading.Thread(target=start_consuming)
        consume_thread.start()

        time.sleep(duration)

        self._channel.stop_consuming()
        consume_thread.join()

        self._channel.queue_unbind(exchange=record_configuration['Exchange'], queue=queue_name, routing_key='/')
        self._channel.queue_delete(queue=queue_name)