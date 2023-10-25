import re


class InvalidTicketFormatError(Exception):
    pass


class CuponazoTicket:
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
    def __init__(self, result: CuponazoTicket) -> None:
        self.result = result

    def check_ticket(self, ticket: CuponazoTicket) -> int:
        if ticket.number == self.result.number:
            if ticket.serie == self.result.serie:
                return CuponazoTicket.number_length + 1
            else:
                return CuponazoTicket.number_length

        coincidences_forward = self.__get_coincidences_from_number(
            self.result.number,
            ticket.number,
        )
        coincidences_reverse = self.__get_coincidences_from_number(
            self.__reverse_str(self.result.number),
            self.__reverse_str(ticket.number),
        )

        return max(coincidences_forward, coincidences_reverse)

    def __get_coincidences_from_number(self, result: str, ticket: str) -> int:
        for i, r, t in zip(
            range(len(result)),
            list(result),
            list(ticket),
        ):
            if r != t:
                break

        return i

    def __reverse_str(self, s: str) -> str:
        return s[::-1]
