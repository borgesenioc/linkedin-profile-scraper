from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from requests.auth import HTTPBasicAuth
from .config import settings

_AUTH_MUTATION = gql("""
mutation CreateToken($client_id: String!) {
  createToken(client_id: $client_id) { token }
}
""")

def fetch_token(email: str = settings.of_email,
                password: str = settings.of_password) -> str:
    """Return a fresh JWT using basic-auth + external header."""
    transport = RequestsHTTPTransport(
        url=settings.of_api_url,
        auth=HTTPBasicAuth(email, password),
        headers={"X-OnFrontiers-External-Auth": settings.of_external_auth},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    resp = client.execute(_AUTH_MUTATION, variable_values={"client_id": "bot"})
    return resp["createToken"]["token"]