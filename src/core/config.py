import json

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="auth_")

    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

    JWT_PUBLIC: str = (BASE_DIR / "creds" / "jwt-public.pem").read_text()
    JWT_PRIVATE: str = (BASE_DIR / "creds" / "jwt-private.pem").read_text()

class DatabaseSettings(BaseSettings):
    # env_prefix="db_" означает, что в .env ищем db_user, db_host и т.д.
    model_config = SettingsConfigDict(env_prefix="db_", env_file=".env", extra="ignore")
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    name: str = "online_store"

    @property
    def URL(self):
        # Для asyncpg используем правильный драйвер
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_", env_file=".env", extra="ignore")
    host: str = "localhost"
    port: int = 6379

    @property
    def url(self):
        # Redis обычно использует протокол redis://, а не http://
        return f"redis://{self.host}:{self.port}"

class Settings(BaseSettings):
    # Указываем Pydantic, что нужно искать переменные в окружении и .env
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", extra="ignore")
    
    port: int = 8000
    # Инициализируем через Field или просто оставляем тип, 
    # чтобы Pydantic сам собрал их из окружения
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()

    CATEGORIES: list[str] = json.loads((BASE_DIR / "core" / "categories.json").read_text(encoding="utf-8"))

settings = Settings()