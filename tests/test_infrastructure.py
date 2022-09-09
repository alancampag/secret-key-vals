from pathlib import Path
from secretkv.infrastructure import FileRepository


def test_file_is_creted():
    path = "~/.skv/test.json"
    FileRepository(path)

    path_obj = Path(path).expanduser()
    assert path_obj.is_file()
    path_obj.unlink()
