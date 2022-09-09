from typing import Dict, List, Optional

from secretkv import config
from secretkv.application import SecretKV
from secretkv.utils import Result, Status


def list(
    app: SecretKV,
    password: str,
    all: bool = False,
) -> Result[Dict[str, List[str]]]:
    app.crypto.configure(password)

    if not app.verify_password():
        return Result[Dict[str, List[str]]](Status.Err, {})

    data = {"keys": [k for k in app.list_every_key(all) if k != config.TAG]}
    return Result[Dict[str, List[str]]](Status.Ok, data)


def get(
    app: SecretKV,
    key: str,
    password: str,
    history: bool = False,
) -> Result[Dict[str, List[str]]]:
    app.crypto.configure(password)

    if (
        not key
        or key == config.TAG
        or not app.verify_password()
        or not (
            val := app.get_history_from_key(key)
            if history
            else (lambda x: [x] if x and isinstance(x, str) else [])(
                app.get_value_from_key(key)
            )
        )
    ):
        return Result[Dict[str, List[str]]](Status.Err, {})

    return Result[Dict[str, List[str]]](Status.Ok, {"values": val[::-1]})


def set(
    app: SecretKV,
    key: str,
    val: str,
    password: str,
) -> Result[Dict[str, List[str]]]:
    app.crypto.configure(password)

    if (
        not key
        or key == config.TAG
        or not val
        or not app.verify_password()
        or not (app.create_or_append(key, val))
    ):
        return Result[Dict[str, List[str]]](Status.Err, {})

    return Result[Dict[str, List[str]]](Status.Ok, {})


def delete(
    app: SecretKV,
    key: str,
    password: str,
) -> Result[Dict[str, List[str]]]:
    app.crypto.configure(password)

    if (
        not key
        or key == config.TAG
        or not app.verify_password()
        or not (app.mark_as_deleted(key))
    ):

        return Result[Dict[str, List[str]]](Status.Err, {})

    return Result[Dict[str, List[str]]](Status.Ok, {})


def dump(
    app: SecretKV,
    password: str,
    plaintext: bool = False,
    output: Optional[str] = None,
) -> None:
    app.crypto.configure(password)
    ...


def restore(
    app: SecretKV,
    password: str,
    replace: bool = False,
) -> None:
    app.crypto.configure(password)
    ...
