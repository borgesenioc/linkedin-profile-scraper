# tests/test_client.py
from onfrontiers import OnFrontiersClient

def test_balance_query():
    client = OnFrontiersClient()
    assert client.balance_cents("918") is not None