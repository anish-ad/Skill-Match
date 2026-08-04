from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()