# Playwright PoC (pytest)

Simple Playwright + pytest proof-of-concept. This README explains how to set up the environment and run tests.

## Prerequisites
- Linux (instructions assume bash)
- Python 3.8+
- git (optional)

## Quick setup
1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install test dependencies (adjust if you have requirements.txt):
```bash
pip install pytest pytest-playwright pytest-html
pip install playwright
```

3. Install Playwright browsers:
```bash
playwright install
```

## Environment options
- Run browser slower for debugging: set PLAYWRIGHT_SLOW_MO in milliseconds (default used in this project is 200):
```bash
export PLAYWRIGHT_SLOW_MO=500
```
- Run tests in headless mode by passing `--headless` to pytest (see commands below).

## Run tests
Run the full test suite and generate an HTML report:
```bash
pytest -s --html=reports/report.html --self-contained-html
```

Run tests headless:
```bash
pytest -s --headless
```

Run a single test file or test:
```bash
pytest tests/test_example.py -q
pytest tests/test_example.py::test_name -q
pytest -s --html=reports/report.html --self-contained-html --tracing on
```

Useful flags:
- `-k <expr>` run tests matching expression
- `-x` stop after first failure
- `-q` quiet output
- `-s` show print/log output
- `--maxfail=N` stop after N failures

## Screenshot on failure
This project captures page screenshots automatically for failing tests. Screenshots are saved under:
```
./screenshots/
```
Filenames include a sanitized test name and timestamp.

## Reports and artifacts
- HTML report: `reports/report.html` (created when you use `--html`)
- Screenshots: `screenshots/`

Create directories if needed (tests will create them automatically when saving artifacts).

## Cleaning
Remove generated reports and screenshots:
```bash
rm -rf reports screenshots .pytest_cache
```

## CI notes (basic)
- Ensure dependencies are installed and `playwright install` is run.
- Set up a virtualenv or use the system Python.
- Run `pytest -q --html=reports/report.html --self-contained-html` and store `reports/` and `screenshots/` as build artifacts.

## Tips
- Use `PLAYWRIGHT_SLOW_MO` and non-headless mode to visually debug flaky tests.
- Keep tests idempotent and isolated — the fixture in this project creates a new browser context per test.

If you want, add a `requirements.txt` with pinned versions and a GitHub Actions workflow to run tests on push.