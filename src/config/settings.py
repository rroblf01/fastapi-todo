from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    HOST_DB: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
