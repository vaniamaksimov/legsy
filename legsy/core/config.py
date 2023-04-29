from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SECRET_KEY: str
    APP_TITLE: str
    APP_DESCRIPTION: str

    POSTGRES_SCHEME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str | int
    POSTGRES_DB: str
    DATABASE_URL: str | PostgresDsn | None = None

    @validator('DATABASE_URL', pre=True)
    def db_url_validator(
        cls, value: str, values: dict[str, str]
    ) -> str | PostgresDsn:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme=values.get('POSTGRES_SCHEME'),
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=str(values.get('POSTGRES_PORT')),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    class Config:
        env_file = '.env'


settings = Settings()
