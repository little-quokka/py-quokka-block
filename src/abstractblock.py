import abc
import hashlib


class AbstractBlock(abc.ABC):
    @property
    @abc.abstractmethod
    def index(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def timestamp(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def data(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def previous_hash(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def hash(self):
        raise NotImplementedError()

    def _hash(self):
        encoding = 'utf-8'
        sha256 = hashlib.sha256()
        sha256.update(str(self.index).encode(encoding))
        sha256.update(str(self.timestamp).encode(encoding))
        sha256.update(str(self.data.hash).encode(encoding))
        sha256.update(str(self.previous_hash).encode(encoding))
        return sha256.hexdigest()

    def show(self):        
        print('{:>15s}: {}'.format('Block index', self.index))
        print('{:>15s}: {}'.format('Timestamp', self.timestamp))
        print('{:>15s}: {}'.format('Data hash', self.data.hash))
        print('{:>15s}: {}'.format('Previous hash', self.previous_hash))
        print('{:>15s}: {}'.format('Hash', self.hash))
        print()

    def json_dict(self):
        return {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data.json_dict(),
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }
