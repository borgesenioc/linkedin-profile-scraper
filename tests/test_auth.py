from onfrontiers.auth import fetch_token

def test_fetch_token():
    token = fetch_token()
    # crude JWT sanity-check: three dot-separated chunks
    assert token and token.count(".") == 2