"""
Provides functionality to parse HML docuements.
"""


import bs4


class HtmlParser:
    """
    Parses a HTML document and makes the result accesible to other client modules.
    Currently, only the extraction of URLs is supported.
    """

    def __init__(self, html_document):
        """
        :param html_document: HTML content to be parsed. Decoding is handled automatically.
        :type html_document: str or bytes
        """

        self._html_document = html_document

    def extract_links(self):
        """Extracts links from the HTMl document retrieved via the fetcher.

        :note: Here is the actual content retrieved as well. Thus, it might need some time.

        :return: A list of parsed links.
        """

        # Parses the content and handles decoding of bytes automatically
        parser = bs4.BeautifulSoup(self._html_document, "html.parser")

        # Determine all links
        retrieved_links = list()
        links = parser.find_all("a")
        for tag in links:
            link = tag.get("href", None)
            if link is not None:
                retrieved_links.append(link)
        return retrieved_links


class HtmlParserError(Exception):
    pass
