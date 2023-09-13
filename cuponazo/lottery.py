import re


class InvalidTicketFormatError(Exception):
    pass


class CuponazoTicket:
    def __init__(self, number: str, serie: str) -> None:
        number_regex = r"^[0-9]{5}$"
        serie_regex = r"^[0-9]{3}$"

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
    def __init__(self, result: CuponazoTicket) -> None:
        self.result = result

    def check_ticket(self, ticket: CuponazoTicket) -> None:
        pass
