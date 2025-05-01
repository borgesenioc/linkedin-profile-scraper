from onfrontiers import OnFrontiersClient

def test_balance_query():
    client = OnFrontiersClient()
    balance = client.balance_cents("918")      # use a billing-ID you can see
    assert balance is not None and balance >= 0