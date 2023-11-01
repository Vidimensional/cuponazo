import logging

from http import HTTPStatus

import requests
import xmltodict

from requests.exceptions import RequestException

from cuponazo.domain import results_fetcher
from cuponazo.domain import ticket

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}
url = "https://www.juegosonce.es/rss/sorteos2.xml"


class ResultsFetcher(results_fetcher.Interface):
    """Class responsible to fetch results from Juegosonce.

    Parameters
    ----------
    `url` (`str`)
        URL for the Juegosonce endpoint with latests results.

    `http` (`requests.sessions.Session`)
        Requests sessions used to make the actual request to `url`.
    """

    def __init__(self, url: str, http: requests.sessions.Session) -> None:
        self.url = url
        self.http = http

    def fetch_cuponazo(self) -> list[ticket.Cuponazo]:
        """Fetches restulsts from `self.url` and returns a list of `ticket.Cuponazo` with the winning combination.

        Returns
        -------
        `list[ticket.Cuponazo]`
            List with the result of the latest Cuponazo lottery.
        """
        return [
            ticket.Cuponazo(item["numero"], item["serie"])
            for item in self.__fetch("cuponazo")
        ]

    def __fetch(self, lottery_type: str) -> list[dict[str, str]]:
        try:
            resp = self.http.get(self.url)
        except RequestException as err:
            raise results_fetcher.Error(
                f"Unable to request juegosonce results: {str(err)}"
            )

        if resp.status_code is not HTTPStatus.OK.value:
            raise results_fetcher.Error(
                f"Invalid response from juegosonce:{resp.reason}({resp.status_code})"
            )

        return [
            item
            for item in self.__get_items_from_response(resp.text)
            if item["tipo"] == lottery_names[lottery_type]
        ]

    def __get_items_from_response(self, r: str) -> list[dict[str, str]]:
        try:
            items = xmltodict.parse(r)["items"]["item"]

        except Exception as err:
            # This raises too many kinds of Exceptions... Let's catch all.
            raise results_fetcher.Error(
                f"Got an issue parsing juegosonce XML response: {str(err)}"
            )

        if type(items) is not type([]):
            return [items]
        else:
            return items
