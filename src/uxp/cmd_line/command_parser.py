import argparse
from uxp.cmd_line.commands import CliNewArgs, CliListArgs, CliDeleteArgs, CliEditArgs, CliShowArgs, CliCopyArgs


def add_common_args(sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument('-d', '--date', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')
    sub_parser.add_argument('-n', '--now', type=int, required=False, help='Number of days w.r.t today (can be negative for past days).')
    return sub_parser


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
    add_common_args(new_daily)

    edit = sub_parser.add_parser('edit')
    add_common_args(edit)

    delete = sub_parser.add_parser('delete')
    add_common_args(delete)

    show = sub_parser.add_parser('show')
    add_common_args(show)

    list_parser = sub_parser.add_parser('list')
    list_parser = add_common_args(list_parser)
    list_parser.add_argument('-b', type=int, default=10, required=False,
                             help='Number of days to list before stated date.')
    list_parser.add_argument('-a', type=int, default=10, required=False,
                             help='Number of days to list after stated date.')
    list_parser.add_argument('-A', '--all', default=False, action='store_true',
                             help='Whether to display everything or not')

    report = sub_parser.add_parser('report')
    add_common_args(report)

    copy_parser = sub_parser.add_parser('copy')
    copy_parser.add_argument('-d1', '--date_1', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')
    copy_parser.add_argument('-d2', '--date_2', type=str, default=None, required=False, help='Date of the daily plan, with format="YYYY-MM-DD"')

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
    elif ns.command == 'show':
        return CliShowArgs.from_namespace(ns)
    elif ns.command == 'copy':
        return CliCopyArgs.from_namespace(ns)
    elif ns.command == 'report':
        raise NotImplementedError('report is not implemented yet')
    else:
        raise Exception('Unknown command: {}.\navailable commands: new, edit, report')
