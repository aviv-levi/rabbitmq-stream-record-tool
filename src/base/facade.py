import logging
import os
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path

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
        return [
            Path(file_path).read_bytes()
            for root, _, files in os.walk(path)
            for file_path in [os.path.join(root, file) for file in files]
            if os.path.isfile(file_path)
        ]

    def _start_stream(self):
        logger.info("Facade start_stream")
        stream_conf = self._configuration['Stream']
        self._channel.exchange_declare(exchange=stream_conf['Exchange'])

        binary_files = self._get_stream_files(stream_conf)

        rate = stream_conf['Rate']
        duration = stream_conf['Duration']
        exchange = stream_conf['Exchange']
        loop = bool(stream_conf['Loop'])

        sent_count = 0
        elapsed_seconds = 0

        while elapsed_seconds < duration and (loop or sent_count == 0):
            for i, binary_data in enumerate(binary_files):
                if sent_count % rate == 0:
                    time.sleep(1)
                    elapsed_seconds += 1
                    if elapsed_seconds == duration:
                        break
                self._channel.basic_publish(
                    exchange=exchange,
                    routing_key='/',
                    body=binary_data
                )
                sent_count += 1

    def _get_stream_files(self, stream_conf):
        match stream_conf['From']:
            case 'Local':
                source_path = stream_conf['Local']['Source']
                return self._load_local_binary_files(source_path)
            case 'S3':
                # TODO: Implement S3 streaming support
                return []
            case _:
                raise Exception("Unknown stream source")

    def _start_record(self):
        logger.info("Facade start_record")
        record_conf = self._configuration['Record']
        duration = int(record_conf['Duration'])

        queue_name = f'rabbitmq-stream-record-tool-{uuid.uuid4()}'
        self._channel.queue_declare(queue=queue_name, exclusive=True)
        self._channel.queue_bind(exchange=record_conf['Exchange'], queue=queue_name, routing_key='/')

        self._channel.basic_consume(
            queue=queue_name,
            on_message_callback=lambda ch, method, props, body: self._handle_record_message(record_conf, body),
            auto_ack=True
        )

        def start_consuming():
            try:
                self._channel.start_consuming()
            except pika.exceptions.ConnectionClosedByBroker:
                logger.warning("Connection closed by broker")

        consume_thread = threading.Thread(target=start_consuming)
        consume_thread.start()

        time.sleep(duration)

        self._channel.stop_consuming()
        consume_thread.join()

        self._channel.queue_unbind(exchange=record_conf['Exchange'], queue=queue_name, routing_key='/')
        self._channel.queue_delete(queue=queue_name)

    def _handle_record_message(self, record_conf, body):
        match record_conf['To']:
            case 'Local':
                self._save_message_to_local(record_conf['Local']['Destination'], body)
            case 'S3':
                # TODO: Implement S3 upload support
                pass
            case _:
                raise Exception("Unknown record destination")

    def _save_message_to_local(self, destination_dir, body):
        Path(destination_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uuid.uuid4()}.txt"
        filepath = Path(destination_dir) / filename
        try:
            filepath.write_text(body.decode(), encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to save file {filepath}: {e}")
