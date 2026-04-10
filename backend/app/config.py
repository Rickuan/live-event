from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    admin_username: str
    admin_password_hash: str
    secret_key: str
    cors_origins: str = "http://localhost:5173"

    model_config = {"env_file": ".env"}


settings = Settings()
