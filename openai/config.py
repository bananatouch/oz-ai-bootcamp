# 환경 구성(configuration) 관리 파일
from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
settings.openai_api_key