import http
import unittest
import unittest.mock
import urllib.error

from cuponazo.domain import ticket
from cuponazo.domain import results_fetcher
from cuponazo.infrastructure import results_fetcher as infra

JUEGOSONCE_URL = "https://juegosonce.local/result.xml"


class Test_ResultFetcher_FetchCuponazo(unittest.TestCase):
    @unittest.mock.patch("urllib.request.urlopen")
    def test_remote_returns_correct_response(self, mocked_urlopen):
        populate_mocked_urlopen(
            mocked_urlopen,
            resp_status_code=http.HTTPStatus.OK,
            resp_text=load_fixture("correct_response"),
        )

        fetcher = infra.ResultsFetcher(JUEGOSONCE_URL)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [ticket.Cuponazo("75727", "024")])
        mocked_urlopen.assert_called_once_with(JUEGOSONCE_URL)

    @unittest.mock.patch("urllib.request.urlopen")
    def test_remote_returns_response_without_cuponazo(self, mocked_http):
        populate_mocked_urlopen(
            mocked_http,
            resp_status_code=http.HTTPStatus.OK,
            resp_text=load_fixture("response_without_cuponazo"),
        )

        fetcher = infra.ResultsFetcher(JUEGOSONCE_URL)
        result = fetcher.fetch_cuponazo()

        self.assertEqual(result, [])
        mocked_http.assert_called_once_with(JUEGOSONCE_URL)

    @unittest.mock.patch("urllib.request.urlopen")
    def test_remote_returns_non_OK_response(self, mocked_http):
        populate_mocked_urlopen(
            mocked_http,
            resp_status_code=http.HTTPStatus.NOT_FOUND,
        )

        fetcher = infra.ResultsFetcher(JUEGOSONCE_URL)

        with self.assertRaises(results_fetcher.Error):
            fetcher.fetch_cuponazo()

        mocked_http.assert_called_once_with(JUEGOSONCE_URL)

    @unittest.mock.patch("urllib.request.urlopen")
    def test_newtork_connection_fails(self, mocked_http):
        populate_mocked_urlopen(
            mocked_http,
            err=urllib.error.URLError("Some HTTPError"),
        )
        fetcher = infra.ResultsFetcher(JUEGOSONCE_URL)

        with self.assertRaises(results_fetcher.Error):
            fetcher.fetch_cuponazo()
        mocked_http.assert_called_once_with(JUEGOSONCE_URL)

    @unittest.mock.patch("urllib.request.urlopen")
    def test_response_payload_is_invalid_xml(self, mocked_http):
        populate_mocked_urlopen(
            mocked_http,
            resp_status_code=http.HTTPStatus.OK,
            resp_text="asad.</",
        )
        fetcher = infra.ResultsFetcher(JUEGOSONCE_URL)

        with self.assertRaises(results_fetcher.Error):
            fetcher.fetch_cuponazo()
        mocked_http.assert_called_once_with(JUEGOSONCE_URL)


def load_fixture(case: str) -> str:
    with open(f"test/unit/testdata/juegosonce_remote_{case}.xml") as f:
        return f.read()


def populate_mocked_urlopen(
    mocked_urlopen: unittest.mock.Mock,
    resp_status_code: http.HTTPStatus = None,
    resp_text: str = "",
    err: Exception = None,
) -> unittest.mock.Mock:
    if err is None:
        http_response = unittest.mock.Mock(name="http_response")
        http_response.read.return_value = bytes(resp_text, encoding="utf8")
        http_response.code = resp_status_code.value
        mocked_urlopen.return_value = http_response
    else:
        mocked_urlopen.side_effect = err

    return mocked_urlopen
