import abc

from cuponazo.domain import ticket


class Error(Exception):
    """Raised whenever `ResultsFetcher` encountered an issue to fecth juegosonce results."""

    pass


class Interface(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def fetch_cuponazo(self) -> list[ticket.Cuponazo]:
        raise NotImplementedError
