import os
from dotenv import load_dotenv

# Carrega o arquivo .env da raiz
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-chave-raizes")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "fallback-jwt-raizes")
    
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "raizes_nordeste_db")
    
    # Tratamento caso rode com root sem senha localmente
    if DB_USER == "root" and not DB_PASSWORD:
        # Conecta usando o arquivo de socket do mysql do linux
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}@{DB_HOST}/{DB_NAME}?unix_socket=/var/run/mysqld/mysqld.sock"
    else:
        # Linha de conexao padrao por ip/porta
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False