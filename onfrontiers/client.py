from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from .auth import fetch_token
from .config import settings

_BALANCE_QUERY = gql("""
query BillingBalance($id: String!) {
  billingAccount(id: $id) { credit_balance { cents } }
}
""")

class OnFrontiersClient:
    """A minimal reusable GraphQL client."""

    def __init__(self, token: str | None = None) -> None:
        self._token = token or fetch_token()
        self._client = Client(
            transport=RequestsHTTPTransport(
                url=settings.of_api_url,
                headers={"Authorization": f"Bearer {self._token}"},
            ),
            fetch_schema_from_transport=False,
        )

    # --- public helpers -------------------------------------------------- #

    def balance_cents(self, billing_id: str) -> int | None:
        data = self._client.execute(
            _BALANCE_QUERY, variable_values={"id": billing_id}
        )
        acct = data.get("billingAccount")
        return acct["credit_balance"]["cents"] if acct else None

    # example skeleton for later:
    # def create_unregistered_expert(self, **kwargs): …

# convenience factory
def get_client() -> OnFrontiersClient:
    return OnFrontiersClient()