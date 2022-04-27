from unittest import mock

import pytest
from html_parser.fetcher import Fetcher, FetcherError

# actually we want to test the HtmlParser class, but it invokes Fetcher, so
# we need to import Fetcher as well
from html_parser.parser import HtmlParser, HtmlParserError


class TestHtmlParser:
    def setup_method(self, _):
        self._fetcher_mock = mock.Mock(spec=Fetcher)
        self._parser = HtmlParser(self._fetcher_mock)

    def test_extract_links_success(self):
        # Configure the mock
        self._fetcher_mock.retrieve.return_value = (
            "<a href='/index.html'>index.html</a>"
        )

        # Call the method to test
        extracted_links = self._parser.extract_links()

        # Check the assertions
        assert len(extracted_links) == 1
        assert extracted_links[0] == "/index.html"
