import abc

from cuponazo.domain import ticket


class Error(Exception):
    """Raised whenever `TicketRepository` encountered an issue to read/write tickets on the DB."""

    pass


class Interface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_tickets_by_id(self, ticket_id: str) -> list[ticket.Cuponazo]:
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_ticket_to_id(self, ticket_id: str, ticket: ticket.Cuponazo) -> None:
        raise NotImplementedError
