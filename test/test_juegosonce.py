import json
import unittest
from unittest.mock import Mock

from cuponazo.juegosonce import ResultsFetcher
from cuponazo.juegosonce import url as juegosonce_url


class TestResultFetcher(unittest.TestCase):
    def test_fetch_cuponazo_juegosonce_returns_correct_response(self):
        raffle_type = "cuponazo"
        test_case = "correct_response"

        expected_http_reponse = Mock()
        expected_http_reponse.text = load_fixture(test_case)

        mocked_http = Mock()
        mocked_http.get = Mock(return_value=expected_http_reponse)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, load_expected_result(raffle_type, test_case))

    def test_fetch_cuponazo_juegosonce_returns_response_without_cuponazo(self):
        raffle_type = "cuponazo"
        test_case = "response_without_cuponazo"

        expected_http_reponse = Mock()
        expected_http_reponse.text = load_fixture(test_case)

        mocked_http = Mock()
        mocked_http.get = Mock(return_value=expected_http_reponse)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        # FIXME should we expect an exception here?
        self.assertEqual(result, load_expected_result(raffle_type, test_case))


def load_fixture(case: str) -> str:
    with open(f"test/testdata/juegosonce_remote_{case}.xml") as f:
        return f.read()


def load_expected_result(lottery_type: str, case: str) -> str:
    with open(f"test/testdata/juegosonce_{lottery_type}_fetcher_{case}.json") as f:
        return json.loads(f.read())
