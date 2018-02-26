import hashlib
import uuid

from textdata import TextData


class TextDataV1(TextData):
    @property
    def type(self):
        return self._type

    @property
    def version(self):
        return self._version

    @property
    def nonce(self):
        return self._nonce

    @property
    def data(self):
        return self._data

    @property
    def hash(self):
        return self._root_hash

    def __init__(self, data):
        self._type = "TextData"
        self._version = 1
        self._nonce = uuid.uuid4().hex
        self._data = data
        self._root_hash = self._hash()

    def _hash(self):
        encoding = 'utf-8'
        sha256 = hashlib.sha256()
        sha256.update(str(self.nonce).encode(encoding))
        sha256.update(str(self.data).encode(encoding))
        return sha256.hexdigest()

    def json_dict(self):
        return {
            "type": self.type,
            "version": self.version,
            "nonce": self.nonce,
            "data": self.data,
            "hash": self.hash
        }