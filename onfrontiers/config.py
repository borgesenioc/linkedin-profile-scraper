"""
onfrontiers.config
~~~~~~~~~~~~~~~~~~

Loads & validates all environment variables needed for the OnFrontiers API.

* Works with Pydantic v2 (preferred) or v1.
* Pulls variables from the OS or a project-root `.env` via python-dotenv.
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------------------------------- #
# Detect Pydantic major version once and branch                               #
# --------------------------------------------------------------------------- #
try:
    # ---------- Pydantic v2.x ------------------------------------------------
    from pydantic_settings import BaseSettings  # type: ignore
    from pydantic import Field, ValidationError  # type: ignore

    _USING_V2 = True
except ImportError:                             # pragma: no cover
    # ---------- Pydantic v1.x ------------------------------------------------
    from pydantic import BaseSettings, Field, ValidationError  # type: ignore

    _USING_V2 = False

# --------------------------------------------------------------------------- #
# Load .env from the repo root (if present)                                   #
# --------------------------------------------------------------------------- #
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env", override=False)

# --------------------------------------------------------------------------- #
# Settings model                                                              #
# --------------------------------------------------------------------------- #
class Settings(BaseSettings):
    """Validated view of all env-driven config."""

    of_email: str = Field(..., alias="ONFRONTIERS_API_EMAIL")
    of_password: str = Field(..., alias="ONFRONTIERS_API_PASSWORD")
    of_api_url: str = Field(
        "https://api.onfrontiers.com/graphql",
        alias="ONFRONTIERS_API_URL",
    )
    of_external_auth: str = Field(..., alias="X_ONFRONTIERS_EXTERNAL_AUTH")
    of_auth_token: str | None = Field(None, alias="ONFRONTIERS_AUTH_TOKEN")

    # ---------------------- version-specific config ------------------------ #
    if _USING_V2:
        model_config = dict(
            populate_by_name=True,
            extra="ignore",
            case_sensitive=False,
        )
    else:  # v1 style
        class Config:  # type: ignore[missing-class-docstring]
            allow_population_by_field_name = True
            extra = "ignore"
            case_sensitive = False

    # ------------------------------------------------------------------ #
    # helper: safe representation (masks secrets)                         #
    # ------------------------------------------------------------------ #
    def masked(self) -> "Settings":
        data = self.dict()
        if data.get("of_password"):
            data["of_password"] = "***"
        if data.get("of_auth_token"):
            data["of_auth_token"] = data["of_auth_token"][:6] + "…"
        return Settings(**data)  # type: ignore[arg-type]


# Singleton instance imported everywhere else
try:
    settings = Settings()
except ValidationError as exc:  # pragma: no cover
    missing = ", ".join(e["loc"][0] for e in exc.errors())
    raise RuntimeError(f"[config] Missing required env vars: {missing}") from exc