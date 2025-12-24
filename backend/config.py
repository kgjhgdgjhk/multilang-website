from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MultiLang Website"
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./test.db"
    
    class Config:
        env_file = ".env"

settings = Settings()