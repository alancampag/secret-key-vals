from __future__ import annotations

from typing import NamedTuple

from secretkv.crypto import EncryptedStr


class Secret(NamedTuple):
    key: EncryptedStr
    val: EncryptedStr
