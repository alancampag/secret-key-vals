import json
import uuid
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generic, MutableMapping, TypeVar


class Status(Enum):
    Ok = 0
    Err = 1


RT = TypeVar("RT")


class Result(Generic[RT]):
    def __init__(self, status: Status, data: RT) -> None:
        self.status = status
        self.data = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Result):
            return NotImplemented
        return self.status == other.status and self.data == other.data


KT = TypeVar("KT")
VT = TypeVar("VT")


class PersistentDict(MutableMapping[KT, VT]):
    def __init__(
        self,
        *args,
        file: str = f"/tmp/{uuid.uuid4()}",
        **kwargs,
    ) -> None:

        self._file = Path(file)

        if not self._file.exists():
            self._file.write_text("{}")

        self.update(dict(*args, **kwargs))

    def _load(self) -> Dict[KT, VT]:
        return json.loads(self._file.read_text())

    def _save(self, dct: Dict[KT, VT]) -> None:
        self._file.write_text(json.dumps(dct))

    def update(self, *args, **kwargs) -> None:
        dct = self._load()
        dct.update(dict(*args, **kwargs))
        self._save(dct)

    def __getitem__(self, key: KT) -> VT:
        dct = self._load()
        return dct[key]

    def __setitem__(self, key: KT, value: VT) -> None:
        dct = self._load()
        dct[key] = value
        self._save(dct)

    def __delitem__(self, key: KT) -> None:
        dct = self._load()
        del dct[key]
        self._save(dct)

    def __iter__(self):
        dct = self._load()
        return iter(dct)

    def __len__(self) -> int:
        dct = self._load()
        return len(dct)

    def __str__(self) -> str:
        dct = self._load()
        return str(dct)

    def __repr__(self) -> str:
        dct = self._load()
        return repr(dct)
