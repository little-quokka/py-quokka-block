import abc


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
    def data(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def hash(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def json_dict(self):
        raise NotImplementedError