from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int


# JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
# JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()
