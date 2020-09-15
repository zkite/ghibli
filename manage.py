import sys
import argparse

from service.app import app
from common.logger import logger


def runserver(host, port):
    app.run(host=host, port=port)


def parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest="command")
    sparser = subparsers.add_parser(runserver.__name__, add_help=False, help="Start server")
    sparser.add_argument("-h", "--host", dest="host", default="0.0.0.0", type=str, help="Host address")
    sparser.add_argument("-p", "--port", dest="port", default=5000, type=int, help="Host post")

    return parser.parse_args(args=args)


def main(args=None):
    parsed_args = parse_args(args or sys.argv[1:])
    runserver(parsed_args.host, parsed_args.port)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Service is going to shutdown. Error message: {}".format(e))
        exit(1)
    finally:
        logger.error("Service stopped.")
