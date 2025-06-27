from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str 
    DATABASE_URL:str
    POSTGRES_PORT: int 
    HOST:str
    PORT:str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://postgres:root"
            f"@localhost:5432/Recipe"
        )

settings = Settings()
