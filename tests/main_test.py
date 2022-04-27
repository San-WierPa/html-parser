""""
Provides tests for the main module.

@author: schlauch
"""


import os
import subprocess
import sys

import pytest


## tmpdir: temporal directories
## capfd: capture filedescriptor
def test_parse_localfile_success(tmpdir, capfd):
    # Create a valid HTML document
    html_document = tmpdir.join("test.html")
    html_document.write("<html><body><a href='new_link.html'>Test</a></body></html>")

    # Run the command
    exit_code = _run_main_script([str(html_document)])

    # Make sure it is successfully run
    assert exit_code == 0
    assert capfd.readouterr()[0].startswith("new_link.html")


# def test_parse_remotefile_success(capfd):
#    # Run the script accessing the URL
#    exit_code = _run_main_script(["https://hifis.net"])
#
#    # Check that the expected HIFIS imprint link has been found
#    assert exit_code == 0
#    assert "https://www.desy.de/imprint" in capfd.readouterr()[0]


def test_parse_remotefile_success(httpserver, capfd):
    # Create a valid HTML document and serve it via the fake HTTP server
    content = "<html><body><a href='new_link.html'>Test</a></body></html>"
    url = httpserver.url_for("/test.html")

    # Configure endpoint
    httpserver.expect_request("/test.html").respond_with_data(content)

    # Run the command
    exit_code = _run_main_script([url])

    # Make sure it is successfully run
    assert exit_code == 0
    assert capfd.readouterr()[0].startswith("new_link.html")


def _run_main_script(parameters):
    """Helper to run the main routine of the HTML parser."""

    command = [
        sys.executable,
        "-m",
        "html_parser.main",
    ] + parameters  # python -m html_parser.main <parameters>
    return subprocess.call(command)
