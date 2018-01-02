import abc
import hashlib


class AbstractDataPackage(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def version(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def nonce(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def data(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def hash(self):
        raise NotImplementedError()

    def _hash(self):
        encoding = 'utf-8'
        sha256 = hashlib.sha256()
        sha256.update(str(self.nonce).encode(encoding))
        sha256.update(str(self.data).encode(encoding))
        return sha256.hexdigest()

    @abc.abstractmethod
    def json_dict(self):
        raise NotImplementedError