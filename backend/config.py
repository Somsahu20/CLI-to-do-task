from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Get the project root directory (parent of backend folder)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"



class Settings(BaseSettings):
    db_name: str
    db_host: str
    db_port: str
    password: str
    db_user: str
    url: str

    model_config = SettingsConfigDict(env_file=str(ENV_FILE),
                                      env_file_encoding='utf-8',
                                    case_sensitive=False)

settings = Settings()