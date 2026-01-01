import requests

BASE_URL = "http://127.0.0.1:8000"

def test_login_page_accessibility():
    url = f"{BASE_URL}/accounts/login/"
    try:
        response = requests.get(url, timeout=30)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        content = response.text.lower()
        assert "invite-only" in content or "invitation" in content or "authentication" in content, \
            "Login page does not indicate invite-only authentication mechanism."
    except requests.RequestException as e:
        assert False, f"Request to login page failed: {e}"

test_login_page_accessibility()