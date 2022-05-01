# Test Automation with  Python

<!--
## Agenda Day 1 (26.04.2022)


| Time          | Topic                                                        |
| ------------- | ------------------------------------------------------------ |
| 09:00 - 09:30 | Welcome & Introduction                                       |
| 09:30 - 10:00 | Introduction to test automation                              |
| 10:00 - 12:15 | Introduction to pytest                                       |
| 12:15 - 13:00 | HTML parser: Introduction and initial characterization tests |
| 13:00 - 13:05 | Wrap up day 1                                                |

*Times are approximate. We will have a break of 15 minutes about every 90 minutes.*

## Agenda Day 2 (27.04.2022)

| Time          | Topic                                                        |
| ------------- | ------------------------------------------------------------ |
| 09:00 - 09:15 | Recap day 1                                                  |
| 09:15 - 10:45 | HTML parser: Test isolation with test doubles       |
| 10:45 - 11:15 | HTML parser: Analyzing the code coverage                     |
| 11:15 - 11:45 | HTML parser: Improving the test suite and the code structure |
| 11:45 - 12:15 | HTML parser: Build automation and CI/CD with GitLab          |
| 12:15 - 13:00 | QA / Wrap Up / Feedback                                      |

*Times are approximate. We will have a break of 15 minutes about every 90 minutes.*

<!--
## Open Questions
-->


<!-
## Further Readings

