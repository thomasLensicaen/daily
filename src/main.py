import sys
from common import DEFAULT_CONFIG_PATH
import argparse
from config import Config
from functionalities.create_new_daily import CliNewArgs
from functionalities.edit_daily import CliEditArgs
from functionalities.delete_daily import CliDeleteArgs


def arg_interpreter(args) -> argparse.Namespace:
    """Parses arguments from command line.

    Args:
        args: List of command line argument.

    Returns:
        Parsed arguments as a argparse.Namespace.
        """
    parser = argparse.ArgumentParser(
        description='Script that is used to perform data pre-processing over fusion-risk raw data')

    sub_parser = parser.add_subparsers(dest='command')
    new_daily = sub_parser.add_parser('new')
    new_daily.add_argument('-d', '--date', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')
    new_daily.add_argument('-n', '--now', type=int, required=False, help='Number of days w.r.t today (can be negative for past days).')

    edit = sub_parser.add_parser('edit')
    edit.add_argument('-d', '--date', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')
    edit.add_argument('-n', '--now', type=int, required=False, help='Number of days w.r.t today (can be negative for past days).')

    delete = sub_parser.add_parser('delete')
    delete.add_argument('-d', '--date', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')
    delete.add_argument('-n', '--now', type=int, required=False, help='Number of days w.r.t today (can be negative for past days).')

    report = sub_parser.add_parser('report')
    parsed = parser.parse_args(args[1:])
    return parsed


def parse_args(args):
    ns: argparse.Namespace = arg_interpreter(args)
    if ns.command == 'new':
        return CliNewArgs.from_namespace(ns)
    elif ns.command == 'edit':
        return CliEditArgs.from_namespace(ns)
    elif ns.command == 'delete':
        return CliDeleteArgs.from_namespace(ns)
    elif ns.command == 'list':
        return CliListArgs.from_namespace(ns)
    elif ns.command == 'report':
        print('report is not implemented yet')
    else:
        raise Exception('Unknown command: {}.\navailable commands: new, edit, report')


def main():
    command = parse_args(sys.argv)
    config = Config.from_file(DEFAULT_CONFIG_PATH)
    command.apply(config)


if __name__ == '__main__':
    main()

