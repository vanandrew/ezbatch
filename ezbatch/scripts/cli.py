from argparse import ArgumentParser
from typing import Any

from ezbatch._version import version
from ezbatch.compute_environment import (
    create_compute_environment,
    delete_compute_environment,
    list_compute_environments,
    toggle_compute_environment,
)


def sanitize_args(args: dict[str, Any]) -> dict[str, Any]:
    """Remove command, subcommand, and None values from a args dictionary."""
    del args["command"]
    del args["subcommand"]
    return {k: v for k, v in args.items() if v is not None}


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

    # compute environment command
    compute_environment_command = subparsers.add_parser("compute-environment", help="Compute Environment Management")
    compute_environment_subcommands = compute_environment_command.add_subparsers(dest="subcommand", help="Subcommands")

    # create compute environment
    create = compute_environment_subcommands.add_parser("create", help="Create a new Compute Environment")
    create.add_argument("--name", type=str, required=True, help="The name of the Compute Environment")
    create.add_argument("--service-role", type=str, default=None, help="The ARN of the service role")
    create.add_argument(
        "--type", type=str, default="FARGATE", choices=["FARGATE", "EC2"], help="The type of the Compute Environment"
    )
    create.add_argument("--max-vcpus", type=int, default=256, help="The maximum number of vCPUs")
    create.add_argument("--subnets", type=str, nargs="+", default=None, help="The subnets to use")
    create.add_argument("--security-group-ids", type=str, nargs="+", default=None, help="The security group IDs to use")
    create.add_argument("--tags", type=str, nargs="+", default=[], help="The tags to apply, in the format key=value")

    # list compute environments
    list = compute_environment_subcommands.add_parser("list", help="List all Compute Environments")

    # toggle compute environment
    toggle = compute_environment_subcommands.add_parser("toggle", help="Toggle the state of a Compute Environment")
    toggle.add_argument("--name", type=str, required=True, help="The name or ARN of the Compute Environment")

    # delete compute environment
    delete = compute_environment_subcommands.add_parser("delete", help="Delete a Compute Environment")
    delete.add_argument("--name", type=str, required=True, help="The name or ARN of the Compute Environment")

    # parse the arguments
    args = parser.parse_args()

    # handle the command
    if args.command == "compute-environment":
        if args.subcommand == "create":
            args_dict = vars(args)
            args_dict["tags"] = {tag.split("=")[0]: tag.split("=")[1] for tag in args_dict["tags"]}
            args_dict = sanitize_args(args_dict)
            create_compute_environment(**args_dict)
        elif args.subcommand == "list":
            list_compute_environments()
        elif args.subcommand == "toggle":
            toggle_compute_environment(args.name)
        elif args.subcommand == "delete":
            delete_compute_environment(args.name)
