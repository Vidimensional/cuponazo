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

        i_forward = self.__get_prize_from_number(self.result.number, ticket.number)
        i_reverse = self.__get_prize_from_number(
            self.result.number[::-1],
            ticket.number[::-1],
        )

        return max(i_forward, i_reverse)

    def __get_prize_from_number(self, result_number: str, ticket_number: str) -> int:
        for i in range(CuponazoTicket.number_length):
            result_nimber = result_number[i]
            nimber = ticket_number[i]
            if result_nimber != nimber:
                break
        return i
