import requests
import xmltodict

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}
url = "https://www.juegosonce.es/rss/sorteos2.xml"


class ResultsFetcher:
    def __init__(self, url: str, http: requests.Session) -> None:
        self.url = url
        self.http = http

    def fetch_cuponazo(self) -> str:
        return self.fetch("cuponazo")

    def fetch(self, lottery_type: str) -> str:
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
