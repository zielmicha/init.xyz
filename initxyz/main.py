import sys
import argparse

from initxyz import commands

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    for command in commands.commands:
        subparser = subparsers.add_parser(command.name)
        subparser.set_defaults(command=command)
        command.make_parser(subparser)

    ns = parser.parse_args()
    if not hasattr(ns, 'command'):
        parser.print_usage()
        sys.exit(1)

    ns.command.run(ns)
