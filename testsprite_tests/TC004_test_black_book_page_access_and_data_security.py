import requests

BASE_URL = "http://127.0.0.1:8000"
BLACK_BOOK_PATH = "/black-book/"
LOGIN_PATH = "/accounts/login/"
TIMEOUT = 30

# Credentials for a test user - placeholder values, replace with valid test user credentials
TEST_USER_CREDENTIALS = {
    'username': 'testuser',
    'password': 'testpassword'
}

def test_black_book_page_access_and_data_security():
    session = requests.Session()

    # First, attempt to access black book page without authentication
    try:
        unauth_resp = session.get(f"{BASE_URL}{BLACK_BOOK_PATH}", allow_redirects=False, timeout=TIMEOUT)
        # Expecting redirect (302) to login page since user is not logged in
        assert unauth_resp.status_code == 302, f"Expected 302 redirect for unauthenticated access but got {unauth_resp.status_code}"
        location = unauth_resp.headers.get("Location", "")
        assert LOGIN_PATH in location, f"Expected redirect location to contain login page but got: {location}"
    except requests.RequestException as e:
        raise AssertionError(f"Request failed during unauthenticated access check: {e}")

    # Login to obtain authenticated session
    try:
        # Get login page first to get any cookies if needed
        login_get_resp = session.get(f"{BASE_URL}{LOGIN_PATH}", timeout=TIMEOUT)
        assert login_get_resp.status_code == 200, f"Failed to load login page, status code: {login_get_resp.status_code}"

        # Form payload (assuming standard Django login form fields)
        login_payload = {
            'username': TEST_USER_CREDENTIALS['username'],
            'password': TEST_USER_CREDENTIALS['password'],
        }

        login_post_resp = session.post(f"{BASE_URL}{LOGIN_PATH}", data=login_payload, allow_redirects=True, timeout=TIMEOUT)
        # After login, user should not be redirected back to login page
        assert login_post_resp.status_code == 200 or login_post_resp.status_code == 302, f"Unexpected login POST status code: {login_post_resp.status_code}"
        if login_post_resp.history:
            # If redirected, ensure it is not redirected back to login page
            for resp in login_post_resp.history:
                assert LOGIN_PATH not in resp.headers.get("Location", ""), "Login POST redirects back to login page, login may have failed"

    except requests.RequestException as e:
        raise AssertionError(f"Login request failed: {e}")

    # Now try to access black book page authenticated
    try:
        auth_resp = session.get(f"{BASE_URL}{BLACK_BOOK_PATH}", timeout=TIMEOUT)
        assert auth_resp.status_code == 200, f"Expected 200 for authenticated black book access but got {auth_resp.status_code}"

        # Validate that private curated venues data is present
        # Since no API schema defines the JSON, and likely this is a rendered page,
        # we check for expected keywords in response text indicating curated and private venues
        content = auth_resp.text
        # Check presence of indicative phrases - adapt as needed for actual implementation
        assert "Black Book" in content or "curated" in content.lower(), "Response content does not indicate private curated venues"
        # Additional check for login user name or privacy indication (optional)
        assert "Logout" in content or "logout" in content.lower(), "Authenticated page does not show logout option, might not be properly logged in"

    except requests.RequestException as e:
        raise AssertionError(f"Authenticated black book page request failed: {e}")

test_black_book_page_access_and_data_security()