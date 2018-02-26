import json
import uuid

from transactiondata import TransactionData


class TransactionDataV1(TransactionData):
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
    def hash(self):
        return self._hash

    @property
    def data(self):
        return self._data

    def __init__(self, data):
        self._type = "TransactionData"
        self._version = 1
        self._nonce = uuid.uuid4().hex
        self._data = data
        self._hash = self._hash()

    def json_dict(self):
        return {
            "type": self.type,
            "version": self.version,
            "nonce": self.nonce,
            "data": json.dumps(self.data),
            "hash": self.hash
        }