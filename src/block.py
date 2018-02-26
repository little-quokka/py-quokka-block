import datetime

from abstractblock import AbstractBlock


class Block(AbstractBlock):
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

    @property
    def data_hash(self):
        return self._data_hash

    def __init__(self, previous_hash, index, data):
        # previous block
        self._previous_hash = previous_hash

        # current block
        self._index = index
        self._timestamp = datetime.datetime.utcnow()
        self._data = data
        self._data_hash = self._data.hash
        self._hash = self._hash()
