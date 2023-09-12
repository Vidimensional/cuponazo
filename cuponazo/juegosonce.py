import logging
import requests
from requests.exceptions import RequestException
import xmltodict

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}
url = "https://www.juegosonce.es/rss/sorteos2.xml"


class CuponazoResult:
    def __init__(self, number: str, serie: str):
        self.number = number
        self.serie = serie

    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.serie == __value.serie


class ResultsFetcher:
    def __init__(self, url: str, http: requests.Session) -> None:
        self.url = url
        self.http = http

    def fetch_cuponazo(self) -> list[CuponazoResult]:
        return [
            CuponazoResult(item["numero"], item["serie"])
            for item in self.__fetch("cuponazo")
        ]

    def __fetch(self, lottery_type: str) -> list[dict[str, str]]:
        try:
            resp = self.http.get(self.url)
        except RequestException as err:
            logging.error("Problem fetching juegosonce results: %s", str(err))
            raise

        return [
            item
            for item in self.__get_items_from_response(resp.text)
            if item["tipo"] == lottery_names[lottery_type]
        ]

    def __get_items_from_response(self, r: str) -> list[dict[str, str]]:
        items = xmltodict.parse(r)["items"]["item"]

        if type(items) is not type([]):
            return [items]
        else:
            return items
