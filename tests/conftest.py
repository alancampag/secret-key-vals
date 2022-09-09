import pytest
from secretkv import config
from secretkv.application import SecretKV
from secretkv.crypto import Crypto, EncryptedStr
from secretkv.domain import Secret
from secretkv.infrastructure import FileRepository, InMemoryRepository


@pytest.fixture(scope="session")
def password():
    return "123456"


@pytest.fixture(scope="session")
def wrong_password():
    return "654321"


@pytest.fixture(scope="session")
def plaintext():
    return "test"


@pytest.fixture(scope="session")
def ciphertext():
    return EncryptedStr(
        "gAAAAAAAAAAEDD9dWoav88oSAgySOtxskhlXiXqjKPp7dxXidYSLdRxGWiJcRygTgp1AQNtESUY1ztX2WE2SBSdOpF1uUJJlsQ=="
    )


@pytest.fixture
def crypto(password, scope="session"):
    crypto = Crypto()
    crypto.configure(password)
    return crypto


@pytest.fixture(scope="session")
def unconfigured_crypto():
    return Crypto()


@pytest.fixture
def in_memory_repository(crypto: Crypto):
    repository = InMemoryRepository()
    repository.save(
        Secret(crypto.encrypt(config.TAG, deterministic=True), crypto.encrypt(config.TAG[::-1]))
    )
    repository.save(Secret(crypto.encrypt("key0", deterministic=True), crypto.encrypt("")))
    repository.save(Secret(crypto.encrypt("key1", deterministic=True), crypto.encrypt("val1a")))
    repository.save(Secret(crypto.encrypt("key1", deterministic=True), crypto.encrypt("val1b")))
    repository.save(Secret(crypto.encrypt("key2", deterministic=True), crypto.encrypt("val2")))
    return repository


@pytest.fixture
def file_repository(crypto: Crypto):
    repository = FileRepository("test.json")
    repository.save(
        Secret(crypto.encrypt(config.TAG, deterministic=True), crypto.encrypt(config.TAG[::-1]))
    )
    repository.save(Secret(crypto.encrypt("key0", deterministic=True), crypto.encrypt("")))
    repository.save(Secret(crypto.encrypt("key1", deterministic=True), crypto.encrypt("val1a")))
    repository.save(Secret(crypto.encrypt("key1", deterministic=True), crypto.encrypt("val1b")))
    repository.save(Secret(crypto.encrypt("key2", deterministic=True), crypto.encrypt("val2")))
    yield repository
    repository.clear()


@pytest.fixture
def skv(crypto, request):
    repository = request.getfixturevalue(request.param)
    return SecretKV(repository, crypto)
