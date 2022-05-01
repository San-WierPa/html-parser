"""
The main script which implements a small command line interface.
"""
import os
import sys

from html_parser.fetcher import FetcherError, create_fetcher
from html_parser.parser import HtmlParser, HtmlParserError


def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        try:
            fetcher = create_fetcher(path)
            html_document = fetcher.retrieve()
            parser = HtmlParser(html_document)
            extracted_links = parser.extract_links()
        except (FetcherError, HtmlParserError) as error:
            print(
                "Sorry an error occurred: {0}".format(error),
                error.__cause__,
                error.__cause__.__cause__,
            )
            return -1
        else:
            for link in extracted_links:
                print(link)
    else:
        script_name = os.path.basename(__file__)
        print(
            "General Usage:        {0} [PATH TO HTML DOCUMENT]\n"
            "It currently parses a HTML document and prints all links.\n\n"
            "Example local file:   {0} /home/user/test.html\n"
            "Example HTTP:         {0} https://www.google.de/\n".format(script_name)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
