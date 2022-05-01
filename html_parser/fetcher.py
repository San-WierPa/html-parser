"""
Defines the Fetcher interface which is used to retrieve the content of documents from a given path.
It aims to support a wide range of different protocols (e.g., HTTP, local file).
"""


from urllib.request import urlopen


class Fetcher:
    """
    Defines the basic interface for a Fetcher instance.
    It is used to retrieve HTML docuements from varous source.
    """

    def __init__(self, path):
        """
        :param path: Identifies the document to retrieve. Supported is the "file" and "http" scheme.
        :type path: str
        """

        self._path = path

    def retrieve(self):
        """Returns the content of the document.

        :return: Binary content of the document.
        :rtype: bytes

        :raise FetcherError: Indicates problems accessing the content of the document.
        """

        raise NotImplementedError(
            "This is the base class of all Fetcher instances. You need to subclass and implement this method properly."
        )


class LocalFileFetcher(Fetcher):
    """Retrieves content from a local file."""

    def retrieve(self):
        try:
            with open(self._path, mode="rb") as file_object:
                return file_object.read()
        except IOError as error:
            raise FetcherError("Failed to retrieve content of '{0}'!".format(self._path)) from error


class HttpFetcher(Fetcher):
    """Retrieves content via HTTP."""

    def retrieve(self):
        try:
            with urlopen(self._path) as file_object:
                return file_object.read()
        except (IOError, ValueError) as error:
            raise FetcherError("Failed to retrieve content of '{0}'!".format(self._path)) from error


class FetcherError(Exception):
    pass


def create_fetcher(path):
    """
    Creates a fetchers instance to handle the given path.

    :param path: Identifies the document to retrieve. You can provide a HTTP/HTTPS URL or a local file path.
    :type path: str

    :return: The initialized fetcher instance.
    :rtype: `Fetcher`
    """

    if path.startswith("http"):
        return HttpFetcher(path)
    else:
        return LocalFileFetcher(path)
