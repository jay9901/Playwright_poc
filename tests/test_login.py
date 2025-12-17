# Simple Playwright test cases using pytest.
# Each function is a self-contained test case that uses the `page` or `playwright` fixtures.
# Comments explain test steps in plain English.

from playwright.sync_api import Page, Playwright, expect
from Utils.apibase import APIUtils
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_login_success(page, credentials):
    login = LoginPage(page)

    login.open()
    login.login(credentials["valid_user"], credentials["valid_password"])
    login.verify_login_success()

    assert "/inventory.html" in page.url

def test_login_failure(page, credentials):
    login = LoginPage(page)

    login.open()
    login.login(credentials["invalid_user"], credentials["invalid_password"])
    login.verify_login_failure()

def test_add_item_to_cart(page, credentials):
    login = LoginPage(page)
    inventory = InventoryPage(page)

    login.open()
    login.login(credentials["valid_user"], credentials["valid_password"])

    inventory.add_backpack_to_cart()
    inventory.verify_cart_count("1")

def test_remove_item_from_cart(page, credentials):
    login = LoginPage(page)
    inventory = InventoryPage(page)

    login.open()
    login.login(credentials["valid_user"], credentials["valid_password"])

    inventory.add_backpack_to_cart()
    inventory.remove_backpack_from_cart()
    inventory.verify_cart_empty()




