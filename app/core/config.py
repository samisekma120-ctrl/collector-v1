from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="collector-v1", alias="APP_NAME")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")

    # DB (utilisé plus tard, gardé dès le socle)
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
        alias="DATABASE_URL",
    )

    # Auth placeholders (socle)
    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")


settings = Settings()
