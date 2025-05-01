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

AUTH_MUTATION = gql("""
mutation CreateToken($client_id: String!) {
  createToken(client_id: $client_id) {
    token
  }
}
""")

def auth(email: str, password: str, url: str, external_auth: str) -> str:
    transport = RequestsHTTPTransport(
        url=url,
        auth=HTTPBasicAuth(email, password),
        headers={"X-OnFrontiers-External-Auth": external_auth},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    resp = client.execute(AUTH_MUTATION, variable_values={"client_id": "bot"})
    return resp["createToken"]["token"]

if __name__ == "__main__":
    assert all([email, password, api_url, external_auth]), "Missing env vars"
    try:
        token = auth(email, password, api_url, external_auth)
        print("Successfully logged in!\nToken:", token)
    except Exception as e:
        print("Failed to log in:", e)