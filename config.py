from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    DATABASE_URL:str
    POSTGRES_PORT: int = 5432  

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://postgres:root"
            f"@localhost:5432/Recipe"
        )

settings = Settings()
