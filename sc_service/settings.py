import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = os.getenv("DB_HOST", "db_stat")
    port: str = os.getenv("DB_PORT", "5432")
    db_user: str = os.getenv("DB_USER", "stat")
    password: str = os.getenv("DB_PASSWORD", "stat")
    db_name: str = os.getenv("DB_NAME", "stat")
    secure_token: str = os.getenv("SECURE_TOKEN", "mXTBFv4hmo6E9*jsD**vV@Zu")

    @property
    def uri_engine(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.password}@{self.host}:{self.port}"
        )

    @property
    def uri_postgresql(self):
        return f"postgresql://{self.db_user}:{self.password}@{self.host}:{self.port}"


app_config = Settings()
