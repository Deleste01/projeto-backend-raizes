from app import create_app
from app.infrastructure.database import db
from app.infrastructure.seed import popular_dados_iniciais

app = create_app()

with app.app_context():
    db.create_all()
    popular_dados_iniciais()
    print("Banco de dados populado com sucesso para a Rede Raízes do Nordeste!")
