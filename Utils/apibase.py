# from playwright.sync_api import sync_playwright 
from playwright.sync_api import Playwright

class APIUtils:
    """
    Utility for calling Restful Booker API.
    Handles authentication and reusable requests.
    """

    def __init__(self, playwright: Playwright):
        self.base_url = "https://restful-booker.herokuapp.com"
        self.request_context = playwright.request.new_context()

    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticate to Restful Booker API and return token
        """
        auth_url = f"{self.base_url}/auth"

        response = self.request_context.post(
            auth_url,
            data={
                "username": username,
                "password": password
            }
        )

        if not response.ok:
            raise Exception(f"Auth failed: HTTP {response.status}")

        json_response = response.json()

        if "token" not in json_response:
            raise Exception("Token not found in response: " + str(json_response))

        return json_response["token"]

    def get_booking_ids(self):
        """
        Example request: Get all booking IDs using token
        """
        url = f"{self.base_url}/booking"
        response = self.request_context.get(url)

        if not response.ok:
            raise Exception(f"Failed to fetch bookings: HTTP {response.status}")

        return response.json()

