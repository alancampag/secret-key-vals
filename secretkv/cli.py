from __future__ import annotations

import getpass
import json
from argparse import ArgumentParser
from typing import Any, Dict, List, Optional, Sequence

import secretkv
from secretkv import config
from secretkv.utils import Result, Status

CommandOutput = Dict[str, List[str]]


class InvalidCommandException(Exception):
    ...


def get_master_password(command: Command) -> str:
    return command.kwargs.pop("masterpass", "") or config.MASTERPASS or Cli.prompt_for_password()


class Command:
    def __init__(self, func_name: str, kwargs: Dict[str, str]) -> None:
        self.func_name = func_name
        self.kwargs = kwargs

    def execute(self, dependencies: Dict[str, Any]) -> Optional[CommandOutput]:
        func = getattr(secretkv, self.func_name, None)
        if not func or not callable(func):
            return {"message": [f"Command {self.func_name} doesn't exist"]}

        self.kwargs["password"] = get_master_password(self)

        self.kwargs.update(dependencies)
        response: Result[CommandOutput] = func(**self.kwargs)
        if response.status == Status.Ok:
            if output := response.data:
                return output
            return None

        return {"message": ["Something went wrong!"]}


class Cli:
    def __init__(self, parser: ArgumentParser) -> None:

        subparsers = parser.add_subparsers(
            title="subcommmands", dest="func", metavar="", required=True
        )

        list_subcommand = subparsers.add_parser(
            "list",
            help="list every key",
        )
        list_subcommand.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="include deleted key",
        )
        list_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        get_subcommand = subparsers.add_parser(
            "get",
            help="get secret",
        )
        get_subcommand.add_argument(
            "key",
            help="key name",
        )
        get_subcommand.add_argument(
            "-H",
            "--history",
            action="store_true",
            help="get entire history of values",
        )
        get_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        set_subcommand = subparsers.add_parser(
            "set",
            help="set secret",
        )
        set_subcommand.add_argument(
            "key",
            help="key name",
        )
        set_subcommand.add_argument(
            "val",
            help="secret value",
        )
        set_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        del_subcommand = subparsers.add_parser(
            "del",
            help="delete secret",
        )
        del_subcommand.add_argument(
            "key",
            help="key name",
        )
        del_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        dump_subcommand = subparsers.add_parser(
            "dump",
            help="dump all secrets",
        )
        dump_subcommand.add_argument(
            "--plaintext",
            action="store_true",
            help="dump secrets in plaintext",
        )
        dump_subcommand.add_argument(
            "-o",
            "--output",
            help="write dump to file",
        )
        dump_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        restore_subcommand = subparsers.add_parser(
            "restore",
            help="restore from dump file",
        )
        restore_subcommand.add_argument(
            "file",
            help="dump file",
        )
        restore_subcommand.add_argument(
            "--replace",
            help="drop full database before restore",
        )
        restore_subcommand.add_argument(
            "-p",
            "--masterpass",
            help="master password",
        )

        self._parser = parser

    def parse(self, argv: Optional[Sequence[str]]) -> Command:
        kwargs = vars(self._parser.parse_args(argv))
        func_name = kwargs.pop("func")
        return Command(func_name, kwargs)

    @staticmethod
    def prompt_for_password() -> str:
        return getpass.getpass()

    @staticmethod
    def show_output(results: CommandOutput) -> None:
        if "values" in results:
            results = [v if v != "" else None for v in results["values"]]
        print(json.dumps(results, indent=2))
