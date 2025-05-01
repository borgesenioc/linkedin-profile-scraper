# of_api_test.py
from dotenv import load_dotenv
import os
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from requests.auth import HTTPBasicAuth

load_dotenv()

email         = os.getenv("ONFRONTIERS_API_EMAIL")
password      = os.getenv("ONFRONTIERS_API_PASSWORD")
api_url       = os.getenv("ONFRONTIERS_API_URL")
external_auth = os.getenv("X_ONFRONTIERS_EXTERNAL_AUTH")

# --- 1) login ---------------------------------------------------------------
AUTH_MUTATION = gql("""
mutation CreateToken($client_id: String!) {
  createToken(client_id: $client_id) { token }
}
""")

def create_token() -> str:
    transport = RequestsHTTPTransport(
        url=api_url,
        auth=HTTPBasicAuth(email, password),
        headers={"X-OnFrontiers-External-Auth": external_auth},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    resp = client.execute(AUTH_MUTATION, variable_values={"client_id": "bot"})
    return resp["createToken"]["token"]

# --- 2) balance query -------------------------------------------------------
BALANCE_QUERY = gql("""
query BillingBalance($id: String!) {      # ← String! here
  billingAccount(id: $id) {
    credit_balance { cents }
  }
}
""")

def get_balance(billing_id: str, token: str) -> int | None:
    transport = RequestsHTTPTransport(
        url=api_url,
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    data = client.execute(BALANCE_QUERY, variable_values={"id": billing_id})
    acct = data.get("billingAccount")
    return acct["credit_balance"]["cents"] if acct else None

if __name__ == "__main__":
    token = create_token()
    cents = get_balance("918", token)
    print("Balance:", cents)