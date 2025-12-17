from playwright.sync_api import Page, expect

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = ".shopping_cart_badge"

    def add_backpack_to_cart(self):
        self.page.click("button[data-test='add-to-cart-sauce-labs-backpack']")

    def remove_backpack_from_cart(self):
        self.page.click("button[data-test='remove-sauce-labs-backpack']")

    def verify_cart_count(self, count: str):
        expect(self.page.locator(self.cart_badge)).to_have_text(count)

    def verify_cart_empty(self):
        expect(self.page.locator(self.cart_badge)).to_have_count(0)
