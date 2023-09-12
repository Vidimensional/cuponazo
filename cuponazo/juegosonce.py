import logging

from http import HTTPStatus

import requests
import xmltodict

from requests.exceptions import RequestException

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}
url = "https://www.juegosonce.es/rss/sorteos2.xml"


class CuponazoResult:
    def __init__(self, number: str, serie: str):
        self.number = number
        self.serie = serie

    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.serie == __value.serie


class ResultsFetchError(Exception):
    pass


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
            raise ResultsFetchError(f"Unable to request juegosonce results: {str(err)}")

        if resp.status_code is not HTTPStatus.OK.value:
            raise ResultsFetchError(
                f"Invalid response from juegosonce:{resp.reason}({resp.status_code})"
            )

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
