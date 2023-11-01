import re


class InvalidFormatError(Exception):
    """Raised when tried to create new `ticket.Cuponazo` with incorrect format parameters."""

    pass


class Cuponazo:
    """Represents a ticket of Cuponazo lottery.

    Parameters
    ----------
    `number` (`str`)
        A string of 5 numbers, represents the main extractions of the lottery.

    `serie` (`str`)
        A string of 3 numbers, represent the extra extraction required for the main prize.

    Raises
    ------
    `InvalidFormatError`
        If the parameters doesn't fit the specifications.
    """

    number_length = 5
    serie_length = 3

    def __init__(self, number: str, serie: str) -> None:
        number_regex = r"^[0-9]{%s}$" % self.number_length
        serie_regex = r"^[0-9]{%s}$" % self.serie_length

        if not re.match(number_regex, number):
            raise InvalidFormatError(
                f"Number '{number}' has an invalid format. Number should match r'{number_regex}' regex."
            )
        self.__number = number

        if not re.match(serie_regex, serie):
            raise InvalidFormatError(
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
