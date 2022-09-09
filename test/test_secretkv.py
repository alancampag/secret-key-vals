import pytest
import secretkv
from secretkv.utils import Status
from secretkv import config


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get(skv, password):
    result = secretkv.get(skv, "key1", password)
    assert result.status == Status.Ok and result.data == {"values": ["val1b"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_history(skv, password):
    result = secretkv.get(skv, "key1", password, history=True)
    assert result.status == Status.Ok and result.data == {"values": ["val1a", "val1b"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_missing_key(skv, password):
    result = secretkv.get(skv, "key", password)
    assert result.status == Status.Err and result.data == {"values": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_empty_key(skv, password):
    result = secretkv.get(skv, "", password)
    assert result.status == Status.Err and result.data == {"values": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_deleted_key(skv, password):
    result = secretkv.get(skv, "key0", password)
    assert result.status == Status.Err and result.data == {"values": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_with_wrong_password(skv, wrong_password):
    result = secretkv.get(skv, "key1", wrong_password)
    assert result.status == Status.Err and result.data == {"values": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_get_tag_key(skv, password):
    result = secretkv.get(skv, config.TAG, password)
    assert result.status == Status.Err and result.data == {"values": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set(skv, password):
    result = secretkv.set(skv, "key3", "val3", password)
    assert result.status == Status.Ok and result.data == {"keys": ["key3"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_empty_key(skv, password):
    result = secretkv.set(skv, "", "val3", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_empty_val(skv, password):
    result = secretkv.set(skv, "key3", "", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_with_wrong_password(skv, wrong_password):
    result = secretkv.set(skv, "key1", "val1", wrong_password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_tag_key(skv, password):
    result = secretkv.set(skv, config.TAG, "val0", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list(skv, password):
    result = secretkv.list(skv, password)
    assert result.status == Status.Ok and result.data == {"keys": ["key1", "key2"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list_including_deleted(skv, password):
    result = secretkv.list(skv, password, all=True)
    assert result.status == Status.Ok and result.data == {"keys": ["key0", "key1", "key2"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list_with_wrong_password(skv, wrong_password):
    result = secretkv.list(skv, wrong_password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list_including_deleted_with_wrong_password(skv, wrong_password):
    result = secretkv.list(skv, wrong_password, all=True)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list_doesnt_include_tag_key(skv, password):
    result = secretkv.list(skv, password)
    assert result.status == Status.Ok and config.TAG not in result.data.get("keys")


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_list_including_deleted_doesnt_include_tag_key(skv, password):
    result = secretkv.list(skv, password)
    assert result.status == Status.Ok and config.TAG not in result.data.get("keys")


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete(skv, password):
    result = secretkv.delete(skv, "key2", password)
    assert result.status == Status.Ok and result.data == {"keys": ["key2"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_missing_key(skv, password):
    result = secretkv.delete(skv, "key", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_empty_key(skv, password):
    result = secretkv.delete(skv, "", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_already_deleted_key(skv, password):
    result = secretkv.delete(skv, "key0", password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_with_wrong_password(skv, wrong_password):
    result = secretkv.delete(skv, "key1", wrong_password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_tag_key(skv, password):
    result = secretkv.delete(skv, config.TAG, password)
    assert result.status == Status.Err and result.data == {"keys": []}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_and_then_get(skv, password):
    secretkv.set(skv, "key3", "val3", password)

    result = secretkv.get(skv, "key3", password)
    assert result.data == {"values": ["val3"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_set_and_then_list(skv, password):
    secretkv.set(skv, "key3", "val3", password)
    result = secretkv.list(skv, password)
    assert result.data == {"keys": ["key1", "key2", "key3"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_and_then_list(skv, password):
    secretkv.delete(skv, "key2", password)

    result = secretkv.list(skv, password)
    assert result.data == {"keys": ["key1"]}


@pytest.mark.parametrize("skv", ["in_memory_repository", "file_repository"], indirect=True)
def test_delete_and_then_list_including_deleted(skv, password):
    secretkv.delete(skv, "key2", password)
    result = secretkv.list(skv, password, all=True)
    assert result.data == {"keys": ["key0", "key1", "key2"]}
