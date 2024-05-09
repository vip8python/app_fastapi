from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @classmethod
    def get_database_url(cls, v):
        cls.DATABASE_URL = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASSWORD']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return cls.DATABASE_URL

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'


settings = Settings()
Settings.get_database_url(settings.__dict__)


