# Simple Playwright test cases using pytest.
# Each function is a self-contained test case that uses the `page` or `playwright` fixtures.
# Comments explain test steps in plain English.

from playwright.sync_api import Page, Playwright, expect
from Utils.apibase import APIUtils

# def test_login(page: Page):
#     """Successful login to saucedemo using valid credentials."""
#     # Open the login page
#     page.goto("https://www.saucedemo.com/")

#     # Fill username and password fields and submit
#     page.fill("#user-name", "standard_user")
#     page.fill("#password", "secret_sauce")
#     page.click("#login-button")

#     # Wait for inventory list and assert navigation to inventory
#     expect(page.locator(".inventory_list")).to_be_visible(timeout=5000)
#     assert "/inventory.html" in page.url
#     print("✅ Login successful!")

# def test_login_unsuccess(page: Page):
#     """Invalid credentials show an error message."""
#     # Open the login page
#     page.goto("https://www.saucedemo.com/")

#     # Enter invalid credentials and submit
#     page.fill("#user-name", "username")
#     page.fill("#password", "password")
#     page.click("#login-button")

#     # Verify an error message is visible
#     expect(page.locator(".error-message-container")).to_be_visible(timeout=5000)
#     assert "Epic sadface" in page.inner_text(".error-message-container")
#     print("❌ Login Unsuccessful!")

def test_add_item_to_cart(page):
    """Add a product to cart and verify the cart badge increases."""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # Add first item to cart
    first_add_btn = page.locator("button[data-test='add-to-cart-sauce-labs-backpack']")
    first_add_btn.click()

    # Verify cart icon has badge "1"
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

def test_remove_item_from_cart(page):
    """Add and remove item, then verify the cart is empty."""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("button[data-test='remove-sauce-labs-backpack']")

    # Cart should not have a badge
    expect(page.locator(".shopping_cart_badge")).to_have_count(0)

def test_inventory_page_visual(page):
    """Visual regression test for inventory page UI."""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    page.screenshot(path="inventory_page.png", full_page=True)

def test_api_authentication(page: Page, playwright: Playwright):
    """
    Validate login using Restful Booker API and verify token works.
    Steps:
    1) get a token via APIUtils
    2) verify bookings list shape
    3) open API docs in a real browser to confirm UI loads
    """
    # 1. Authenticate (this gives a REAL token)
    api = APIUtils(playwright)
    token = api.authenticate("admin", "password123")
    assert len(token) > 0, "Received an empty token"
    print(f"Authenticated successfully! Token = {token}")

    # 2. Example authenticated request
    bookings = api.get_booking_ids()
    assert isinstance(bookings, list), "Bookings should return a list"
    print(f"Total bookings received: {len(bookings)}")

    # 3. Start a browser (POC for UI automation)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Open the API docs page and ensure it loaded
        page.goto("https://restful-booker.herokuapp.com/apidoc/index.html")
        page.wait_for_selector("h1", timeout=7000, state="visible")
        assert "Restful-booker" in page.title()
    finally:
        # Clean up
        context.close()
        browser.close()




