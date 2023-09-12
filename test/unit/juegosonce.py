import logging
import unittest
from unittest.mock import Mock

from requests.exceptions import RequestException

from cuponazo.juegosonce import CuponazoResult
from cuponazo.juegosonce import ResultsFetcher
from cuponazo.juegosonce import url as juegosonce_url


class Test_ResultFetcher_FetchCuponazo(unittest.TestCase):
    def test_remote_returns_correct_response(self):
        test_case = "correct_response"
        expected_http_reponse = Mock()
        expected_http_reponse.text = load_fixture(test_case)

        mocked_http = Mock()
        mocked_http.get = Mock(return_value=expected_http_reponse)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [CuponazoResult("75727", "024")])
        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_remote_returns_response_without_cuponazo(self):
        test_case = "response_without_cuponazo"
        expected_http_reponse = Mock()
        expected_http_reponse.text = load_fixture(test_case)

        mocked_http = Mock()
        mocked_http.get = Mock(return_value=expected_http_reponse)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [])
        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_we_receive_error_in_connection(self):
        mocked_http = Mock()
        mocked_http.get = Mock(side_effect=RequestException)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)

        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(RequestException):
                fetcher.fetch_cuponazo()
        mocked_http.get.assert_called_once_with(juegosonce_url)


def load_fixture(case: str) -> str:
    with open(f"test/unit/testdata/juegosonce_remote_{case}.xml") as f:
        return f.read()
