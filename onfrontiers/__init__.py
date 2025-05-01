# onfrontiers/__init__.py   ← NEW, inside the package
from .client import OnFrontiersClient, get_client
from .config import settings

__all__ = ["OnFrontiersClient", "get_client", "settings"]