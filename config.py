import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-raizes-local")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "chave-jwt-raizes-local")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'raizes.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
