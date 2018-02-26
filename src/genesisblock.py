import datetime

from abstractblock import AbstractBlock
from textdatav1 import TextDataV1


class GenesisBlock(AbstractBlock):
    @property
    def id(self):
        return self._index

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def data(self):
        return self._data

    @property
    def previous_hash(self):
        return self._previous_hash

    @property
    def hash(self):
        return self._hash

    def __init__(self):
        genesis_index = 0
        self._index = genesis_index
        self._previous_hash = genesis_index
        self._timestamp = datetime.datetime.utcnow()
        self._data = TextDataV1("Genesis Block")
        self._hash = self._hash()
