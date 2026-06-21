from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instancia o banco e as migrations globais
db = SQLAlchemy()
migrate = Migrate()