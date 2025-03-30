from os import getenv
from pydantic import SecretStr

class Settings():
    BOT_TOKEN: SecretStr = SecretStr(getenv('BOT_TOKEN'))
    MONGODB_URL: SecretStr = SecretStr(getenv('MONGODB_URL'))
    MONGODB_DB: SecretStr = SecretStr(getenv('MONGODB_DB'))
    LOGGING_CHAT: str = getenv('LOGGING_CHAT')

SETTINGS = Settings()