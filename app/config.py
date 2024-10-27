from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

    def get_db_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DATABASE_URL}"


settings = Settings()
