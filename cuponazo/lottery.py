import re


class InvalidTicketFormatError(Exception):
    """Raised when tried to create new `CuponazoTicket` with incorrect format parameters."""

    pass


class CuponazoTicket:
    """Represents a ticket of Cuponazo lottery.

    Parameters
    ----------
    `number` (`str`)
        A string of 5 numbers, represents the main extractions of the lottery.

    `serie` (`str`)
        A string of 3 numbers, represent the extra extraction required for the main prize.

    Raises
    ------
    `InvalidTicketFormatError`
        If the parameters doesn't fit the specifications.
    """

    number_length = 5
    serie_length = 3

    def __init__(self, number: str, serie: str) -> None:
        number_regex = r"^[0-9]{%s}$" % self.number_length
        serie_regex = r"^[0-9]{%s}$" % self.serie_length

        if not re.match(number_regex, number):
            raise InvalidTicketFormatError(
                f"Number '{number}' has an invalid format. Number should match r'{number_regex}' regex."
            )
        self.__number = number

        if not re.match(serie_regex, serie):
            raise InvalidTicketFormatError(
                f"Serie '{serie}' has an invalid format. Serie should match r'{serie_regex}' regex."
            )
        self.__serie = serie

    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.serie == __value.serie

    @property
    def number(self) -> str:
        return self.__number

    @property
    def serie(self) -> str:
        return self.__serie


class TicketChecker:
    """Class resposible to check tickets against the lottery `result`. It implements the `check_ticket` method that would
    check the prize level of the provided `ticket` against the `result`.

    Parameters
    ----------
    `result` (`CuponazoTicket`)
        The result of the lottery that we want to check tickets against it.
    """

    def __init__(self, result: CuponazoTicket) -> None:
        self.result = result

    def check_ticket(self, ticket: CuponazoTicket) -> int:
        """Returns the prize level of the ticket, that it would be the number of coincident numbers between `ticket`
        and `self.result`. It'll return a 6 (5+1) if we have 5 coincidences and also the serie coincides.

        Parameters
        ----------
        `ticket` (`CuponazoTicket`)
            A ticket we want to check the prize level of it.

        Returns
        -------
        `int`
            The prize level, it'll range from 0 to 6 (6 being 5 coincidences and the same serie)
        """
        if ticket.number == self.result.number:
            if ticket.serie == self.result.serie:
                # Prize to the five numbers and serie
                return CuponazoTicket.number_length + 1
            else:
                # Prize to five numbers but not serie
                return CuponazoTicket.number_length

        # In case we don't have the 5 numbers, we'll check how many numbers we coincide (forward and reverse)
        coincidences_forward = self.__get_coincidences_from_number(
            self.result.number,
            ticket.number,
        )
        coincidences_reverse = self.__get_coincidences_from_number(
            self.__reverse_str(self.result.number),
            self.__reverse_str(ticket.number),
        )

        # We'll keep with the biggest ammount of coincidences
        return max(coincidences_forward, coincidences_reverse)

    def __get_coincidences_from_number(self, result: str, ticket: str) -> int:
        """Returns the number of coincident numbers between `result` and `ticket` (going from right to left).
        It assumes that length of `result` and `ticket` is the same, but that it's already checked when
        called from `check_ticket`.

        Parameters
        ----------
        `result` (`str`)
            The numbers of the result of the lottery.

        `ticket` (`str`)
            The numbers of the ticket we want to check.

        Returns
        -------
        `int`
            The number of coincidences (from right to left) of two numbers.
        """
        for i, r, t in zip(
            range(len(result)),
            list(result),
            list(ticket),
        ):
            if r != t:
                break

        return i

    def __reverse_str(self, s: str) -> str:
        """Returns the string reversed: 'asdf' -> 'fdsa'"""
        return s[::-1]
