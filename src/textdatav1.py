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
        return self._hash

    def __init__(self, data):
        # specific to TextDataV1
        if isinstance(data, str):
            self._data = data
        else:
            raise Exception("Provided data is not a string.")

        # for every AbstractDataPackage
        self._type = "TextData"
        self._version = 1
        self._nonce = uuid.uuid4().hex

        self._hash = self._hash()

    def json_dict(self):
        return {
            "type": self.type,
            "version": self.version,
            "nonce": self.nonce,
            "data": self.data,
            "hash": self.hash
        }