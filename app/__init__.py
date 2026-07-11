from flask import Flask
from flask_cors import CORS
from config import Config
from app.infrastructure.database import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.domain import models  # noqa: F401

    from app.auth import auth_bp
    from app.pedidos import pedidos_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(pedidos_bp)

    from app.infrastructure.seed import popular_dados_iniciais
    with app.app_context():
        db.create_all()
        popular_dados_iniciais()

    @app.cli.command("seed-db")
    def seed_db():
        import click
        popular_dados_iniciais()
        click.echo("Banco de dados populado com sucesso para a Rede Raízes do Nordeste!")

    return app
