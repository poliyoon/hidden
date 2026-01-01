import requests

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/accounts/login/"
HOME_URL = BASE_URL + "/"

def test_home_page_access_for_authenticated_users():
    session = requests.Session()
    try:
        # Obtain login page to get cookies if any
        login_get_resp = session.get(LOGIN_URL, timeout=30)
        assert login_get_resp.status_code == 200, "Login page did not load correctly"

        # Perform login - credentials need to be valid for successful authentication
        login_payload = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_post_resp = session.post(LOGIN_URL, data=login_payload, timeout=30, allow_redirects=False)
        # Expect a redirect (302) on successful login to home/dashboard
        assert login_post_resp.status_code in [302, 303], f"Login failed or unexpected status: {login_post_resp.status_code}"
        assert "location" in login_post_resp.headers, "Redirect location missing after login"
        assert login_post_resp.headers["location"] in ["/", "/home", "/dashboard", "/"], "Unexpected redirect location after login"

        # Access home page as authenticated user
        home_resp = session.get(HOME_URL, timeout=30)
        assert home_resp.status_code == 200, f"Home page did not load properly for authenticated user, status: {home_resp.status_code}"
        # Check presence of curated luxury content indicator text or meta description in response content (simple check)
        assert b"curated" in home_resp.content.lower() or b"luxury" in home_resp.content.lower(), "Curated luxury content not found on home page"

    finally:
        session.close()

test_home_page_access_for_authenticated_users()
