all: audit

clean:
	rm -rf build
	rm -rf dist
	poetry run coverage erase

prepare:
	mkdir -p build

test: prepare
	poetry run pytest --junit-xml=build/tests.xml tests/

test-quick: prepare
	poetry run pytest --junit-xml=build/tests.xml -m "not large" tests/

formatting:
	poetry run black .

check-formatting:
	poetry run black . --check

check-code:
	poetry run flake8 html_parser tests

check-coverage-small-medium: prepare
	poetry run pytest --cov=. --cov-fail-under=50 --cov-report=term-missing -m "not large" tests/

check-coverage: prepare
	poetry run pytest --cov=. --cov-fail-under=90 --cov-report=term-missing --cov-report=html --cov-report=xml tests/

check-license-metadata:
	poetry run reuse lint

audit: check-formatting check-code check-coverage-small-medium check-coverage check-license-metadata

package: prepare
	poetry build -f sdist
