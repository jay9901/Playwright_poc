# from playwright.sync_api import Page
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.username = "#user-name"
        self.password = "#password"
        self.login_btn = "#login-button"
        self.error_msg = ".error-message-container"

    def open(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.page.fill(self.username, username)
        self.page.fill(self.password, password)
        self.page.click(self.login_btn)

    def verify_login_success(self):
        expect(self.page.locator(".inventory_list")).to_be_visible(timeout=5000)

    def verify_login_failure(self):
        expect(self.page.locator(self.error_msg)).to_be_visible(timeout=5000)