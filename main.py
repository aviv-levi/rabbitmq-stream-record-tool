from src.initializer import Initializer


def main():
    initializer = Initializer()
    facade = initializer.initialize()
    facade.start()


if __name__ == '__main__':
    main()
# # import pika
# # import sys
# from app import run
#
# def main():
#     run()
#
#     # print(sys.argv[1])
#
#     # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     # channel = connection.channel()
#     # channel.queue_declare(queue='hello')
#
#     # import yaml
#     #
#     # with open("configuration.yaml") as stream:
#     #     try:
#     #         print(yaml.safe_load(stream))
#     #     except yaml.YAMLError as exc:
#     #         print(exc)
#
#
# if __name__ == '__main__':
#     main()