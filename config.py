# from pydantic import BaseModel, field_validator
# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str
#
#     @property
#     def get_database_url(self):
#         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
#
#     class Config:
#         env_file = '.env'
#
#
# settings = Settings()
#
# print(settings.DATABASE_URL)

from pydantic import BaseModel
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

    class Config:
        env_file = '.env'


settings = Settings()
Settings.get_database_url(settings.__dict__)


