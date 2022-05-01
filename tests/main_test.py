""""
Provides tests for the main module.
"""


import os
import subprocess
import sys

import pytest


@pytest.mark.large
def test_parse_localfile_success(tmpdir, capfd):
    # Create a valid HTML document
    html_document = tmpdir.join("test.html")
    html_document.write("<html><body><a href='new_link.html'>Test</a></body></html>")

    # Run the command
    exit_code = _run_main_script([str(html_document)])

    # Make sure it is successfully run
    assert exit_code == 0
    assert capfd.readouterr()[0].startswith("new_link.html")


@pytest.mark.large
def test_parse_remotefile_success(httpserver, tmpdir, capfd):
    # Create a valid HTML document and serve it via the fake HTTP server
    content = "<html><body><a href='new_link.html'>Test</a></body></html>"
    httpserver.expect_request("/test.html").respond_with_data(content)

    # Run the command
    exit_code = _run_main_script([httpserver.url_for("/test.html")])

    # Make sure it is successfully run
    assert exit_code == 0
    assert capfd.readouterr()[0].startswith("new_link.html")


@pytest.mark.large
def test_show_help_message_when_wrongly_called(capfd):
    # Run the command without any parameters
    exit_code = _run_main_script([])

    # Make sure taht the usage text is printed
    assert exit_code == 0
    assert "General Usage" in capfd.readouterr()[0]


@pytest.mark.large
def test_handle_chained_error(capfd):
    # Trigger an error via an non-existing file
    input_file = "__UNKONWN__"
    assert not os.path.exists(input_file)
    exit_code = _run_main_script([input_file])

    # Make sure that the chained error is printed
    assert exit_code != 0
    assert "No such file or directory" in capfd.readouterr()[0]


def _run_main_script(parameters):
    """Helper to run the main routine of the HTML parser."""

    command = [
        sys.executable,
        "-m",
        "html_parser.main",
    ] + parameters  # python -m html_parser.main <parameters>
    return subprocess.call(command)
