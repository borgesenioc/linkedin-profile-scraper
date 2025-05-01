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

    # onfrontiers/client.py
    def balance_cents(self, billing_id: str) -> int | None:
        data = self._client.execute(
            _BALANCE_QUERY, variable_values={"id": billing_id}
        )
        acct = data.get("billingAccount")
        if not acct:
            return None

        # Some GraphQL scalars come back as str → normalise to int
        cents_raw = acct["credit_balance"]["cents"]
        try:
            return int(cents_raw)
        except (TypeError, ValueError):
            # unexpected payload; bubble up or log as needed
            raise RuntimeError(f"Unexpected cents value: {cents_raw!r}")

    # example skeleton for later:
    # def create_unregistered_expert(self, **kwargs): …

# convenience factory
def get_client() -> OnFrontiersClient:
    return OnFrontiersClient()