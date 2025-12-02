from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_field = "#user-name"
        self.password_field = "#password"
        self.login_button = "#login-button"
        self.inventory_container = ".inventory_list"

    def goto(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.login_button)

    def is_login_successful(self) -> bool:
        return self.page.is_visible(self.inventory_container)
