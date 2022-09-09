from __future__ import annotations

import base64
from typing import Any, Optional, cast

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from secretkv import config


class MissingCipherKeyException(Exception):
    ...


class InvalidKeyException(Exception):
    ...


class EncryptedStr:
    def __init__(self, ciphertext: str) -> None:
        self._ciphertext = ciphertext

    def __str__(self) -> str:
        return self._ciphertext

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EncryptedStr):
            return NotImplemented
        return self._ciphertext == other._ciphertext


class Crypto:
    def __init__(self) -> None:
        self._seed: Optional[bytes] = None
        self._cipher: Optional[Fernet] = None

    def configure(self, password: str) -> None:
        self._seed = self._digest(config.SEED or password)

        key = self._derive_key_from_password(password)
        self._cipher = Fernet(key)

    def encrypt(self, msg: str, deterministic: bool = False) -> EncryptedStr:
        if not self._cipher:
            raise MissingCipherKeyException("Cipher not configured")

        try:
            if not deterministic:
                return EncryptedStr(self._cipher.encrypt(msg.encode()).decode())

            return EncryptedStr(
                self._cipher._encrypt_from_parts(
                    msg.encode(),
                    len(msg),
                    cast(bytes, self._seed)[16:],
                ).decode()
            )
        except InvalidToken:
            raise InvalidKeyException("Invalid key")

    def decrypt(self, msg: EncryptedStr) -> str:
        if not self._cipher:
            raise MissingCipherKeyException("Cipher not configured")

        try:
            return self._cipher.decrypt(str(msg).encode()).decode()
        except InvalidToken:
            raise InvalidKeyException("Invalid key")

    def _derive_key_from_password(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=cast(bytes, self._seed)[:16],
            iterations=390000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _digest(self, msg: str) -> bytes:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(msg.encode())
        return digest.finalize()
