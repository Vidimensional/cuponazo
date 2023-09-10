import requests
import xmltodict

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}
url = "https://www.juegosonce.es/rss/sorteos2.xml"


class CuponazoResult:
    def __init__(self, number: str, serie: str):
        self.number = number
        self.serie = serie


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
        resp = self.http.get(self.url)

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
