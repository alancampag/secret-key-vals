from argparse import ArgumentParser
from typing import Optional, Sequence

from secretkv import SecretKV
from secretkv.cli import Cli
from secretkv.crypto import Crypto
from secretkv.infrastructure import FileRepository


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(prog="skv")
    cli = Cli(parser)

    command = cli.parse(argv)

    app = SecretKV(
        FileRepository(),
        Crypto(),
    )

    if output := command.execute(dependencies={"app": app}):
        Cli.show_output(output)

    return 0


if __name__ == "__main__":
    exit(main())
