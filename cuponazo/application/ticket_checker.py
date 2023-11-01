from cuponazo.domain import ticket


class TicketChecker:
    """Class resposible to check tickets against the lottery `result`. It implements the `check_ticket` method that would
    check the prize level of the provided `ticket` against the `result`.

    Parameters
    ----------
    `result` (`CuponazoTicket`)
        The result of the lottery that we want to check tickets against it.
    """

    def __init__(self, result: ticket.Cuponazo) -> None:
        self.result = result

    def check_ticket(self, t: ticket.Cuponazo) -> int:
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
        if t.number == self.result.number:
            if t.serie == self.result.serie:
                # Prize to the five numbers and serie
                return ticket.Cuponazo.number_length + 1
            else:
                # Prize to five numbers but not serie
                return ticket.Cuponazo.number_length

        # In case we don't have the 5 numbers, we'll check how many numbers we coincide (forward and reverse)
        coincidences_forward = self.__get_coincidences_from_number(
            self.result.number,
            t.number,
        )
        coincidences_reverse = self.__get_coincidences_from_number(
            self.__reverse_str(self.result.number),
            self.__reverse_str(t.number),
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
