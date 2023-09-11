import json
import unittest
from unittest.mock import Mock

from cuponazo.juegosonce import CuponazoResult
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

        self.assertTrue(len(result), 1)
        self.assertEqual(result[0].number, "75727")
        self.assertEqual(result[0].serie, "024")

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
        self.assertEqual(result, [])


def load_fixture(case: str) -> str:
    with open(f"test/unit/testdata/juegosonce_remote_{case}.xml") as f:
        return f.read()
