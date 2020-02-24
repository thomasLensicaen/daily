import sys
from common import DEFAULT_CONFIG_PATH
from config import Config
from uxp.cmd_line.command_parser import parse_args


def main():
    command = parse_args(sys.argv)
    config = Config.from_file(DEFAULT_CONFIG_PATH)
    command.apply(config)


if __name__ == '__main__':
    main()
