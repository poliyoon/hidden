import requests

BASE_URL = "http://127.0.0.1:8000"
PROFILE_URL = f"{BASE_URL}/profile/"
LOGIN_URL = f"{BASE_URL}/accounts/login/"

def test_profile_page_displays_user_details_and_preferences():
    session = requests.Session()
    try:
        # First, access the profile page without authentication to ensure redirect or denial
        response = session.get(PROFILE_URL, allow_redirects=False, timeout=30)
        # If not authenticated, expect 302 redirect to login
        if response.status_code == 302:
            # Follow redirect location should be login page or related
            assert '/accounts/login/' in response.headers.get('Location', ''), "Redirect location should be login page"
            # Need to perform login to access profile page
        else:
            # If no redirect and status is 200, but user not authenticated? Fail because user must be authenticated
            assert response.status_code != 200, "Unauthenticated access to profile page should redirect or deny"

        # Perform login - GET login page to get CSRF token
        login_get_resp = session.get(LOGIN_URL, timeout=30)
        assert login_get_resp.status_code == 200, "Login page must be accessible"

        # Extract CSRF token from cookies or login page form (Django default: csrftoken cookie)
        csrf_token = session.cookies.get('csrftoken', '')
        assert csrf_token, "CSRF token not found in login page cookies"

        # Prepare login payload - assumed keys: username and password per Django default
        # NOTE: Credentials must be supplied or known. For testing, use placeholder user.
        login_payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'csrfmiddlewaretoken': csrf_token,
        }
        login_headers = {
            'Referer': LOGIN_URL,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Post login form
        login_post_resp = session.post(LOGIN_URL, data=login_payload, headers=login_headers, timeout=30, allow_redirects=True)
        # After login, the typical status code is 200 or 302 redirect
        assert login_post_resp.status_code in (200, 302), "Login POST must return status 200 or redirect"
        # If redirect after login, follow protection not needed as session maintains cookies and auth

        # Now access profile page authenticated
        profile_resp = session.get(PROFILE_URL, timeout=30)
        assert profile_resp.status_code == 200, f"Profile page must return 200 for authenticated user, got {profile_resp.status_code}"

        # Validate response content contains expected user details and preferences placeholders
        content = profile_resp.text
        # We expect user details like username or preferences keywords in HTML content. Checking basic presence:
        assert "testuser" in content.lower() or "user" in content.lower(), "Profile page should display user details"
        assert "preferences" in content.lower(), "Profile page should display user preferences"

    finally:
        session.close()

test_profile_page_displays_user_details_and_preferences()