from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()  # search .env in CWD

class Settings(BaseSettings):
    of_email: str = Field(..., env="ONFRONTIERS_API_EMAIL")
    of_password: str = Field(..., env="ONFRONTIERS_API_PASSWORD")
    of_api_url: str = Field("https://api.onfrontiers.com/graphql",
                            env="ONFRONTIERS_API_URL")
    of_external_auth: str = Field(..., env="X_ONFRONTIERS_EXTERNAL_AUTH")
    of_auth_token: str | None = Field(None, env="ONFRONTIERS_AUTH_TOKEN")

settings = Settings()  # singleton import everywhere