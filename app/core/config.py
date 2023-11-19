from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Сервис сбора пожертвований для котиков.'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'NEW_SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
