from html_parser.parser import HtmlParser


class TestHtmlParser:
    def test_extract_links_success(self):
        parser = HtmlParser("<a href='/index.html'>index.html</a>")

        extracted_links = parser.extract_links()

        assert len(extracted_links) == 1
        assert extracted_links[0] == "/index.html"

    def test_extract_links_no_links(self):
        parser = HtmlParser("<html></html>")

        extracted_links = parser.extract_links()

        assert len(extracted_links) == 0

    def test_extract_links_without_href(self):
        parser = HtmlParser("<a>a link</a>")

        extracted_links = parser.extract_links()

        assert len(extracted_links) == 0

    def test_extract_links_invalid_html(self):
        parser = HtmlParser("<html</html /a <A></p>")

        extracted_links = parser.extract_links()

        assert len(extracted_links) == 0

    def test_extract_links_empty_document(self):
        parser = HtmlParser("")

        extracted_links = parser.extract_links()

        assert len(extracted_links) == 0

    def test_handle_string_content_success(self):
        parser = HtmlParser("<a href='/indäx.html'>index.html</a>")

        extracted_links = parser.extract_links()

        assert extracted_links[0] == "/indäx.html"

    def test_handle_binary_content_success(self):
        # We have to provide a proper encoding hint in the HTML document.
        # Otherwise bs4 might fail determining the encoding.
        binary_content = (
            "<meta charset=\"utf-8\"/><a href='/indäx.html'>index.html</a>".encode(
                "utf-8"
            )
        )
        parser = HtmlParser(binary_content)

        extracted_links = parser.extract_links()

        assert extracted_links[0] == "/indäx.html"
