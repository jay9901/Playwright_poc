import re
import os
from pathlib import Path
from datetime import datetime
from contextlib import suppress
from typing import Generator

import shutil
from pathlib import Path
import pytest
from playwright.sync_api import Error as PlaywrightError, Page, Playwright, Browser, BrowserContext

def pytest_sessionstart(session):
    """
    Runs once before ANY test.
    Cleans the screenshots folder to ensure fresh execution.
    """
    screenshots_dir = Path(session.config.rootpath) / "screenshots"
    if screenshots_dir.exists():
        shutil.rmtree(screenshots_dir)
        print("🧹 Old screenshots removed.")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    print("📁 Fresh screenshot folder created.")

# Provide a simple CLI flag to run browsers in headless mode
def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")

@pytest.fixture(scope="function")
def page(request, playwright: Playwright) -> Generator[Page, None, None]:
    """
    Per-test Playwright Page fixture:
    - launches a Chromium browser
    - creates a fresh context and page for each test
    - attaches page to the test node so the failure hook can access it
    - ensures browser/context are closed even if the test fails
    """
    headless = request.config.getoption("--headless")
    # allow overriding default slow_mo via environment variable (milliseconds)
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "200"))

    browser: Browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()

    # attach page to the test node so pytest hooks can grab it on failure
    request.node.page = page

    try:
        yield page
    finally:
        # close resources, ignoring any errors during shutdown
        with suppress(Exception):
            context.close()
        with suppress(Exception):
            browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test phase.
    If the test 'call' phase failed and a page is available, capture a screenshot.
    Screenshots are saved to ./screenshots/<sanitized_test_name>_<timestamp>.png
    """
    outcome = yield
    result = outcome.get_result()

    if result.when != "call" or not result.failed:
        return

    page = getattr(item, "page", None)
    if page is None:
        # nothing to do if page wasn't created (e.g., a collection/setup failure)
        return

    screenshots_dir = Path(item.config.rootpath) / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    raw_name = getattr(item, "name", item.nodeid)
    safe_name = re.sub(r"[^\w\-.]", "_", raw_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = screenshots_dir / f"{safe_name}_{timestamp}.png"

    try:
        # prefer Playwright's own error type for clearer messages
        page.screenshot(path=str(file_path), full_page=True)
        print(f"\n📸 Screenshot saved: {file_path}")
    except PlaywrightError as e:
        print(f"Screenshot failed (PlaywrightError): {e}")
    except Exception as e:
        print(f"Unexpected error saving screenshot: {e}")
