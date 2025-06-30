import requests

def test_api_healthcheck_pass():
    response = requests.get("http://httpbin.org/status/200", timeout=5)
    assert response.status_code == 200
