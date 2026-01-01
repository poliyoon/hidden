import requests
from requests.exceptions import RequestException

BASE_URL = "http://127.0.0.1:8000"
PROFILING_PATH = "/profiling/"
LOGIN_PATH = "/accounts/login/"
TIMEOUT = 30

def test_profiling_page_displays_ai_chat_survey():
    session = requests.Session()
    try:
        # Access profiling page without authentication to verify redirect
        response = session.get(f"{BASE_URL}{PROFILING_PATH}", allow_redirects=False, timeout=TIMEOUT)
        assert response.status_code == 302, f"Expected redirect (302) for unauthenticated access, got {response.status_code}"
        # Follow redirect location to login page
        location = response.headers.get("Location")
        assert location, "Redirect location header missing"
        assert LOGIN_PATH in location, f"Expected redirect to login page but got redirect to {location}"

        # Get login page to retrieve any cookies and session data
        login_page = session.get(f"{BASE_URL}{LOGIN_PATH}", timeout=TIMEOUT)
        assert login_page.status_code == 200, f"Failed to load login page, status code {login_page.status_code}"

        # Perform login with valid credentials - these must be replaced with valid test user credentials
        login_payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        login_response = session.post(f"{BASE_URL}{LOGIN_PATH}", data=login_payload, allow_redirects=True, timeout=TIMEOUT)
        # After login, should redirect to home or another page; status code may be 200 after redirects
        assert login_response.status_code == 200, f"Login failed or unexpected status code {login_response.status_code}"

        # Access profiling page after authentication
        profiling_response = session.get(f"{BASE_URL}{PROFILING_PATH}", timeout=TIMEOUT)
        assert profiling_response.status_code == 200, f"Expected 200 OK for authenticated access, got {profiling_response.status_code}"
        content = profiling_response.text.lower()

        # Validate that AI chat-based preference survey content is present (heuristic checks)
        assert "ai chat" in content or "preference survey" in content or "chat survey" in content or "survey" in content, \
            "Profiling page does not appear to contain AI chat-based preference survey content."

    except RequestException as e:
        assert False, f"Request failed: {e}"
    finally:
        session.close()

test_profiling_page_displays_ai_chat_survey()