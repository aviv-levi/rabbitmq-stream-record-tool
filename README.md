# RabbitMQ Stream & Record Tool

A lightweight and easy-to-use side project that enables streaming and recording of RabbitMQ messages using a simple, declarative configuration file.

## Modes of Operation

The tool runs with a single argument that determines the mode:

- `stream` – Reads messages from a local folder or S3 and publishes them to a RabbitMQ exchange at a defined rate and duration. Supports looping.
- `record` – Listens to a RabbitMQ exchange using a temporary queue (auto-delete) and saves the incoming messages to a local folder or S3 for a defined duration.

## Configuration Example

```yaml
RabbitMq:
  Host: localhost
  Port: 5672
  Username: guest
  Password: guest

Stream:
  Loop: True
  Duration: 60
  Rate: 100
  Exchange: StreamExample
  From: Local
  Local:
    Source: StreamFolderExample
  S3:
    Url: Placeholder
    Bucket: Placeholder
  Redis:
    Url: Placeholder

Record:
  Duration: 60
  Exchange: RecordExample
  To: Local
  Local:
    Destination: RecordFolderExample
  S3:
    Url: Placeholder
    Bucket: Placeholder
  Redis:
    Url: Placeholder
```

## Key Features

- **Streaming** of messages (JSON files or other formats):
  - Control message rate (messages per second)
  - Set streaming duration in seconds
  - Optional loop mode
  - Support for local folders or S3 as source

- **Recording** of messages:
  - Uses a temporary (auto-delete) queue to consume messages
  - Saves messages to a local folder or S3
  - Supports fixed listening duration

- S3 support as input/output source

- Redis integration planned for future 


## Example Usage

```bash
# Stream messages from a local folder or S3 to a RabbitMQ exchange
python main.py stream

# Record messages from a RabbitMQ exchange and save to local folder or S3
python main.py record
```

## Use Cases

- Load testing of message consumers or services
- Simulating real-time systems
- Capturing traffic for debugging or replay

## TODO

- Add full support for reading from and writing to S3 & Redis
- Add serialization/deserialization support for messages (e.g., JSON, Avro, Protobuf)
