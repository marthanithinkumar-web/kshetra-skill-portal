# Use pydantic v2 settings API when available
try:
    # pydantic v2
    from pydantic_settings import BaseSettings
except Exception:
    # fallback for older pydantic versions
    from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8'
    }

settings = Settings()
