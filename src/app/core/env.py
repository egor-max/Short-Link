from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class FastApiSettings(BaseSettings):

    app_host: str
    app_port: int
    app_description: str
    app_title: str
    app_debug: bool


class PostgresSettings(BaseSettings):

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def postgres_url(self) -> str:

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        ).unicode_string()


class Settings(FastApiSettings, PostgresSettings):

    model_config= ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
