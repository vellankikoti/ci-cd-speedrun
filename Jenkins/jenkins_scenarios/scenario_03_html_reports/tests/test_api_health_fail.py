import requests

def test_api_healthcheck_fail():
    response = requests.get("http://httpbin.org/status/500", timeout=5)
    assert response.status_code == 200
