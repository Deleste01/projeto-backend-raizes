from app.infrastructure.database import db
from app.domain.models import Unidade, Produto, Estoque, Usuario

UNIDADE_PADRAO = {'id': 1, 'nome': 'Unidade Paraty', 'cidade': 'Paraty'}

PRODUTOS_PADRAO = [
    {'id': 1, 'nome': 'Tapioca de Carne de Sol', 'preco': 18.50},
    {'id': 2, 'nome': 'Suco de Graviola 400ml', 'preco': 8.00}
]

ESTOQUE_INICIAL = 50


def popular_dados_iniciais():
    
    unidade = Unidade.query.get(UNIDADE_PADRAO['id'])
    if not unidade:
        unidade = Unidade(**UNIDADE_PADRAO)
        db.session.add(unidade)
        db.session.flush()

    
    for dados in PRODUTOS_PADRAO:
        produto = Produto.query.get(dados['id'])
        if not produto:
            produto = Produto(**dados)
            db.session.add(produto)
            db.session.flush()

        
        estoque = Estoque.query.filter_by(unidade_id=unidade.id, produto_id=produto.id).first()
        if not estoque:
            novo_estoque = Estoque(
                unidade_id=unidade.id, 
                produto_id=produto.id, 
                quantidade=ESTOQUE_INICIAL
            )
            db.session.add(novo_estoque)

    
    
    if not Usuario.query.filter_by(email='gustavo@raizes.com').first():
        usuario_func = Usuario(
            nome='Gustavo (Funcionario)',
            email='gustavo@raizes.com',
            role='funcionario'
        )
        usuario_func.set_senha('meusegredo123')
        db.session.add(usuario_func)
        
    
    if not Usuario.query.filter_by(email='cliente@raizes.com').first():
        usuario_cliente = Usuario(
            nome='Cliente de Teste',
            email='cliente@raizes.com',
            role='cliente'
        )
        usuario_cliente.set_senha('cliente123')
        db.session.add(usuario_cliente)
        

    db.session.commit()
    print("Carga inicial de dados finalizada com sucesso.")
    return unidade