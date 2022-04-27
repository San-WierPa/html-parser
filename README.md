# HTML Parser

html-parser is a command line tool to extract links from HTML documents (e.g., from local files or URLs).

## Requirements

- Python >=3.6
- beautifulsoup4 >=4.4

You can install the required dependencies via: `pip install -r requirements.txt`

## Usage

Run the tool as follows:

```
> export PYTHONPATH=.
> python -m html_parser.main <URL_or_LOCAL_HTML_FILE>
```

For more information, please see the help message:

```
General Usage:

html-parser [PATH TO HTML DOCUMENT]
It currently parses a HTML document and prints all links.

Example local file:   html-parser /home/user/test.html
Example HTTP:         html-parser https://www.google.de/
```

## Testing

We require additional dependencies for testing.
You can install them via: `pip install -r requirements-dev.txt`

Then, you can run the available tests as follows:

```
> export PYTHONPATH=.
> pytest tests/
```

# Test automation / Software testing

Software testing is the process of executing and analyzing a software to find errors.
Errors are deviations of the actual from the required state.

## Why Do We Need Automated Tests?

You typically only change a small portion of the code. But you have to make sure that a
growing number code keeps its behavior.

### Automated tests establish a safety net for working with code:

+ Tests protect code behavior
+ Change of behavior results in instant feedback

This approach makes even larger modifications possible with less fear of breaking existing behavior.

**IMPORTANT**: Always test the code alongside the development, not only at the end...

## NOTES (see also https://notes.desy.de/urWp3p8NS5OGerUZR-Nhfw?view)

+ Tests should be automaticated
+ Tested code should be a team effort!

You can test a large portion of code but:

+ Complex test setup as the software needs to be deployed into a production-like environment.
+ Long execution times as setting up the environment might take time and many components and external services are involved.
+ Test results are often unreliable as they depend on many additional factors.
+ `self._*` means stored internally

### Parametrization

```python
    @pytest.mark.parametrize("n, F_n", [
        (4, 5), (5, 8), (6, 13)
    ])
    def test_fibo_n(n, F_n):
        assert fibo(n) == F_n
```

+ Only thing what changes in the function are the parameters!
+ We're telling pytest, that it should expect only a change of parameters!

### urls

- https://notes.desy.de/urWp3p8NS5OGerUZR-Nhfw?view
- https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials
- https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser

### mock

+ So it's like the `__init__`-function just for test classes?
  No!

+ Sometimes the tests can mutate the precondition objects (like the fetcher)
  to assure they are the same for every test, they are so to say reset before every test