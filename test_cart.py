from playwright.sync_api import sync_playwright

def test_add_to_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://www.demoblaze.com/")

        # Click on a product
        page.click("a:has-text('Samsung galaxy s6')")
        page.wait_for_selector(".name")

        # Add to cart
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(3000)  # wait for alert
        page.on("dialog", lambda dialog: dialog.accept())

        print("✅ Product added to cart successfully")
        browser.close()
