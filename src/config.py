from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRY: int

    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",

    )

config = Config()

# Celery configuration
broker_url = config.REDIS_URL
result_backend = config.REDIS_URL
broker_connection_retry_on_startup = True

