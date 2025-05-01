# tests/test_client.py
from onfrontiers import OnFrontiersClient

def test_fetch_token():
    token = OnFrontiersClient.fetch_token()
    assert token and token.count(".") == 2       # crude JWT sanity-check