from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Scheduler API"
    ENV: str = "dev"

    # MySQL + PyMySQL
    DATABASE_URL: str = "mysql+pymysql://scheduler:scheduler123@127.0.0.1:3306/scheduler?charset=utf8mb4"

    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MIN: int = 60 * 12

    class Config:
        env_file = ".env"

settings = Settings()
