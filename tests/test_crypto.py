import pytest

from secretkv.crypto import MissingCipherKeyException


def test_encrypt_deterministic(crypto, plaintext, ciphertext):
    result = crypto.encrypt(plaintext, deterministic=True)
    assert result == ciphertext


def test_decrypt(crypto, plaintext, ciphertext):
    result = crypto.decrypt(ciphertext)
    assert result == plaintext


def test_encrypt_then_decrypt(crypto, plaintext):
    result = crypto.decrypt(crypto.encrypt(plaintext))
    assert result == plaintext


def test_uncofigured_crypto_on_encrypt(unconfigured_crypto, plaintext):
    with pytest.raises(MissingCipherKeyException):
        unconfigured_crypto.encrypt(plaintext)


def test_uncofigured_crypto_on_decrypt(unconfigured_crypto, ciphertext):
    with pytest.raises(MissingCipherKeyException):
        unconfigured_crypto.decrypt(ciphertext)
