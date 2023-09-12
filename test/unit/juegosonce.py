import logging
import unittest

from http import HTTPStatus
from unittest.mock import Mock

import requests

from requests.exceptions import RequestException

from cuponazo.juegosonce import CuponazoResult
from cuponazo.juegosonce import ResultsFetcher
from cuponazo.juegosonce import ResultsFetchError
from cuponazo.juegosonce import url as juegosonce_url


class Test_ResultFetcher_FetchCuponazo(unittest.TestCase):
    def test_remote_returns_correct_response(self):
        mocked_http = build_mocked_http(
            resp_status_code=HTTPStatus.OK,
            resp_text=load_fixture("correct_response"),
        )

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [CuponazoResult("75727", "024")])
        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_remote_returns_response_without_cuponazo(self):
        mocked_http = build_mocked_http(
            resp_status_code=HTTPStatus.OK,
            resp_text=load_fixture("response_without_cuponazo"),
        )

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [])
        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_remote_returns_non_OK_response(self):
        mocked_http = build_mocked_http(resp_status_code=HTTPStatus.NOT_FOUND)

        fetcher = ResultsFetcher(juegosonce_url, mocked_http)

        with self.assertRaises(ResultsFetchError):
            fetcher.fetch_cuponazo()

        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_newtork_connection_fails(self):
        mocked_http = build_mocked_http(err=RequestException)
        fetcher = ResultsFetcher(juegosonce_url, mocked_http)

        with self.assertRaises(ResultsFetchError):
            fetcher.fetch_cuponazo()
        mocked_http.get.assert_called_once_with(juegosonce_url)

    def test_response_payload_is_invalid_xml(self):
        mocked_http = build_mocked_http(
            resp_status_code=HTTPStatus.OK,
            resp_text="asad.</",
        )
        fetcher = ResultsFetcher(juegosonce_url, mocked_http)

        with self.assertRaises(ResultsFetchError):
            fetcher.fetch_cuponazo()
        mocked_http.get.assert_called_once_with(juegosonce_url)


def load_fixture(case: str) -> str:
    with open(f"test/unit/testdata/juegosonce_remote_{case}.xml") as f:
        return f.read()


def build_mocked_http(
    resp_status_code: HTTPStatus = None,
    resp_text: str = None,
    err: Exception = None,
) -> Mock | requests.Session:
    mocked_http = Mock()
    mocked_http.get = Mock()

    if err is None:
        http_response = Mock()
        http_response.text = resp_text
        http_response.status_code = resp_status_code.value
        mocked_http.get.return_value = http_response
    else:
        mocked_http.get.side_effect = err

    return mocked_http
