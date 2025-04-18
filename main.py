from src.initializer import Initializer


def main():
    initializer = Initializer()
    facade = initializer.initialize()
    facade.start()


if __name__ == '__main__':
    main()