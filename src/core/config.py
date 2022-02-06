from typing import Union

from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_BASE_URL: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, list[str]]
    ) -> Union[list[str], str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
