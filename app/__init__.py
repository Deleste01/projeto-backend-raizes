from flask import Flask
from flask_cors import CORS
from config import Config
from app.infrastructure.database import db, migrate

def create_app():
    app = Flask(__name__)
    
    # pega as configs que estao no arquivo config.py
    app.config.from_object(Config)
    
    # libera o cors pros testes
    CORS(app)
    
    # inicia o banco e as migrations ligadas no app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # garante que os modelos vao pro sqlalchemy antes das rotas
    from app.domain import models 
    
    # blueprints das rotas
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.pedidos import pedidos_bp
    app.register_blueprint(pedidos_bp)
    
    # comando cli para dar o seed inicial nas tabelas
    import click
    @app.cli.command("seed-db")
    def seed_db():
        from app.domain.models import Unidade, Produto, Estoque
        
        # cria a unidade inicial se ja nao tiver cadastrada
        unidade = Unidade.query.filter_by(nome="Unidade Paraty").first()
        if not unidade:
            unidade = Unidade(nome="Unidade Paraty", cidade="Paraty")
            db.session.add(unidade)
            db.session.flush() 
        
        # itens do cardapio para o teste do fluxo
        produtos_dados = [
            {"id": 101, "nome": "Tapioca de Carne de Sol", "preco": 18.50},
            {"id": 305, "nome": "Suco de Graviola 400ml", "preco": 8.00}
        ]
        
        for prod in produtos_dados:
            item = Produto.query.get(prod["id"])
            if not item:
                item = Produto(id=prod["id"], nome=prod["nome"], preco=prod["preco"])
                db.session.add(item)
                db.session.flush()
            
            # poe estoque inicial pro item nessa unidade
            estoque_unidade = Estoque.query.filter_by(unidade_id=unidade.id, produto_id=item.id).first()
            if not estoque_unidade:
                estoque_unidade = Estoque(unidade_id=unidade.id, produto_id=item.id, quantidade=50)
                db.session.add(estoque_unidade)
                
        db.session.commit()
        click.echo("Banco de dados populado com sucesso para a Rede Raízes do Nordeste!")
    
    return app