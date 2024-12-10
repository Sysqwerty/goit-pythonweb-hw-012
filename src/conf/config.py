from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application

    Attributes:
        DB_URL (str): Database URL
        JWT_SECRET (str): Secret key for JWT
        JWT_ALGORITHM (str): Algorithm for JWT
        JWT_EXPIRATION_SECONDS (int): Expiration time for JWT

        MAIL_USERNAME (EmailStr): Username for email
        MAIL_PASSWORD (str): Password for email
        MAIL_FROM (EmailStr): Email from
        MAIL_PORT (int): Port for email
        MAIL_SERVER (str): Server for email
        MAIL_FROM_NAME (str): Name for email
        MAIL_STARTTLS (bool): StartTLS for email
        MAIL_SSL_TLS (bool): SSL/TLS for email
        USE_CREDENTIALS (bool): Use credentials for email
        VALIDATE_CERTS (bool): Validate certs for email

        CLD_NAME (str): Name for Cloudinary
        CLD_API_KEY (int): API key for Cloudinary
        CLD_API_SECRET (str): API secret for Cloudinary
    """

    DB_URL: str = ""
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600

    MAIL_USERNAME: EmailStr = "test@mail.com"
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = "test@mail.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLD_NAME: str = ""
    CLD_API_KEY: int = 0
    CLD_API_SECRET: str = ""

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
