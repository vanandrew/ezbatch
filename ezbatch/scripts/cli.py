from argparse import ArgumentParser

from ezbatch._version import version


def ezbatch_cli():
    """CLI function for EZBatch"""
    parser = ArgumentParser(description=f"EZBatch CLI, Version {version}")
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"EZBatch CLI, Version {version}",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    init_command = subparsers.add_parser(
        "init", help="Initialize EZBatch configuration"
    )

    # parse the arguments
    args = parser.parse_args()

    # parse the command
    if args.command == "init":
        print("Initializing EZBatch configuration")
