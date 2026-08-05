from app.infrastructure.database import db
from app.domain.models import Unidade, Produto, Estoque

UNIDADE_PADRAO = {'id': 1, 'nome': 'Unidade Paraty', 'cidade': 'Paraty'}

PRODUTOS_PADRAO = [
    {'id': 1, 'nome': 'Tapioca de Carne de Sol', 'preco': 18.50},
    {'id': 2, 'nome': 'Suco de Graviola 400ml', 'preco': 8.00}
]

ESTOQUE_INICIAL = 50


def popular_dados_iniciais():
    # Verifica se a unidade ja esta no banco
    unidade = Unidade.query.get(UNIDADE_PADRAO['id'])
    if not unidade:
        unidade = Unidade(**UNIDADE_PADRAO)
        db.session.add(unidade)
        db.session.flush()

    # Percorre a lista de produtos padrao
    for dados in PRODUTOS_PADRAO:
        produto = Produto.query.get(dados['id'])
        if not produto:
            produto = Produto(**dados)
            db.session.add(produto)
            db.session.flush()

        # Cria o estoque amarrando produto e unidade
        estoque = Estoque.query.filter_by(unidade_id=unidade.id, produto_id=produto.id).first()
        if not estoque:
            novo_estoque = Estoque(
                unidade_id=unidade.id, 
                produto_id=produto.id, 
                quantidade=ESTOQUE_INICIAL
            )
            db.session.add(novo_estoque)

    db.session.commit()
    print("Carga inicial de dados finalizada com sucesso.")
    return unidade