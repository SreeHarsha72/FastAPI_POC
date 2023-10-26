from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_name: str
    database_hostname: str
    database_port: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"

settings = Settings()