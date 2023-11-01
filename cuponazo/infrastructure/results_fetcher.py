import http
import urllib.error
import urllib.request

import xmltodict

from cuponazo.domain import results_fetcher
from cuponazo.domain import ticket

lottery_names = {"cuponazo": "Cuponazo", "cupon_diario": "Cup&oacute;n Diario"}


class ResultsFetcher(results_fetcher.Interface):
    """Class responsible to fetch results from Juegosonce.

    Parameters
    ----------
    `url` (`str`)
        URL for the Juegosonce endpoint with latests results.
    """

    def __init__(self, url: str) -> None:
        self.url = url

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
            resp = urllib.request.urlopen(self.url)
        except urllib.error.URLError as err:
            raise results_fetcher.Error(
                f"Unable to request juegosonce results: {str(err)}"
            )

        if resp.code is not http.HTTPStatus.OK.value:
            raise results_fetcher.Error(
                f"Invalid response from juegosonce:{resp.reason}({resp.status_code})"
            )

        return [
            item
            for item in self.__get_items_from_response(resp.read())
            if item["tipo"] == lottery_names[lottery_type]
        ]

    def __get_items_from_response(self, r: bytes) -> list[dict[str, str]]:
        try:
            items = xmltodict.parse(r)["items"]["item"]

        # This raises too many kinds of Exceptions... Let's catch all.
        except Exception as err:
            raise results_fetcher.Error(
                f"Got an issue parsing juegosonce XML response: {str(err)}"
            )

        if type(items) is not type([]):
            return [items]
        else:
            return items
