# coding=utf8
"""
Implements tests for the fetcher module.
"""


import pytest
from html_parser.fetcher import FetcherError, HttpFetcher, LocalFileFetcher


class TestLocalFileFetcher:
    @pytest.mark.medium
    def test_retrieved_is_binary(self, tmpdir):
        # Create source file
        html_document = tmpdir.join("test.html")
        content = "<html><body><a href='test.html'>Test</a></body></html><p>ä</p>"
        binary_content = content.encode("utf-8")
        html_document.write(binary_content, mode="wb")

        # Create fetcher and retrieve content
        fetcher = LocalFileFetcher(str(html_document))
        retrieved_content = fetcher.retrieve()

        # Make sure we still have the right binary content
        assert binary_content == retrieved_content

    @pytest.mark.medium
    def test_file_not_found(self):
        fetcher = LocalFileFetcher("__UNKNOWN__.html")
        with pytest.raises(FetcherError):
            fetcher.retrieve()


class TestHttpFetcher:
    @pytest.mark.medium
    def test_retrieved_is_binary(self, httpserver):
        # Create a valid HTML document and serve it via the fake HTTP server
        content = "<html><body><a href='test.html'>Test</a></body></html><p>ä</p>"
        binary_content = content.encode("utf-8")
        httpserver.expect_request("/test.html").respond_with_data(content)

        # Create fetcher and retrieve content
        fetcher = HttpFetcher(httpserver.url_for("/test.html"))
        retrieved_content = fetcher.retrieve()

        # Make sure we still have the right binary content
        assert binary_content == retrieved_content

    @pytest.mark.medium
    def test_file_not_found(self, httpserver):
        fetcher = HttpFetcher(httpserver.url_for("/UNKNOWN.html"))
        with pytest.raises(FetcherError):
            fetcher.retrieve()

    @pytest.mark.medium
    def test_unknown_protocol(self):
        fetcher = HttpFetcher("httpUNKNOWN")
        with pytest.raises(FetcherError):
            fetcher.retrieve()
