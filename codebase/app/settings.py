from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    APP_HOST: str = "localhost"
    APP_PORT: int = 8080
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "test"
    DB_USER: str = "test"
    DB_PASSWORD: str = "test"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

env = Settings()
password = quote_plus(env.DB_PASSWORD)  # Safely encode any special characters
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{env.DB_USER}:{password}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}?autocommit=true&charset=utf8mb4"
)