- [Workshop Materials](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials)
- [HTML Parser code example](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser)
- [mypy](http://mypy-lang.org/) - Linter that makes use of the optional static typing support in Python. 
- [Python Plugins to Love](https://towardsdatascience.com/pytest-plugins-to-love-%EF%B8%8F-9c71635fbe22)
- [Dustin Boswell, Trevor Foucher: "The Art of Readable Code", O'Reilly Media, 2011](http://shop.oreilly.com/product/9780596802301.do) - Contains a section about writing readable test cases.
- Please use [`tmp_path`](https://docs.pytest.org/en/6.2.x/tmpdir.html) fixture instead of the `tmp_dir` as it supports the new Python `pathlib.Path` interface.
- [Real Python, "Understanding the Python Mock Object Library"](https://realpython.com/python-mock-library/) for more information about the `unittest.mock`.
-->

<!--
## Organizational Details

### Before the workshop

- Please fill out the [pre-workshop survey](https://survey.pt-dlr.de/index.php?r=survey/index&sid=1001&lang=en) to help us preparing the workshop.

<!--
- Please check your technical setup:
    
    - [ ] Please make sure that you installed Required Software Tools (see below).
    
  - [ ] Please connect to the [Gather Town room](https://app.gather.town/app/nkxyTbuI84smfiQk/HMC-Workshop-Lounge). You spawn directly in the auditorium in which we start. Feel free to already explore the map :)
    - Please **use a recent Chromium-based browser** (e.g., Chromium, Microsoft Edge). Other modern browsers (e.g., FireFox) might work as well but we noticed sometimes performance issues.
    - Please avoid using VPN (if you use any) to improve your connection performance.
    - For further information, please see: [System Requirements](https://support.gather.town/help/system-specifications), [Getting Started Guide](https://support.gather.town/help/movement-and-basics), [Audio and Video Troubleshooting](https://support.gather.town/help/av-troubleshooting)
        
    - [ ] At the end of the workshop, we would like to give you explicit time for your special testing topics. If you want to discuss a topic, please send us a short description of it in advance!
-->

#### Required Software Tools

- Please install a Python 3 interpreter (3.7 or newer) and your favorite text editor (e.g., Notepad++, gedit,...).
- Additionally, you need the following third-party Python modules:
    - beautifulsoup4>=4.9.3
    - pytest>=6.1.1
    - pytest-cov>=2.10.1
    - coverage>=5.3
    - pytest-httpserver>=0.3.5
- Please also download and extract the [example code](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/archive/01-add-further-characterization-tests/html-parser-01-add-further-characterization-tests.zip).

### During the workshop

- Please be back in time after breaks
- Make use of the chat if you have questions or remarks
- We try to keep this pad up-to-date during the lesson so you can catch up


# Day 1 - 26-04-2022

## Introduction Round

- What is your name and affiliation?
- Why do you use Python and what is your primary project?


## [Introduction to Test Automation](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode01.md)

>  Software testing is the process of executing and analyzing a software to find errors. Errors are deviations of the actual from the required state.

### Why Do We Need Automated Tests?

You typically only change a small portion of the code. But you have to make sure that **a growing number code keeps its behavior**:

![Protect existing behaviour](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/protect-behavior.svg)


Automated tests establish a safety net for working with code:
  - Tests protect code behavior
  - Change of behavior results in instant feedback

This approach makes even larger modifications possible with less fear of breaking existing behavior.


### Test Types

#### Large Tests

> Large tests check whether the software works as a whole in a production-like environment.

![Large test scope](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/large-test-type.svg)

- You can test a large portion of code but:
  - Complex test setup as the software needs to be deployed into a production-like environment.
  - Long execution times as setting up the environment might take time and many components and external services are involved.
  - Test results are often unreliable as they depend on many additional factors.


#### Medium Tests

> Medium tests checks the interaction of a subset of code units and external services.

![Medium test scope](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/medium-test-type.svg)

- Differences to large tests:
  - The test setup is less complex.
  - The test execution time (< 1s) is faster.
  - The tests produce more reliable results.


#### Small Tests

> Small tests check a specific code unit in isolation.

![Small test scope](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/small-test-type.svg)

- Small tests provide extremely fast and reliable feedback.
- Make sure to not "isolate away" the real source of errors.


#### Delimitation by Resource Usage

|         Resource        | Large Tests  |     Medium Tests   |     Small Tests    |
|:-----------------------:|:------------:|:------------------:|:------------------:|
|     Network             |       X      |      local host    |      mocked        |
|     Database            |       X      |          X         |      mocked        |
|     File system         |       X      |          X         |      mocked        |
|     GUI                 |       X      |     discouraged    |      mocked        |
|     System calls        |       X      |     discouraged    |          -         |
|     Multiple threads    |       X      |          X         |     discouraged    |
|     Sleep statements    |       X      |          X         |          -         |

Required execution environment:
- Small and medium tests should run directly on the developer machine.
- Large tests usually require a dedicated execution environment

### Structuring Your Test Suite

The test pyramid provides a simple heuristic to create a fast and maintainable automated test suite.

![Test pyramid](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/test-pyramid.svg)

You should not become too attached to concrete numbers, layers and names. But the two important takeaway points:

1. You should write tests with different level of granularity which complement each other.
1. The more high-level you get, the less tests you should write.

### Key Points

- Test automation is an important tool for effective and efficient software testing.
- A fast and maintainable automated test suite is key to keep your software maintainable.
- The test pyramid provides a simple model to structure your automated test suite properly.


## [Introduction to pytest](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode02.md)


Python already provides a built-in [unittest](https://docs.python.org/3/library/unittest.html) framework.
However, it has some shortcomings:

- Limited automatic test discovery.
- Bloated boiler-plate code.
- Clunky assertions.



Thus, we selected [pytest](https://docs.pytest.org/en/stable/)
It is compatible to `unittest` and follows the [xUnit approach](https://en.wikipedia.org/wiki/XUnit)

<table>
<tr><th>pytest</th><th>unittest</th></tr>
<tr><td>

```python
from math import factorial

def test_factorial_success():
    assert factorial(1) == 1
```

</td><td>

```python
import unittest

from math import factorial

class TestFactorial(unittest.TestCase):
    def testSuccess(self):
        self.assertEqual(factorial(1), 1)
```

</td></tr></table>


### Test Driven Development (TDD)

![Test driven development cycle](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/tdd_cycle.png)


TDD is an approach to build such a safety net:

1. Write a test that fails ("Red").
1. Write just enough code that the test passes ("Green").
1. Refactor and improve the code without changing the behaviour of the code ("Refactor").


<!-
### Testing the Fibonacci Sequence

<!-
Fibonacci sequence is known to be the following infinite series of numbers:

> 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

It can be expressed with the following recursive formula:

\begin{align}
F_0 = F_1 = 1 \\
F_n = F_{n - 1} + F_{n - 2}
\end{align}

<!-

### Step 1: Simple Tests

- Create a file `fibo_test.py` and add the following code:

    ```python
    from fibo import fibo

    def test_fibo_start():
        assert fibo(0) == 1
    ```

- Execute the test with `pytest`:

    ```bash
    $ pytest fibo_test.py
    ```

- Create a file `fibo.py` with the following content:

    ```python
    def fibo(n):
        return 1
    ```

- Again, run the test:

    ```bash
    $ pytest fibo_test.py
    ```

- Modify `test_fibo_start` to read like the following:

    ```python
    def test_fibo_start():
        assert fibo(0) == 1
        assert fibo(1) == 1
    ```

- Add the following test to `fibo_test.py`:

    ```python
    def test_fibo_2():
        assert fibo(2) == 2
    ```

- Run the tests again

    ```bash
    $ pytest fibo_test.py
    ```

- Change `fibo.py` to read as follows:

    ```python
    def fibo(n):
        if n < 2:
            return 1
        else:
            return 2
    ```

- Run the tests again.

    ```bash
    $ pytest fibo_test.py
    ```
<!-
#### Exercise

- Add another test to `fibo_test.py` to calculate `fibo(3)`.
- Fix your implementation of `fibo(n)` for the last test to succeed.
  *Choose the minimalistic solution, we will add a proper implementation in a minute.*


<!-
### Step 2: Parametric Tests

- At the beginning of `fibo_test.py` add the following line:

    ```python
    import pytest
    ```

- Then, add the following test case to `fibo_test.py`:

    ```python
    @pytest.mark.parametrize("n, F_n", [
        (4, 5), (5, 8), (6, 13)
    ])
    def test_fibo_n(n, F_n):
        assert fibo(n) == F_n
    ```

- Execute the tests:

    ```bash
    $ pytest fibo_test.py
    ```

- Change `fibo.py` to read as follows:

    ```python
    def fibo(n):
        if n < 2:
            return 1
        else:
            return fibo(n - 1) + fibo(n - 2)
    ```

- Run the tests again:

    ```bash
    $ pytest fibo_test.py
    ```
<!-
### Step 3: Choosing Test Cases

![Numeric domain of Fibonacci sequence](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/numeric-domain.svg)


- Add the following test to `fibo_test.py`:

    ```python
    def test_fibo_negative():
        with pytest.raises(ValueError):
            fibo(-1)
    ```

- Execute the test and look at the results:

    ```bash
    $ pytest fibo_test.py
    ```

- Update `fibo.py` to check for negative values:

    ```python
    def fibo(n):
        if n < 0:
            raise ValueError("Fibonacci sequence is only defined for non-negative n.")
        elif n < 2:
            return 1
        else:
            return fibo(n - 1) + fibo(n - 2)
    ```

- Run the tests again:

    ```bash
    $ pytest fibo_test.py
    ```
<!-
#### Exercise

- Write a test that checks if `fibo()` raises an `TypeError` if a non-integer value is passed.
- Update the implementation to successfully pass the test.

<!-
### Step 4: Refactoring Supported by Tests

- Add the following test to `fibo_test.py`:

    ```python
    def test_fibo_huge():
        assert fibo(35) == 14930352
    ```


- Excute the tests again:

    ```bash
    $ pytest fibo_test.py
    ```

- Create a file `pytest.ini` with the following content:

    ```ini
    [pytest]
    markers =
        slow: Tests that take longer to execute.
    ```

- Change `fibo_test.py` by adding an annotation to `fibo_test_huge()`:

    ```python
    @pytest.mark.slow
    def test_fibo_huge():
        assert fibo(35) == 14930352
    ```

- Now we can skip `slow` tests by running:

    ```bash
    $ pytest -m "not slow" fibo_test.py
    ```
<!-
#### Exercise

- Refactor `fibo.py` to avoid recursive calls.
  Use a list and a loop to implement the calculation.
- Test your new implementation against your test suite.
  See how the runtime of your tests changes.


```python
_fibo = [1, 1]


def fibo(n):
    if not isinstance(n, int):
        raise TypeError("Fibonacci sequence is only defined for integer values.")
    elif n < 0:
        raise ValueError("Fibonacci sequence is only defined for positive n.")
    else:
        while len(_fibo) <= n:
            _fibo.append(_fibo[-1] + _fibo[-2])
        return _fibo[n]
```
<!-
### Key Points

- *pytest* is a good alternative to Python's `unittest` module.
  It reduces boilerplate code, integrates test discovery, and allows to write better readable assertions.
- Test cases are simple Python functions that start with `test_` or end with `_test`.
- You can use the `assert` statement to make assertions.
  *pytest* will provide useful error messages for them if they fail.
- Test cases can be parametrized using the decorator `@pytest.mark.parametrize(...)`.
- To test raised errors, you can use `with pytest.raises(...)` as context.
- You can add custom markers to filter test execution, for example, to skip slow tests.

-->

<!-
## [HTML Parser: Introduction and Initial Characterization Tests](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode03.md)


![HTML Parser context](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/html-parser-context-view.png)

You are the new maintainer of the **HTML parser tool**. The former maintainer already left and sent you [the link to the Git repository](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/tree/00-intial-version). But where are the tests??


### How to Approach Legacy Code?

```python
def test_parser_success():
    fetcher = ...
    html_parser = HTMLParser(fetcher)
    links = html_parser.extract_links()
    assert len(links) ...
```

If you want to test the `HTMLParser` object of this code base using a **small test**, you have to write something like this. But this is not easy to do because:
  - How to create a `fetcher`?
  - How can we add tests without changing `HTMLParser` in the first place?

Write **characterization tests** to establish an **initial safety net** and to **capture our intial findings** when we start working with the application!


#### Question: Which Code Type Should Be Covered by which Tests?

![Test portfolio](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/costs-benefits-small-tests.svg)

- Use small tests for **algorithm like code**.
- Use medium tests for **coordinator code**.
- **Trivial code** is usually tested (implicitly) by large and medium tests.
- **Overcomplicated code**: establish safety net, refactor, optimize.

### Creating Initial Characterization Tests

> [Example Code: Add further characterization tests](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/archive/01-add-further-characterization-tests/html-parser-01-add-further-characterization-tests.zip)

- Extract archive and add it to your `PYTHONPATH`:
    - Change into the directory, and ...
    - ... for Window (`cmd.exe`) type: `set PYTHONPATH=.`
    - ... for PowerShell: `$PYTHONPATH = "."`
    - ... for Linux (e.g., `bash`) type: `export PYTHONPATH=.`
    - *This should also work for following examples/exercises as long as you are in the correct directory.*

- You can check if everything works:
    - `python -m html_parser.main` shoud give a help message.
    - `python -m html_parser.main https://www.dlr.de` should list all links from the DLR home page.

- Run the tests with `python -m pytest tests`.



#### Exercise

- Please implement the `test_parse_remotefile_success` test case.
  The test should retrieve a HTML file from a Web server (e.g., `https://www.dlr.de`) and check for a specific link in the command-line output.
- Hints:
  - Please run the `html-parser` tool manually to find out the test setup (URL to check) and the expected result (a link contained in the HTML document).
  - Please make sure to provide the right parameter to the `_run_main_script()` function.
  - Please use the `capfd` fixture to check the output of the command-line tool.
    You can check whether a string is contained in the output as follows: `assert "link" in capfd.readouterr()[0]`.
- Please run the tests again to make sure that everything works as expected.
    - What changes do you notice when running the tests?
    - How stable do you consider this test case?

<!-
Example Solution:

```python

def test_parse_remotefile_success(capfd):
    # Run the script accessing the URL
    exit_code = _run_main_script(["https://hifis.net"])

    # Check that the expected HIFIS imprint link has been found
    assert exit_code == 0
    assert "https://www.desy.de/imprint" in capfd.readouterr()[0]

```

### Key Points

- When testing legacy code without any tests, you usually need to establish a safety net consisting of **characterization tests**.
- These tests are usually large tests which can help you to safely refactor overcomplicated code into testable units.
- It is important to test a specific functionality on the right test level and to keep an eye on the overall test suite structure.
- `pytest` can be used to automate medium and large tests as well.


<!-
# Day 2 27-04-2022

## Welcome and Recap

### Where to go from here?

- With our initial safety net in place, we can now:
  - Start improving / changing the code.
  - Start improving our test suite:
      - Add more fine granular tests (levels M and S)
      - Refactor existing tests to make them more reliable / faster.

## Continue [HTML Parser: Introduction and Initial Characterization Tests](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode03.md)


## [HTML Parser: Test Isolation with Test Doubles](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode04.md)

Software can get complex, dependencies have further dependencies. The scope of the *unit under test* might easily get unclear.

![Isolating test scope](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/unit-isolation.svg)

It is desireable to isolate the *unit under test* from the rest of the system.

---

In addition, we already have seen that there might be slow interactions with external systems that are not under our control.

![Call hierarchy](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/html-parser-sequence-diagram.png)

This is also undesireable for designing deterministic tests.

### Hierarchy of Test Doubles

* Dummy Objects
* Stub Objects
* Fake Objects
* Mock Objects

### Usage Recommendations

You have to decide on the specific situation which test double is suited most (order implicates applicability):
 - **External system which is out of control:** fake object, record and play libraries (kind of automatically created/updatable stub), stub, mock
 - **Slow tests because of external system access:** fake object, stub / mock + minimal tests with real dependency
 - **It is hard to bring the sysinitem under test into a specific state:** stub, mock
 - **Missing components:** dummy object, stub, mock
 - **Non-observable state:** mock


## HTML Parser: Improving the Remote Access Test with a Fake Object


We start from the existing test case:

```python
def test_parse_remotefile_success(capfd):
    # Define URL
    url = "https://hifis.net"

    # Run the command
    exit_code = _run_main_script([url])

    # Make sure it is successfully run
    assert exit_code == 0
    assert ("/events") in capfd.readouterr()[0]
```

We adapt this test case to use a local HTTP server instead of a file as source.
This way we can test if the script works with remote data.

- Change the name of the test to `test_parse_remotefile_success`
- Add another fixture `httpserver` as a parameter to the test.
  `tmpdir` is no longer needed.
- Configure the `httpserver` fixture to deliver given data for `/test.html`:
  ```python
    content = "<html><body><a href='new_link.html'>Test</a></body></html>"
    httpserver.expect_request("/test.html").respond_with_data(content)
  ```
- Call the script with the URL of the `httpserver`.

The resulting tests looks as follows:

```python
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
```

The pytest plugin provides a test fixture named `httpserver`.
This object can be used to define an expected request for which we return the prepared HTML content.
Then, we can determine the actual URL and pass it to our HTML parser tool.

The advantages of this fake object are that we are in control of its behavior and that we still test everything using a real HTTP stack.

## HTML Parser: Testing the Parser Module

Next, we want to test the link extraction behavior of the `HtmlParser` class in isolation.
For this purpose, we use a stub object to replace the required `Fetcher` instance.
The stub object is configured using the library `unittest.mock`.

```python
from unittest import mock

import pytest

from html_parser.fetcher import Fetcher, FetcherError
from html_parser.parser import HtmlParser, HtmlParserError


class TestHtmlParser:
    def setup_method(self, _):
        self._fetcher_mock = mock.Mock(spec=Fetcher)
        self._parser = HtmlParser(self._fetcher_mock)
```
In `setup_method` we define a mock which replaces a real `Fetcher` instance.
This mock exposes all methods of `Fetcher` allowing us to configure the expected behaviour.
With the help of this mock, we construct the `HtmlParser` instance under test.
Now, we can use the mock to provide the required behavior in every test case.

The next step is to use the created object within the test cases.
The first test case shall test the successful extraction of a link.

```python
    def test_extract_links_success(self):
        # Configure the mock
        self._fetcher_mock.retrieve.return_value = "<a href='/index.html'>index.html</a>"

        # Call the method to test
        extracted_links = self._parser.extract_links()

        # Check the assertions
        assert len(extracted_links) == 1
        assert extracted_links[0] == "/index.html"
```

In the `test_extract_links_success` test case, we configure our `Fetcher` mock to return valid HTML when the `retrieve` method is called.
This can be done using the `return_value` attribute of the (mocked) method in question.

The second test case shall test the behavior of the `HtmlParser` when a `FetcherError` is raised within the Fetcher.
The expected behavior is that the `HtmlParser` will raise an `HtmlParserError`.

```python
    def test_extract_links_fetcher_error(self):
        # Configure the mock
        self._fetcher_mock.retrieve.side_effect = FetcherError

        # Call the method to test and check for the expected error
        with pytest.raises(HtmlParserError):
            self._parser.extract_links()
```

In the `test_extract_links_fetcher_error` test case, we used the `side_effect` attribute of the `retrieve` method of `Fetcher`.
This will trigger a `FetcherError` being raised when the method is called.

### Exercise

- Please add further test cases to `parser_test.py`, for example, to test:
  - Parsing an invalid HTML document. \
    Use `<html></html` as invalid HTML document.
  - Parsing a HTML document which contains no links. \
    Use `<html></html>` as empty HTML document.
- Please run all tests to make sure that everything works as expected.
- You can also use the example code on branch [02-add-further-mocked-parser-tests](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/tree/02-add-further-mocked-parser-tests) as an starting point for this exercise.

### Key Points

- Test doubles can be pretty handy to address specific test challenges.
  But try to use the real dependencies as long as it is reasonable.
- Decide on the specific situation which kind of test double is suited most.



## [HTML Parser: Analyzing the Code Coverage](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode05.md)

> Code coverage is a **metric** which indicates the **degree to which the source code is checked by tests**.

### Code Coverage Types

<table>
<tr><th>Code</th><th>Control Flow</th></tr>
<tr>
<td>


```python
def check(x):
    if x > 0:
        y = -x
    else:
        y = x

    while y < 0:
        y += 1
```
</td>
<td>

![Control Flow](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/raw/master/episodes/images/control-flow-coverage.png)

</td>
</tr>
</table>


Typically, one can distinguish the following code coverage types:

- **Statement Coverage (C0):**
  - 100% coverage means every statement is executed once.
  - 2 test cases (e.g., `x = 1`, `x = -1`) are required to achieve 100% statement coverage in the example.
- **Branch Coverage (C1):**
  - 100% coverage means every branch is executed once.
  - 2 test cases (e.g., `x = 1`, `x = -1`) are required to achieve 100% branch coverage in the example.
- **Path Coverage (C2):**
  - 100% coverage means every possible code path is executed once.
  - An infinite number of test cases would be required to achieve 100% path coverage in the example. However, there are also relaxed versions C2 coverage which limit the number of loop executions.

In practice, one usually considers **statement** and **branch** coverage.


### [Analyzing the Code Coverage of the HTML Parser Tool](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode05.md)

> [Example Code: Check code coverage](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/archive/03-check-code-coverage/html-parser-03-check-code-coverage.zip)

- Determine statement coverage:

```bash
$ python -m pytest --cov=html_parser tests
```

- Determine branch coverage:

```bash
$ python -m pytest --cov=html_parser --cov-branch tests
```

- Create a HTML report:

```bash
$ python -m pytest --cov=html_parser --cov-branch --cov-report=html tests
```

#### Exercise

- Please examine the coverage report for every Python module.
  What aspects of the code could require further tests?
- The report indicates a missing special case: `<a>` tags without `href` attributes (e.g., `<a>no href</a>`).
  Please add a test case to `parser_test.py` which covers this special case and check its effect on the coverage report.


### Key Points

- Use code coverage as a tool to detect room for improvements ("test holes").
- `coverage.py` is an excellent tool for measuring and analyzing code coverage of Python programs.


## [HTML Parser: Improving the Test Suite and the Code Structure](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode06.md)

- Based on the coverage analysis we started improving the code and the test suite:
  - Added more error handling tests
  - Decoupled `parser.py` and `fetcher.py` 
- Finally, we want to take a closer look at the test suite structure.

### Refactoring of the Parser Module

<table>
<tr><th></th><th>main.py</th><th>parser.py</th></tr>

<tr>
<td>Before</td>
<td>

```python
fetcher = create_fetcher(path)
parser = HtmlParser(fetcher)
try:
    extracted_links = parser.extract_links()
except HtmlParserError as error:
    ...
```

</td>
<td>

```python
def __init__(self, fetcher):
    self._fetcher = fetcher

def extract_links(self):
    try:
        html_document = self._fetcher.retrieve()
    except FetcherError as error:
        raise HtmlParserError("Cannot retrieve content.")
    else:
        parser = bs4.BeautifulSoup(html_document, "html.parser")
        ...
```

</td>
</tr>
<tr>
<td>After</td>
<td>

```python
try:
    fetcher = create_fetcher(path)
    html_document = fetcher.retrieve()
    parser = HtmlParser(html_document)
    extracted_links = parser.extract_links()
except (FetcherError, HtmlParserError) as error:
    ...
```

</td>
<td>

```python
def __init__(self, html_document):
    self._html_document = html_document

def extract_links(self):
    parser = bs4.BeautifulSoup(self._html_document, "html.parser")
    ...        
```

</td>
</tr>
</table>


### Analyzing the Structure of the Test Suite (Live Demonstration)

> [Code Example: Mark test types](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/html-parser/-/archive/04-mark-test-types/html-parser-04-mark-test-types.zip)

#### Execute **all** tests

```bash
python -m pytest  --cov=html_parser --cov-branch tests
```

- Number of tests: 16
- Execution time 5.24s
- Coverage: 97%

#### Execute only *large* tests:

```bash
python -m pytest -m "large" --cov=html_parser --cov-branch tests
```

- Number of tests: 4
- Execution time 3.11s
- Coverage: 93%

#### Execute only *medium* tests:

```bash
 python -m pytest -m "medium" --cov=html_parser --cov-branch tests
```

- Number of tests: 5
- Execution time 2.80s
- Coverage: 38%


#### Execute only *small* tests (i.e., not *medium* or *large*):

```bash
python -m pytest -m "not large and not medium" --cov=html_parser --cov-branch tests
```

- Number of tests: 7
- Execution time 0.25s
- Coverage: 41%

#### Execute only *small* **and** *medium* tests (i.e., not *medium* or *large*):

```bash
python -m pytest -m "not large" --cov=html_parser --cov-branch tests
```

- Number of tests: 12
- Execution time 2.81s
- Coverage: 55%

#### Summary

- Even our more coordinator code centered application fits to the test pyramid concept (7->5->4). In the example, only the `parser.py` is well suited for writing small tests.
- Execution times:
  - Large tests took the longest execution time (0.78s per test case).
  - Small tests are really fast (0.036s per test case)!
- Code coverage:
  - Large tests produce a lot of code coverage (93%) with only 4 test cases. But this coverage lacks proper assertions.
  - Medium and small tests produce a good portion of code coverage (55%). But they allow more fine-grained assertions
- Overall, the test suite looks fine. In future, we expect a growing number of small tests. Particularily, for new features of the `parser.py` module.


### Key Points

- A safety net consisting of automated tests helps a lot to perform refactoring activities safely.
- `pytest markers` make it easy to select the tests that you want to execute.
- It is important that you have the right mix of tests in your test suite.


## [HTML Parser: Build Automation and CI/CD with GitLab](https://gitlab.com/hifis/hifis-workshops/test-automation-with-python/workshop-materials/-/blob/master/episodes/episode07.md)

### Key Points

- Build automation and a suitable build script are important to standardize testing and additional tests.
- GitLab offers a good support for collaboration and build automation via merge requests and build pipelines.

## Wrap Up Day 2

- Short insight into Property Based Testing?

