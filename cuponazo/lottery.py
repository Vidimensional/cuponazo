class CuponazoTicket:
    def __init__(self, number: str, serie: str) -> None:
        self.number = number
        self.serie = serie

    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.serie == __value.serie
