from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    mail_username: str = "wombat"
    mail_password: str = "wombacisko"
    mail_from: str = "wombat@wombat.com"
    mail_port: int = 37643
    mail_server: str = "wombat.server"
    redis_host: str
    redis_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    # cloudinary_name: str
    # cloudinary_api_key: str
    # cloudinary_api_secret: str
    email_verification_required: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
