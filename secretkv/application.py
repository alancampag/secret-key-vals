from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from secretkv import config
from secretkv.crypto import Crypto, EncryptedStr
from secretkv.domain import Secret


class Repository(ABC):
    @abstractmethod
    def list_latest_version(self) -> List[Secret]:
        ...

    @abstractmethod
    def retrieve_by_key(self, key: EncryptedStr) -> Optional[Secret]:
        ...

    @abstractmethod
    def retireve_history_from_key(self, key: EncryptedStr) -> List[Secret]:
        ...

    @abstractmethod
    def save(self, secret: Secret) -> bool:
        ...

    def is_empty(self) -> bool:
        ...


class SecretKV:
    def __init__(self, repository: Repository, crypto: Crypto) -> None:
        self._repository = repository
        self._crypto = crypto

    @property
    def crypto(self) -> Crypto:
        return self._crypto

    def verify_password(self) -> bool:
        if self._repository.is_empty():
            self.create_or_append(config.TAG, config.TAG[::-1])
            return True

        return bool(self.get_value_from_key(config.TAG))

    def list_every_key(self, include_deleted: bool) -> List[str]:
        return [
            self._crypto.decrypt(secret.key)
            for secret in self._repository.list_latest_version()
            if self._crypto.decrypt(secret.val) or include_deleted
        ]

    def get_history_from_key(self, key: str) -> List[str]:
        return [
            self._crypto.decrypt(secret.val) for secret in self._find_all_versions(key)
        ]

    def get_value_from_key(self, key: str) -> Optional[str]:
        if secret := self._find_latest_version(key):
            return self._crypto.decrypt(secret.val)
        return None

    def create_or_append(self, key: str, val: str) -> Optional[str]:
        secret = Secret(
            self._crypto.encrypt(key, deterministic=True),
            self._crypto.encrypt(val),
        )
        if self._repository.save(secret):
            return key
        return None

    def mark_as_deleted(self, key: str) -> Optional[str]:
        if secret := self._find_latest_version(key):
            if self._crypto.decrypt(secret.val) != "" and self._repository.save(
                Secret(
                    self._crypto.encrypt(key, deterministic=True),
                    self._crypto.encrypt(""),
                )
            ):
                return key
        return None

    def _find_latest_version(self, key: str) -> Optional[Secret]:
        return self._repository.retrieve_by_key(
            self._crypto.encrypt(key, deterministic=True)
        )

    def _find_all_versions(self, key: str) -> List[Secret]:
        return self._repository.retireve_history_from_key(
            self._crypto.encrypt(key, deterministic=True)
        )
