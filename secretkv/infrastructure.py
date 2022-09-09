from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from secretkv.application import Repository
from secretkv.crypto import EncryptedStr
from secretkv.domain import Secret
from secretkv.utils import PersistentDict as PDict

SecretsHistory = List[Tuple[str, int]]
SecretsMapping = Union[
    Dict[str, SecretsHistory],
    PDict[str, SecretsHistory],
]


class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self._secrets: SecretsMapping = {}

    def list_latest_version(self) -> List[Secret]:
        secrets = []
        for key, values in self._secrets.items():
            values.sort(key=lambda x: x[1])

            secrets.append(
                Secret(
                    EncryptedStr(key),
                    EncryptedStr(values[-1][0]),
                )
            )

        return secrets

    def retrieve_by_key(self, key: EncryptedStr) -> Optional[Secret]:
        if not (history := self._retrieve_history_by_key(key)):
            return None

        val, _ = history[-1]
        secret = Secret(key, EncryptedStr(val))
        return secret

    def retireve_history_from_key(self, key: EncryptedStr) -> List[Secret]:
        return [
            Secret(key, EncryptedStr(secret[0]))
            for secret in self._retrieve_history_by_key(key)
        ]

    def save(self, secret: Secret) -> bool:
        latest = self._find_latest_version_number(secret.key)
        self._secrets[str(secret.key)] = self._secrets.get(str(secret.key), []) + [
            (
                str(secret.val),
                latest + 1,
            )
        ]
        return True

    def is_empty(self) -> bool:
        return len(self._secrets) == 0

    def _retrieve_history_by_key(self, key: EncryptedStr) -> SecretsHistory:
        values = [(val, version) for val, version in self._secrets.get(str(key), [])]
        values.sort(key=lambda x: x[1])
        return values

    def _find_latest_version_number(self, key: EncryptedStr) -> int:
        if history := self._retrieve_history_by_key(key):
            return history[-1][1]
        return 0


class FileRepository(Repository):
    def __init__(self, file: str = "secrets.json") -> None:
        self._implementation = InMemoryRepository()
        self._implementation._secrets = PDict(file=file)
        self._file = Path(file)

    def list_latest_version(self) -> List[Secret]:
        try:
            return self._implementation.list_latest_version()
        except Exception:
            return []

    def retrieve_by_key(self, key: EncryptedStr) -> Optional[Secret]:
        try:
            return self._implementation.retrieve_by_key(key)
        except Exception:
            return None

    def retireve_history_from_key(self, key: EncryptedStr) -> List[Secret]:
        try:
            return self._implementation.retireve_history_from_key(key)
        except Exception:
            return []

    def save(self, secret: Secret) -> bool:
        try:
            return self._implementation.save(secret)
        except Exception:
            return False

    def is_empty(self) -> bool:
        return len(self._implementation._secrets) == 0

    def clear(self) -> None:
        self._file.unlink()
