import os
from os.path import dirname, join

from dotenv import load_dotenv

env_path = join(dirname(__file__), "sercrets/.env")
load_dotenv(env_path)


DB_NAME: str = str(os.environ.get("DB_NAME"))
DB_HOST: str = str(os.environ.get("DB_HOST"))
DB_PORT: str = str(os.environ.get("DB_PORT"))
DB_USER: str = str(os.environ.get("DB_USER"))
DB_PASSWORD: str = str(os.environ.get("DB_PASSWORD"))
