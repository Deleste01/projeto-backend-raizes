import sys
import os

sys.path.append(os.path.abspath('.'))

try:
    # Tenta importar o app e o db de diferentes formas comuns
    try:
        from run import app
        from app import db
    except ImportError:
        from app import create_app, db
        app = create_app()

    # Tenta importar o Produto (seja de models direto ou de app.models)
    try:
        from models import Produto
    except ImportError:
        from app.models import Produto

    with app.app_context():
        produto_existente = Produto.query.get(1)
        if not produto_existente:
            db.session.add(Produto(id=1, nome='Produto Teste', preco=10.0))
            db.session.commit()
            print('Sucesso: Produto ID 1 criado com sucesso!')
        else:
            print('Aviso: O Produto ID 1 já existe no banco.')
except Exception as e:
    print('Erro ao inserir produto:', e)
